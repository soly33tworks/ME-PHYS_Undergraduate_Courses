import cv2
import numpy as np
import glob
import keyboard as kb
from time import sleep

def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True

def get_time(L, R, percentage):
    if (len(L) > 2) or (len(R) > 2):
        print("L or R > 2")
        return False
    else:
        tL = 0
        for i, key in enumerate(L):
            if i == 0:
                event_no_L = L[key][0]
            tL += L[key][1]/len(L)
            if event_no_L != L[key][0]:
                print("Selections belonging to different events on L")
                return False
        
        tR = 0
        for i, key in enumerate(R):
            if i == 0:
                event_no_R = R[key][0]
            tR += R[key][1]/len(R)
            if event_no_R != R[key][0]:
                print("Selections belonging to different events on R")
                return False
        
        if event_no_L == event_no_R:
            t = (1-percentage)*tR + percentage*tL
            return t
        else:
            print("L and R belonging to different events")
            return False

def frame_label(i, L, R): # Whether frame is selected as left or right
    text = ""
    if (i in L) and (i in R):
        text = "C"
    elif (i in L) and (i not in R):
        text = "L"+str(len(L))
    elif (i not in L) and (i in R):
        text = "R"+str(len(R))
    return text

def save(results, title):
    print(results)
    with open(title, 'w') as f:
        for result in results:
            for element in result:
                f.write(str(element)+", ")
            f.write('\n')

recording = "1410"
savedir = "Recordings\DataSet5_2022/"+recording+"/saved_frames/"
savedir2 = "Recordings\DataSet5_2022/"+recording+"/saved_frames_final/"
imdir = "Recordings\DataSet5_2022/"+recording+"/frames/"
ext = ['png', 'jpg', 'gif']    # Add image formats here

files = []
[files.extend(glob.glob(imdir + '*.' + e)) for e in ext]

files.sort(key=lambda i:float(i.split('_')[2][:-4]))

names = [file.split('\\')[2] for file in files]

stamps = []
for file in files:
    name = file.split('\\')[2]
    event, time = int(name.split('_')[0]), float(name.split('_')[1][:-4])
    stamp = (event, time)
    stamps.append(stamp)

images = [cv2.imread(file) for file in files]

scale = 98/50
sensing = [147, 230, 148, 340] # x1,y1 - x2,y2
corner_a, x_range_a, y_range_a = [500, 95], 45, 45 # aim box parameters
corner_d, x_range_d, y_range_d = [500, 125], 178, 2 # distance box parameters
colors = [(0,255,0), (0,0,255)]
selection = 1 # 1 for aim 0 for distance
sensitivity = 1 
mode = 0 # 0 For position and 1 for size
t = 0
validity = True # False For invalid and True for valid
L, R = {}, {} # [Frame index (i): event id (must be same), vid_time of LEFT and RIGHT points]

#results = []
results2 = [] # big selections
i = 0
print("Event " + str(stamps[i][0]) + 3*" "+" t = "+ str(stamps[i][1]))

