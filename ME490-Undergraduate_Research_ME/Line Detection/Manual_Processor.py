import cv2
import numpy as np
import random
import Plot_results as plt
from time import sleep, perf_counter
from Helpers import *

np.set_printoptions(threshold=np.inf, linewidth = 200) # To print more columns in the terminal

cap = cv2.VideoCapture('Videos\Chaos Samples/172.mp4')
width = int(cap.get(3)) # Gets width of capture (there are total of 17 properties)
height = int(cap.get(4))
fps = int(cap.get(5))

resolution = str(width)+'x'+str(height)
filter = "Grey + Custom"

fourcc = cv2.VideoWriter_fourcc(*'XVID') # Also check for .avi, .mp4, .wmv in options.txt
out = cv2.VideoWriter('Extracted Data\Output_DotVid.avi', fourcc, fps, (width,  height))
out2 = cv2.VideoWriter('Extracted Data\Output_MaskVid.avi', fourcc, fps, (width,  height))

"""########################################################################
   ########################## 0-SET PARAMETERS ############################
   ########################################################################"""
scale = 30 # Scale of the micrometer key map
s_map = [[590, 899],[1010, 899]]

rangex_center = [445, 540]
rangey_center = [250, 630]
rangex_outline = [450, 500]
rangey_outline = [190, 700]
roi = [[400, 440], [505, 535]] # y_range, x_range
pixel_length = scale/(np.sqrt((s_map[1][0] - s_map[0][0])**2 + (s_map[1][1] - s_map[0][1])**2))

center_width = round((rangex_center[1] - rangex_center[0])/2) # half width of center border
outline_width = round((rangex_outline[1] - rangex_outline[0])/2) # half width of outline border
outline_height = round((rangey_outline[1] - rangey_outline[0])) # height of the outline border

# Parameters for the curve elimination
d_curves = 30 # Spacing inbetween the curves as filters, center_width/5 might be a good starting point
t_curves = 15 # How far 'bent' curves will be considered in units of pixel

data=np.array([0, 1, 2, "-", "Continuity + Regression", 5, 6, 7, 8, 9, 10, 11], dtype=object)
data = np.vstack([data, data])

start_time = perf_counter()
frameNO = 0
time = 0.0
"""########################################################################
   ########################## 1-PROCESS ###################################
   ########################################################################"""
