import cv2
import numpy as np

net = cv2.dnn.readNet("yolov4-tiny.weights","yolov4-tiny.cfg")
classes = []
with open("classes.txt","r") as f:
    classes = f.read().splitlines()

cap = cv2.VideoCapture('los_angeles.mp4')
#img = cv2.imread("image.jpg")
while True:
    _,img = cap.read()
    height ,width , _ = img.shape

    blob = cv2.dnn.blobFromImage(img,1/255,(416,416),(0,0,0),swapRB=True,crop = False)
    net.setInput(blob)
    output_layer_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layer_names)

    class_ids = []
    confidences = []
    boxes = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # rectangular coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    #print(len(boxes))

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size=(len(boxes), 3))

    for i in range(len(boxes)):
        if i in indexes:
    #for i in indexes.flatten():
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = str(round(confidences[i], 2))
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label+" "+confidence, (x, y + 20), font, 1, (255,255,255), 1)

    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key==27:
        break
cap.release()
cv2.destroyAllWindows()