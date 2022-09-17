import numpy as np
import cv2
import pandas as pd
from time import sleep, perf_counter

from skimage import util
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops, regionprops_table
from skimage.morphology import closing, square
from skimage.color import label2rgb

import Plot_results as plt
import Event
from Plates import *
import Tracker

from decord import VideoReader
from decord import cpu, gpu

np.set_printoptions(threshold=np.inf, linewidth = 200)

cap = cv2.VideoCapture('Recordings\DataSet3 SPM-PS 10um/1629/1629.mp4')
width = int(cap.get(3)) # Gets width of capture (there are total of 17 properties)
height = int(cap.get(4))
fps = int(cap.get(5))
cap.release()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('Extracted Data/Labeled.avi', fourcc, fps, (width, height))
out2 = cv2.VideoWriter('Extracted Data/Mask.avi', fourcc, fps, (width, height))

plate1 = [[721,172], [721, 400], [760, 400], [760, 172], [750, 161], [741, 158], [731, 161]]
plate2 = [[794,140], [795, 342], [802, 355], [815, 360], [824, 358], [835, 342], [835, 140]]    

plate_regions = np.array([plate1, plate2])
channel = [10, 1200, 140, 400, 721, 835] # Channel region x1,x2,y1,y2 and active region x1,x2
min_area, max_area = (15, 220)
mask_plates = create_masks(plate_regions, height, width)
bground_thresh, plate_thresh = 195, 80

tracker = Tracker.EuclideanDistTracker(distance_tol=60, memory_length=8)
events = []
font = cv2.FONT_HERSHEY_SIMPLEX