while True:
    ret, frame = cap.read()  # ret shows if the capture actually works
    if ret:
            frameNO+=1
            time += 1/fps
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image = np.zeros(gray.shape, np.uint8)  # Creates a blank page same res as frame from vid
            image2 = np.zeros(gray.shape, np.uint8)  # For the filtered image
            image[:,:] = gray[:]
            image2[:,:] = gray[:]

            ####################  1.1 Add filter  ##############################
            #image2 = cv2.GaussianBlur(image2, (5,5), 175)            
            #image2 = cv2.bilateralFilter(image2,9,15,15)
            
            image2 = custom_filter(image2, rangex_center, rangey_outline, threshold=1100, noise_thresh = 70, kernel_x=4)
            frame, rangex_center, rangex_outline = track(frame, image2, 743, [420, 540], center_width, outline_width)

            # if frameNO == 15:
            #     filter_debug(gray, image2, roi, thresh=70)
            # frame = cv2.rectangle(frame,(roi[1][0], roi[0][0]), (roi[1][1], roi[0][1]),(0,255,0),1)
            #####################################################################

            ####################  1.2 Find top/bottom connections  ##################
            connection_UP=np.array([0, 0])
            connection_DOWN=np.array([0, 0])
            for row in range(rangey_outline[0], rangey_outline[1]):
                if row < (rangey_outline[0] + (outline_height/3)):
                    index_max = max(range(len(image2[row, rangex_outline[0]:rangex_outline[1]])), key=image2[row, rangex_outline[0]:rangex_outline[1]].__getitem__) + rangex_outline[0]
                    connection_UP = np.vstack([connection_UP, [index_max, row]])
                    # frame = cv2.circle(frame, (index_max, row), 2, (0, 255, 255), -1)
                
                elif (rangey_outline[0] + (2*outline_height/3)) < row:
                    index_max = max(range(len(image2[row, rangex_outline[0]:rangex_outline[1]])), key=image2[row, rangex_outline[0]:rangex_outline[1]].__getitem__) + rangex_outline[0]
                    connection_DOWN = np.vstack([connection_DOWN, [index_max, row]])
                    # frame = cv2.circle(frame, (index_max, row), 2, (0, 255, 255), -1)

            connection_UP = np.delete(connection_UP, (0), axis=0)
            connection_DOWN = np.delete(connection_DOWN, (0), axis=0)

            w1, Y1, x1 = MLE(connection_UP, 2, 0.1, [rangey_outline[0], rangey_outline[0] + (outline_height/3)]) # Least squares fit
            w2, Y2, x2 = MLE(connection_DOWN, 2, 0.1, [rangey_outline[0] + (2*outline_height/3), rangey_outline[1]]) # Least squares fit
            top = round(x1[0]) # if bottom detection is better, replace top = bottom
            bottom = round(x2[-1]) # if top detection is better, replace bottom = top

            # for i in range(len(x1)+len(x2)):
            #     if i < len(x1):
            #         row = i
            #         frame = cv2.circle(frame, (round(x1[row]), round(Y1[row][1])), 2, (0, 255, 255), -1)
            #     else:
            #         row = i - len(x1)
            #         frame = cv2.circle(frame, (round(x2[row]), round(Y2[row][1])), 2, (0, 255, 255), -1)
            #####################################################################

            ####################  1.3 Pixel search, elimination methods, reg.  ##################
            orth_dist=np.array([0, 0, 0])
            for row in range(rangey_center[0], rangey_center[1]):
                index_max = max(range(len(image2[row, rangex_center[0]:rangex_center[1]])), key=image2[row, rangex_center[0]:rangex_center[1]].__getitem__) + rangex_center[0]
                absdist, dist = orthogonal_dist(index_max, row, top, bottom, rangey_outline)
                orth_dist = np.vstack([orth_dist, [dist, index_max, row]])
            orth_dist = np.delete(orth_dist, (0), axis=0)

            orth_dist = continuity(orth_dist, 2, 1.5) # Eliminate points by continuity
            curve_params = (d_curves, rangex_outline[0]+15, rangey_outline[0], outline_height, t_curves) # d, x0, y0, h, t
            orth_dist, path = curve_elim(orth_dist, curve_params) # Eliminate points outside of the two curves
            curves = get_curves(path, height, width, curve_params) # Only needed for plotting the curves

            for row in range(len(orth_dist)-1):
                frame = cv2.circle(frame, (int(orth_dist[row][1]), int(orth_dist[row][2])), 2, (0, 0, 255), -1) # Tracing the column in the given range

            mean = np.mean(orth_dist[:,1])
            w, Y, x = MLE(orth_dist[:,1:], 2, 0.1, rangey_center) # Least squares fit
            orth_distMLE = np.array([0, 0, 0, 0])
            for row in range(len(curves)):
                frame = cv2.circle(frame, (curves[row][1], curves[row][0]), 2, (255, 255, 255), -1) # Tracing the elimination curves
                frame = cv2.circle(frame, (curves[row][2], curves[row][0]), 2, (255, 255, 255), -1)
                if row < len(x):
                    # frame = cv2.circle(frame, (round(mean), round(Y[row][1])), 2, (255, 255, 255), -1) # Tracing the mean
                    frame = cv2.circle(frame, (round(x[row]), round(Y[row][1])), 2, (0, 255, 0), -1) # Tracing the least squares solution
                    absdist, dist = orthogonal_dist(x[row], round(Y[row][1]), top, bottom, rangey_outline)
                    orth_distMLE = np.vstack([orth_distMLE, [absdist, dist, x[row], Y[row][1]]])
            orth_distMLE = np.delete(orth_distMLE, (0), axis=0)

            center = np.where(orth_distMLE[int(len(orth_distMLE)/3):2*int(len(orth_distMLE)/3),0] == orth_distMLE[int(len(orth_distMLE)/3):2*int(len(orth_distMLE)/3),0].max())[0] +int(len(orth_distMLE)/3)
            center = find_nearest(center, center.sum()/len(center))
            coor_y = round(orth_distMLE[center, 3])
            coor_x = round(orth_distMLE[center, 2])
            #####################################################################

            ####################  1.4 Mark points,lines on the vid  ##################
            frame = cv2.line(frame, (top, rangey_outline[0]), (bottom, rangey_outline[1]), (255, 0, 0), 2)
            frame = cv2.circle(frame, (coor_x, coor_y), 3, (255, 0, 255), -1)
            frame = cv2.circle(frame, (top, rangey_outline[0]), 2, (0, 0, 255), -1)
            frame = cv2.circle(frame, (bottom, rangey_outline[1]), 2, (0, 0, 255), -1)

            tgt_size = 3
            x1, y1, x2, y2 = s_map[0][0], s_map[0][1], s_map[1][0], s_map[1][1]
            frame = cv2.rectangle(frame, (x1-tgt_size, y1-tgt_size), (x1+tgt_size, y1+tgt_size), (0,255,0), -1)
            frame = cv2.rectangle(frame, (x2-tgt_size, y2-tgt_size), (x2+tgt_size, y2+tgt_size), (0,255,0), -1)
            image2 = cv2.cvtColor(image2, cv2.COLOR_GRAY2BGR)

            cv2.imshow('Frame', frame)
            cv2.imshow('Column Border', frame[rangey_outline[0]:rangey_outline[1], rangex_outline[0]:rangex_outline[1]])
            cv2.imshow('Center Border', frame[rangey_center[0]:rangey_center[1], rangex_center[0]:rangex_center[1]])
            cv2.imshow('Filtered Frame', image2)
            
            out.write(frame)
            out2.write(image2)

            data = np.vstack([data, [str(frameNO), "{0:.3f}".format(time), str("{0:.3f}".format(orth_distMLE[center,1]*pixel_length)), "-", 
                    data[0,4], resolution, fps, filter, "("+str(coor_x)+", "+ str(coor_y)+")", "("+str(top)+", "+ str(rangey_outline[0])+")", "("+str(bottom)+", "+ str(rangey_outline[1])+")", str("{0:.3f}".format(orth_distMLE[center,0]*pixel_length))]])

            milis = int(1000/fps)
            if cv2.waitKey(milis) == ord('q'):  # Waits milis millisecond until q is pressed
                break
            #####################################################################
    else:
        break

cap.release()  # Releases webcama so other apps can use it
out.release()
out2.release()
cv2.destroyAllWindows()

"""########################################################################
   ######################## 2-Evaluate/plot ###############################
   ########################################################################"""
end_time = perf_counter()
total_processing_time = end_time - start_time
print("Time taken: {}".format(total_processing_time))
print("FPS : {}".format(frameNO/total_processing_time))

butterworth_params = (3, 100, 1.5)
plt.plot_results(data, butterworth_params)
