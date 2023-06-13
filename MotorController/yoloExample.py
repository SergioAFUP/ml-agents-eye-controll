import cv2
import numpy as np


# Color function according to confidence
def colorSelector(confidence):
    if confidence > 0.75:
        return (0, 255, 0)
    elif 0.75 >= confidence > 0.5:
        return (255, 255, 0)
    else:
        return (0, 0, 255)


# Load Yolo
net = cv2.dnn.readNet("./yolov3.weights", "./yolov3.cfg")
layer_names = net.getLayerNames()

output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Load classes from .names file
with open("./coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Load camera with cv2
cap = cv2.VideoCapture("rtsp://admin:Chame1eon@192.168.101.21")

while True:
    # Read image and resize it to reduce time
    ret, frame = cap.read()
    frame = cv2.resize(frame, (480, 270))

    height, width, channels = frame.shape

    # Detect objects
    blob = cv2.dnn.blobFromImage(
        frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False
    )
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # apply non-max suppression
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw final bounding boxes with color selection
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            classString = str(classes[class_ids[i]])
            confidence = float(confidences[i])
            label = f"{classString} %{confidence * 100}"
            print(classString)
            print(f"\tpt1: x:{x}, y:{y}")
            print(f"\tpt2: x:{x + w}, y:{y + h}")
            print(f"\tcenter: x:{x + (w / 2)}, y:{y + (h / 2)}")
            cv2.rectangle(frame, (x, y), (x + w, y + h), colorSelector(confidence), 2)
            cv2.putText(
                frame,
                label,
                (x, y + 30),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                colorSelector(confidence),
                3,
            )

    # Display cv2 window to view camera processing
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