try:
    while True:
        frame = images[i][530: 1080, 385: , :] # from top left corner: row range, column range, colors (rgb)
        aim = [(int(corner_a[0]), int(corner_a[0]+x_range_a)), (int(corner_a[1]), int(corner_a[1]+y_range_a))] # x1,x2 - y1,y2
        dist = [(int(corner_d[0]), int(corner_d[0]+x_range_d)), (int(corner_d[1]), int(corner_d[1]+y_range_d))] # x1,x2 - y1,y2
        frame2 = cv2.rectangle(frame.copy(),(aim[0][0],aim[1][0]),(aim[0][1],aim[1][1]),colors[0],1) # Aim
        frame2 = cv2.rectangle(frame2,(dist[0][0],dist[1][0]),(dist[0][1],dist[1][1]),colors[1],1) # Distance box
        x1,y1, x2,y2 = sensing
        frame2 = cv2.rectangle(frame2,(x1, y1),(x2, y2),(255,0,255),1) # Center line
        percentage = 1-(0.5*(sensing[2]+sensing[0])-corner_d[0])/x_range_d
        w = x_range_a/scale
        h = y_range_a/scale
        d = round((w+h)/2,2)
        cv2.putText(frame2, "Event: "+str(stamps[i][0])+ 3*" "+"t = "+str(str(stamps[i][1])), (75,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame2, "d = "+str(d), (75,485), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame2, frame_label(i, L, R), (250,185), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Image", frame2)

        k = cv2.waitKey(60)
        if kb.is_pressed('esc'):
            break
        
        elif kb.is_pressed('right'):
            sleep(0.15)
            if i < len(images)-1:
                i += 1
            #print("Event " + str(stamps[i][0]) + " event time = "+ str(stamps[i][1]) + 3*" "+" t = ", t, " Percentage on right: ", percentage*100)

        elif kb.is_pressed('left'):
            sleep(0.15)
            if i > 0:
                i -= 1
            #print("Event " + str(stamps[i][0]) + " event time = "+ str(stamps[i][1]) + 3*" "+" t = ", t, " Percentage on right: ", percentage*100)
        
        elif kb.is_pressed('z'):
            sleep(0.15)
            sensitivity *= 2
            print("Sensitivity: ", sensitivity)
        elif kb.is_pressed('x'):
            sleep(0.15)
            if sensitivity > 1:
                sensitivity = round(sensitivity/2)
                print("Sensitivity: ", sensitivity)
        
        elif kb.is_pressed('w'):
            if selection:
                if mode:
                    y_range_a += sensitivity
                else:
                    corner_a[1] -= sensitivity
            else:
                if not mode:
                    corner_d[1] -= sensitivity
            #print("AIM C= ", corner_a, " xr= ", x_range_a, " yr=", y_range_a, 7*" ", "DIST C= ", corner_d, " xr= ", x_range_d, " yr=", y_range_d)            
        
        elif kb.is_pressed('s'):
            if selection:
                if mode:
                    y_range_a -= sensitivity
                else:
                    corner_a[1] += sensitivity
            else:
                if not mode:
                    corner_d[1] += sensitivity
            #print("AIM C= ", corner_a, " xr= ", x_range_a, " yr=", y_range_a, 7*" ", "DIST C= ", corner_d, " xr= ", x_range_d, " yr=", y_range_d)    

        elif kb.is_pressed('a'):
            if selection:
                if mode:
                    x_range_a -= sensitivity
                else:
                    corner_a[0] -= sensitivity
            
            else:
                if mode:
                    x_range_d -= sensitivity
                else:
                    corner_d[0] -= sensitivity

            #print("AIM C= ", corner_a, " xr= ", x_range_a, " yr=", y_range_a, 7*" ", "DIST C= ", corner_d, " xr= ", x_range_d, " yr=", y_range_d)    

        elif kb.is_pressed('d'):
            if selection:
                if mode:
                    x_range_a += sensitivity
                else:
                    corner_a[0] += sensitivity
            else:
                if mode:
                    x_range_d += sensitivity
                else:
                    corner_d[0] += sensitivity

            #print("AIM C= ", corner_a, " xr= ", x_range_a, " yr=", y_range_a, 7*" ", "DIST C= ", corner_d, " xr= ", x_range_d, " yr=", y_range_d)    

        elif kb.is_pressed('m'):
            sleep(0.15)
            mode = not mode
            #print("Mode: ", mode)

        elif kb.is_pressed('v'):
            sleep(0.15)
            validity = not validity
            print("Validity: ", validity)

        # elif kb.is_pressed('e'):
        #     sleep(0.25)
        #     if (len(L)>0) and (len(R)>0):
        #         if (get_time(L, R, percentage)): # Check if false is being returned
        #             t = get_time(L, R, percentage)
        #             print("Entry: ", stamps[i][0], t, w, h, np.pi*(w/2)*(h/2), validity)
        #             results.append([stamps[i][0], t, w, h, np.pi*(w/2)*(h/2), validity])
        #             title = savedir+str(stamps[i][0])+"_"+str(stamps[i][1])+".png"
        #             cv2.imwrite(title, frame2)
        
        elif kb.is_pressed('f'):
            sleep(0.25)
            if (len(L)>0) and (len(R)>0):
                if (get_time(L, R, percentage)): # Check if false is being returned
                    t = get_time(L, R, percentage)
                    print("Entry: ", stamps[i][0], t, w, h, np.pi*(w/2)*(h/2), validity)
                    results2.append([stamps[i][0], t, w, h, np.pi*(w/2)*(h/2), validity])
                    title = savedir2+str(stamps[i][0])+"_"+str(stamps[i][1])+".png"
                    cv2.imwrite(title, frame2)

        elif kb.is_pressed('c'):
            sleep(0.15)
            selection = not selection
            colors = colors[::-1]
        
        elif kb.is_pressed('o'):
            sleep(0.35)
            if (len(L) < 3) and (i not in L):
                L[i]=[stamps[i][0], stamps[i][1]]
            else:
                print("Atleast 2 LEFT frames already selected or this frame is already selected as LEFT")

        elif kb.is_pressed('p'):
            sleep(0.35)
            if (len(R) < 3) and (i not in R):
                R[i]=[stamps[i][0], stamps[i][1]]
            else:
                print("Atleast 2 RIGHT frames already selected or this frame is already selected as RIGHT")

        elif kb.is_pressed('r'):
            sleep(0.35)
            L, R = {}, {} # [Frame index (i): event id (must be same), vid_time of LEFT and RIGHT points]

except:
    print("ENDED \n")
    #save(results, savedir+"data.txt")
    save(results2, savedir2+"data_final.txt")


print("ENDED \n")
#save(results, savedir+"data.txt")
save(results2, savedir2+"data_final.txt")
