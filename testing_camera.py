# Python program to explain cv2.rectangle() method  
   
# importing cv2  
import cv2  
   
# path  
cam = cv2.VideoCapture(0)
_, frame = cam.read()
   
# Start coordinate, here (5, 5) 
# represents the top left corner of rectangle 
start_point = (5, 5) 
  
# Ending coordinate, here (220, 220) 
# represents the bottom right corner of rectangle 
end_point = (220, 220) 
  
# Blue color in BGR 
color = (255, 0, 0) 
  
# Line thickness of 2 px 
thickness = 2
  
# Using cv2.rectangle() method 
# Draw a rectangle with blue line borders of thickness of 2 px 
image = cv2.rectangle(frame, start_point, end_point, color, thickness) 
  
# Displaying the image  
cv2.imshow("Test window", frame)
key = cv2.waitKey(5) & 0xFF
if key == 27:
    cam.release()
    cv2.destroyAllWindows()
    break
