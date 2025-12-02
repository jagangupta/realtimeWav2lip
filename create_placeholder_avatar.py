import cv2
import numpy as np
import os

def create_avatar():
    # Create a blank white image
    img = np.ones((512, 512, 3), dtype=np.uint8) * 255
    
    # Draw a face (yellow circle)
    cv2.circle(img, (256, 256), 200, (0, 255, 255), -1)
    
    # Draw eyes (black circles)
    cv2.circle(img, (180, 200), 30, (0, 0, 0), -1)
    cv2.circle(img, (332, 200), 30, (0, 0, 0), -1)
    
    # Draw mouth (black line/ellipse)
    cv2.ellipse(img, (256, 350), (100, 50), 0, 0, 180, (0, 0, 0), 10)
    
    # Save
    os.makedirs('jagan_demo/static/images', exist_ok=True)
    cv2.imwrite('jagan_demo/static/images/avatar.jpg', img)
    print("Avatar created at jagan_demo/static/images/avatar.jpg")

if __name__ == "__main__":
    create_avatar()
