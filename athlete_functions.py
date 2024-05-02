import cv2

# display frame
def display(title, frame):
    cv2.imshow(title, frame)

# athlete speed
def speed(previous_xcenter, current_xcenter, previous_time, current_time):
    delta_t = float((current_time - previous_time).total_seconds())
    delta_x = (current_xcenter - previous_xcenter)
    # if (int(abs(delta_x)) > 0):
    #     if (delta_x < 0):
    #         delta_x += 10
    #     else:
    #         delta_x -= 10
    # else:
    #     delta_x = 0
        
    return delta_x / delta_t

def center(minx, maxx):
    return (minx + maxx) / 2
