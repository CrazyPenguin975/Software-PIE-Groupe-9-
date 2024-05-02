import cv2
import numpy as np
from ultralytics import YOLO
from speed_scale import*
from datetime import datetime


    

# opening the file in read mode
my_file = open("coco.txt", "r")

# reading the file
data = my_file.read()

# replacing end splitting the text | when newline ('\n') is seen.
class_list = data.split("\n")
my_file.close()

# Generate random colors for class list

detection_color =(0,0,255)

# load a pretrained YOLOv8n model
model = YOLO("yolov8n.pt", "v8")


# # Vals to resize video frames | small frame optimise the run
frame_wid = 428
frame_hyt = 720
previous_time = 0
current_time = 0
previous_xcenter = 0
current_xcenter = 0
vitesse = 0
# video capture
cap = cv2.VideoCapture(r'C:\Users\Maxime\Documents\Maxime\Etudes\ENSTA\Cours\PIE\2023-2024\video\athlète.mp4')

#result = cv2.VideoWriter('athlete2.avi',  cv2.VideoWriter_fourcc('X','V','I','D'), 10, (frame_wid,frame_hyt)) 




if not cap.isOpened():
    print("Cannot open camera")
    exit()

try:
    while True:
    # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret :
            break
    
    # current_time = datetime.now()
    # # if frame is read correctly ret is True
    # if not ret:
    #     print("Can't receive frame (stream end?). Exiting ...")
    #     break

    # # resize the frame | small frame optimise the run
        frame = cv2.resize(frame, (frame_wid, frame_hyt))

    # Predict on image
        detect_params = model.predict(source=[frame], conf=0.45, save=False)
    

        boxes = detect_params[0].boxes
        max_area = 0
        biggest_box = None
    
    
        for i in range(len(detect_params[0])):
            box = boxes[i]  
            clsID = box.cls.numpy()[0]
            conf = box.conf.numpy()[0]
            bb = box.xyxy.numpy()[0]
            if (clsID == 0):
                current_area = (bb[2] - bb[0]) * (bb[3] - bb[1])  # Calculate box area
                if current_area > max_area:
                    max_area = current_area
                    biggest_box = bb
        if biggest_box is not None:
        # Draw the biggest box on the frame
            cv2.rectangle(frame,(int(biggest_box[0]), int(biggest_box[1])),(int(biggest_box[2]), int(biggest_box[3])),detection_color,3,)
            current_xcenter = center(int(biggest_box[0]), int(biggest_box[2])) 
            font = cv2.FONT_HERSHEY_SIMPLEX
            if (previous_time == 0):
               vitesse = 0;
            else:
               vitesse = speed(previous_xcenter, current_xcenter, previous_time, current_time)
               vitesse = round(vitesse,2)
        cv2.putText(frame,"epsilon : " + str(current_xcenter-(frame_wid/2)) + " pixel",(30, 30),font,0.75,(0, 0, 255),2,)
        cv2.putText(frame,"depsilon/dt : " + str(vitesse) + " pixel/s",(30, 50),font,0.75,(0, 0, 255),2,)
        previous_time = current_time
        previous_xcenter = current_xcenter
        # result.write(frame) 
        # Display the resulting frame
        display("ObjectDetection", frame)
        result.write(frame)
        

    # Terminate run when "Q" pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Arrêt du programme par l'utilisateur.")
finally :
    cap.release()
    cv2.destroyAllWindows()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
