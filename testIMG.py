import cv2
from cvzone.ColorModule import ColorFinder
from PIL import Image
import numpy as np

brown_limits = {
    "hmin": 6,
    "smin": 57,
    "vmin": 57,
    "hmax": 18,
    "smax": 255,
    "vmax": 255,
}

color_finder = ColorFinder(False)
# path 
image_path = "data\im1.png"
frame = cv2.imread(image_path)
framesize = cv2.resize(frame, (480, 360))
frame, mask = color_finder.update(framesize, brown_limits)
frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
mask_non_black = frame_hsv[:, :, 2] > 50 

mask_ = Image.fromarray(mask)

bbox = mask_.getbbox()

if bbox is not None:
    x1, y1, x2, y2 = bbox
    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
   
    region_non_black = frame_hsv[y1:y2, x1:x2, :][mask_non_black[y1:y2, x1:x2]]

    if region_non_black.size > 0: 
        hue_avg = np.mean(region_non_black[:, 0])
        print("Hue average (not black):", hue_avg)
   
    if hue_avg <= 15:
        cv2.putText(frame, "dead cocoon", (10 , 350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    else:
        cv2.putText(frame, "yellow cocoon", (10, 305 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

cv2.imshow('Real Time', frame)
cv2.imshow('frame', framesize)
cv2.waitKey(0)
cv2.destroyAllWindows()
