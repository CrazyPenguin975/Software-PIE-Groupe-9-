import cv2
import numpy as np
# import RPi.GPIO as GPIO
import time
import math
#%% Affiche la frame
def display(title, frame):
    cv2.imshow(title, frame)
    cv2.waitKey(1)  
#%% Pocess la frame pour qu'elle puisse être exploitée
def process_frame(frame,height,width):
    
    rec = np.zeros((height, width), dtype=np.uint8)
    x_1 = width//4
    x_2 = 3*width//4
    cv2.rectangle(rec, (x_1, int(0.1*height)), (x_2,height), 255, thickness=-1)
    mask_1 = cv2.bitwise_and(frame, frame, mask=rec)
    
    blur = cv2.GaussianBlur(mask_1,(11,11),0)
    
    #low_b = np.uint8([130,130,0])
    low_b = np.uint8([145,145,20]) #valeur inférieure de la plage de couleurs en BGR.
    high_b = np.uint8([255,255,255]) #valeur supérieure de la plage de couleurs en BGR.

    mask_2 = cv2.inRange(blur, low_b, high_b)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    
    dilated = cv2.dilate(mask_2, kernel)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    biggest_contour = max(contours, key=cv2.contourArea)
           
    cv2.drawContours(frame, [biggest_contour], -1, (0, 255, 0), 3)
    
    return(frame, biggest_contour)
#%% Définit la distance à laquelle il faut regarder pour le PID controller ; dépend de la vitesse longitudniale de la voiture
def look_ahead_distance(velocity, Kdd):
    return(velocity*Kdd)
#%% Repère le point 
def point_ahead(biggest_contour, look_ahead_distance, margin):
    x_mean = []
    for point in biggest_contour:
        if look_ahead_distance - margin <= point[0][1] <= look_ahead_distance + margin:
            x_mean.append(point[0][0])
    x_point_ahead = int(sum(x_mean)/len(x_mean))
    y_point_ahead = int(look_ahead_distance)
    return(x_point_ahead, y_point_ahead)
#%%
def point_ahead_2(frame, look_ahead_distance, color,x_point_ahead):
    
    coord = np.column_stack(np.where((frame[look_ahead_distance, :, :] == color).all(axis=1)))
    if len(coord)!=0 :
        x_point_ahead = int(sum(coord)/len(coord))
    y_point_ahead = int(look_ahead_distance)

    return (x_point_ahead, y_point_ahead)
#%% Encercle le  point sur l'image
def circle__point(frame, x, y):
    cv2.circle(frame, (x,y), 5, (0,0,255), -1) 
#%%
def lateral_error(x_point_ahead,width):
    return(width//2-x_point_ahead)
#%%
def PID_controller(sum_error, prev_error, error, dt,kd, ki, kp):
    sum_error += error*dt   
    angle = kp*error + kd*(error-prev_error)/dt + ki*sum_error
    prev_error = error
    return(angle, sum_error, prev_error)
# #%% GPIO
# def init_servo(name, port):
#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setup(11,GPIO.OUT)
#     name = GPIO.PWM(11,50)
#     name.start(7)
#     time.sleep(0.1)

# def steer(name, steering_angle):
#     name.ChangeDutyCycle(steering_angle)
#     time.sleep(0.1)
#%%
def calculate_angle(p1, p2):
    """Calculate the angle from vertical."""
    angle_radians = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    angle_degrees = np.degrees(angle_radians)
    if angle_degrees < 0:
        angle_degrees += 360
    return 90 - angle_degrees if angle_degrees <= 180 else 270 - angle_degrees
#%%
def draw_dashed_line(img, pt1, pt2, color, thickness=1, dash_length=20):
    """ Draw a dashed line in img from pt1 to pt2 with given color and thickness. """
    dist = ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5
    dashes = int(dist / dash_length)  # number of whole dashes
    for i in range(dashes):
        start = (int(pt1[0] + (pt2[0] - pt1[0]) * i / dashes), int(pt1[1] + (pt2[1] - pt1[1]) * i / dashes))
        end = (int(pt1[0] + (pt2[0] - pt1[0]) * (i + 0.5) / dashes), int(pt1[1] + (pt2[1] - pt1[1]) * (i + 0.5) / dashes))
        cv2.line(img, start, end, color, thickness)