vr = VideoReader('Recordings\DataSet3 SPM-PS 10um/1629/1629.mp4', ctx=cpu(0))  # can set to cpu or gpu .. ctx=gpu(0)
count = 0
start_time = perf_counter()
for index in range(0, len(vr)):  # lets loop through the frames until the end
    second = count/fps
    frame = cv2.cvtColor(vr[index].asnumpy(), cv2.COLOR_RGB2BGR)
    count += 1

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = util.invert(gray)

    mask = (gray>bground_thresh) | (((gray >plate_thresh)&mask_plates))
    masked_frame = gray*mask

    thresh = threshold_otsu(masked_frame)
    bw = closing(masked_frame > thresh, square(3))

    cleared = clear_border(bw) # remove artifacts connected to image border
    label_image = label(cleared)
    # to make the background transparent, pass the value of `bg_label`, and leave `bg_color` as `None` and `kind` as `overlay`

    image_label_overlay = label2rgb(label_image, image=frame, bg_label=0)

    props = regionprops_table(label_image, properties=('centroid','orientation','axis_major_length','axis_minor_length'))
    particles = pd.DataFrame(props).to_numpy()

    particle_list = np.array([0, 0, 0, 0, 0, 0, 0]) # x, y, theta, a, b, area, pi*a*b
    detected = []
    for region in regionprops(label_image):
        minr, minc, maxr, maxc = region.bbox
        a, b, theta = region.axis_minor_length*0.75, region.axis_major_length*0.75, region.orientation
        x, y = round(minc+(maxc - minc)/2), round(minr+(maxr - minr)/2)

        if (region.area >= min_area) & (region.area <= max_area) & ((channel[0]<x<channel[1])&(channel[2]<y<channel[3])):
            # draw ellipse around segmented particles
            image_label_overlay = cv2.ellipse(image_label_overlay, (x,y), 
                            (round(a), round(b)), theta, 0, 360, (0, 0, 255), 2)
            frame = cv2.ellipse(frame, (x,y), 
                            (round(a), round(b)), theta, 0, 360, (0, 0, 255), 2)
            particle_list=np.vstack([particle_list, [x, y, theta, a, b, region.area, np.pi*a*b]])
            detected.append([x, y, region.area])
    particle_list = np.delete(particle_list, (0), axis=0)
    image_label_overlay = draw_plates(image_label_overlay, [plate1, plate2])
    frame = draw_plates(frame, [plate1, plate2])
    #image_label_overlay = cv2.line(image_label_overlay, (778,100), (778,300), (255, 255, 0), 1)

    particle_ids, areas = tracker.update(detected)
    for particle_id in particle_ids:
        x, y, area, id = particle_id
        cv2.putText(frame, str(id), (x, y-15), font, 1, (0, 0, 255), 2)

    try:
        valid_particles = (channel[4] < particle_list[:,0]) & (particle_list[:,0] < channel[5])
        valid_particles = particle_list*(np.tile(valid_particles, (7,1)).T)
        valid_particles = valid_particles[~np.all(valid_particles == 0, axis=1)]
    except:
        valid_particles = np.array([])
        #print(particle_list)

    population = len(valid_particles)
    if len(events) == 0:
        if population == 1:
            x, y = valid_particles[0,0], valid_particles[0,1]
            index = np.where(particle_ids[:,0]==x)
            id = particle_ids[index,3]
            surface_area = areas[id.item(0)]
            events.append(Event.Event(count, [y, x], [channel[4], channel[5]], surface_area, tolerances=[4, 45]))
            frame = cv2.putText(frame, 'Channel Status: Active', (25, height - 8), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)

        elif population == 0:
            frame = cv2.putText(frame, 'Channel Status: Inactive', (25, height - 8), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
        
        elif population > 1:
            frame = cv2.putText(frame, 'Channel Status: Invalid', (25, height - 8), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    
    else:
        if population == 1:
            x, y = valid_particles[0,0], valid_particles[0,1]
            frame = cv2.putText(frame, 'Channel Status: Active', (25, height - 8), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)

            if events[-1].isdone:
                index = np.where(particle_ids[:,0]==x)
                id = particle_ids[index,3]
                surface_area = areas[id.item(0)]
                events.append(Event.Event(count, [y, x], [channel[4], channel[5]], surface_area, tolerances=[4, 45]))
            else:
                events[-1].update(count, 1, [y, x])

        elif population == 0:
            if events[-1].isdone:
                frame = cv2.putText(frame, 'Channel Status: Inactive', (25, height - 8), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                events[-1].update(count, 0, [])
                frame = cv2.putText(frame, 'Channel Status: Active', (25, height - 8), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)

        elif population > 1:
            if events[-1].isdone:
                frame = cv2.putText(frame, 'Channel Status: Invalid', (25, height - 8), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                events[-1].update(count, population, [])
                frame = cv2.putText(frame, 'Channel Status: Active', (25, height - 8), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    
    valid_events = []
    for event in events:
        if (event.isdone) & (event.isvalid):
            valid_events.append(event)

    frame = cv2.putText(frame, f"Total Events: {len(valid_events)}." , (25, height - 35), font, 0.6, (0, 0, 255), 2, cv2.LINE_AA)
    frame = cv2.rectangle(frame,(0,191),(30,296),(0,255,0),1)

    " DEBUGGING PART "
    cv2.imshow('OG', frame)
    cv2.imshow('gray', gray[channel[2]:channel[3], channel[0]:channel[1]])
    cv2.imshow('channel masked', masked_frame[channel[2]:channel[3], channel[0]:channel[1]])
    cv2.imshow('Labeled', image_label_overlay[channel[2]:channel[3], channel[0]:channel[1]])

    # if count == 3:
    #     print(regionprops(label_image)[0])
    #     print(pd.DataFrame(props))
    #     print(label_image.shape)
    #     print(particle_list)
    #     print(masked_frame[140:400, 920:963])
    #     print(gray[140:400, 719:763])
    #     sleep(3)
    
    if cv2.waitKey(1) == ord('q'):  # Waits milis millisecond until q is pressed
        break

    masked_frame = cv2.cvtColor(masked_frame, cv2.COLOR_GRAY2BGR)
    out.write(frame)
    out2.write(masked_frame)

    if second % 10 == 0:
        print(second, count)

out.release()
out2.release()
cv2.destroyAllWindows()

end_time = perf_counter()
total_processing_time = end_time - start_time
print("Time taken: {}".format(total_processing_time))
print("FPS : {}".format(count/total_processing_time))

scale = 105/100 # Pixel/Micrometer
data = np.zeros((1,5)) # Frame, t, velocity, area, (y_avg, x_avg)
for event in valid_events:
    data = np.vstack([data, [event.compute(fps, scale)]])
data = np.delete(data, (0), axis=0)

events_E1658 = []

plt.plot_results(data, events_E1658, channel[2:4], scale)
