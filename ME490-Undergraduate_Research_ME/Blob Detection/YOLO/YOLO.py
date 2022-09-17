import cv2
import numpy as np
from time import perf_counter

np.set_printoptions(threshold=np.inf, linewidth = 200) # To print more columns in the terminal

cap = cv2.VideoCapture("Recordings\DataSet2 PS 10um 20um Cell/1609 frames/1609.mp4")
width = int(cap.get(3)) # Gets width of capture (there are total of 17 properties)
height = int(cap.get(4))
whT = 608 # check this value from the config file, it might be 608 for yolov4
confidence_thresh = 0.15
nmsThreshold = 0.05 # High threshold -> less boxes

with open('YOLO\custom_names.txt', 'rt') as classFile:
    classNames = classFile.read().rstrip('\n').split('\n')

### Load the model here (use the custom ones)
modelConfig = 'YOLO\yolov4_dark.cfg'
modelWeights = 'YOLO\yolov4_dark_final.weights'

net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObjects(outputs):
    hT, wT = height, width
    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confidence_thresh:
                w, h = int(det[2]*wT), int(det[3]*hT)
                x,y = int(det[0]*wT - w/2), int(det[1]*hT - h/2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    indices = cv2.dnn.NMSBoxes(bbox, confs, confidence_thresh, nmsThreshold)
    return bbox, classIds, confs, indices

start_time = perf_counter()
frame_count = 0
while True:
    ret, frame = cap.read()

    blob = cv2.dnn.blobFromImage(frame, 1/255, (whT, whT), [0, 0, 0])
    net.setInput(blob)

    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    
    bbox, classIds, confs, indices = findObjects(outputs)

    for i, in indices:
        i = int(i)
        box = bbox[i]
        cv2.rectangle(frame, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), 255, 1)
        cv2.putText(frame, str(classNames[classIds[i]])+": "+str(confs[i]*100)[0:4], (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

    frame_count +=1
    FPS = frame_count/(perf_counter()-start_time)
    cv2.putText(frame, "FPS: "+str(FPS)[0:4], (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Matches", frame)

    key = cv2.waitKey(30) # Press ESC to end
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

