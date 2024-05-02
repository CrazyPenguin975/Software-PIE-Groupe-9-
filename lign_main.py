#%% import 
import cv2 
import numpy as np
import time
import math
from functions import*
#%%
cap = cv2.VideoCapture(r'C:\Users\Maxime\Documents\Maxime\Etudes\ENSTA\Cours\PIE\2023-2024\video\ligne_courbe.mp4')

error = 7
prev_error = 0
sum_error = 0

kp = 2
kd = 0
ki = 0
dt = 0.1

width = 640

height = 720

new_size=(width,height)
x_point_ahead=0

# init_servo(servo,11)

# result = cv2.VideoWriter('ligne_courbe_resize2.avi',  cv2.VideoWriter_fourcc('X','V','I','D'), 30, new_size) 

if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la vidéo.")

try:
    while True :
        ret, frame = cap.read()
        if not ret :
            break
        # frame = cv2.imread('C:/Users/Maxime/Documents/Maxime/Etudes/ENSTA/Cours/PIE/2023-2024/Codes suivi ligne V1/ligne_courbe.mp4')
        
        # On resize l'image, à revoir 
        
        # Utiliser la fonction cv2.resize() pour redimensionner l'image
        frame = cv2.resize(frame, new_size)
        
        p_frame, biggest_contour = process_frame(frame, height, width)
        
        x_point_ahead, y_point_ahead = point_ahead_2(p_frame, int(0.35*height), [0,255,0], x_point_ahead)
        
        print(x_point_ahead, y_point_ahead)
        
        circle__point(p_frame, x_point_ahead, y_point_ahead)
        
        error = lateral_error(x_point_ahead,width)
        
        steering_angle, sum_error, prev_error = PID_controller(sum_error, prev_error, error, dt, kd, ki, kp)
        
        steering_angle += 7
        
        # steer(servo, steering_angle)
        
        
        print(steering_angle)
        
        steering_angle = 0
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        bottom_center = (width // 2, height)
        cv2.line(p_frame, bottom_center, (x_point_ahead, y_point_ahead), (255,255, 0), thickness=2)
        draw_dashed_line(p_frame, bottom_center, (width // 2, y_point_ahead), (255, 255, 0), thickness=2)
        cv2.line(p_frame, (width // 2, y_point_ahead), (x_point_ahead, y_point_ahead), (255,0,255), thickness=2)

        #angle = calculate_angle(bottom_center, (x_point_ahead, y_point_ahead))
        angle = calculate_angle((x_point_ahead, y_point_ahead), (bottom_center))

        angle_text = f"angle : {angle:.2f} degres"

        # Draw the angle using an arc
        # Determine the angle for the arc
        start_angle = 270  # Starting from the top (vertical)
        end_angle = 270 + angle if angle >= 0 else 270 - angle  # Determine end angle based on calculated angle

        # Draw the arc to represent the angle

        # Display the angle on the image
        cv2.putText(p_frame, angle_text, (30, 70), font, 1, (255, 255, 0), 2)
        
        cv2.putText(p_frame,"epsilon : " + str(error) + " pixels",(30, 30),font,1,(255, 0, 255),2,)
        
        cv2.putText(p_frame,"point de mire",(30, 110),font,1,(0, 0, 255),2,)
        
        # result.write(p_frame) 
    
        display('', p_frame)
        
        # result.write(frame) 
    
        display('', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Arrêt du programme par l'utilisateur.")
finally :
    cap.release()
    cv2.destroyAllWindows()
   
