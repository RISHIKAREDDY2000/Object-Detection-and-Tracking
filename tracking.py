import cv2
from tracker import *

#create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture(0)
# object detection from stable camera
object_dectector = cv2.createBackgroundSubtractorMOG2(history = 100,varThreshold=40)

while True:
    ret,frame = cap.read()
    height,width,_ = frame.shape
    #object detection
    mask = object_dectector.apply(frame)
    _,mask=cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 100:
            #cv2.drawContours(frame,[cnt],-1,(0,255,0),2)
            x,y,w,h = cv2.boundingRect(cnt)
            #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            #print(x,y,w,h)
            detections.append([x,y,w,h])

# object tracking
    boxes_ids = tracker.update(detections)
    #print(boxes_ids)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(frame, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    #print(detections)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask",mask)
    key = cv2.waitKey(30)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()