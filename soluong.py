import cv2
from cvzone.ColorModule import ColorFinder  
import time
from PIL import Image
import threading
import numpy as np

class VideoCapture:
    def __init__(self, index):
        self.cap = cv2.VideoCapture(index)
        self.cap.set(3, 640)
        self.cap.set(4, 480)
        self.ret, self.frame = self.cap.read()
        threading.Thread(target=self.update, args=()).start()

    def update(self):
        while True:
            self.ret, self.frame = self.cap.read()

    def read(self):
        return self.ret, self.frame

    def release(self):
        self.cap.release()
# edit color 
brown_limits = {
    "hmin": 11,  
    "hmax": 26,  
    "smin": 61,  
    "smax": 255,  
    "vmin": 61,  
    "vmax": 255,   
}

color_finder = ColorFinder(False)  

cap = VideoCapture(1)

count_vang = 0
count_phe = 0

pTime = 0
cTime = 0
frame_count = 0
fps = 0

inside = False
while True:
    ret, frame = cap.read()  
    frameresize = cv2.resize(frame, (480, 360))
    blurred = cv2.GaussianBlur(frameresize, (5, 5), 0)  
    frame, mask = color_finder.update(blurred,brown_limits)  
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  
    # area 
    cv2.rectangle(frame, (2, 300), (475, 120), (0, 0, 255), 3)
    cv2.rectangle(frameresize, (2, 300), (475, 120), (0, 0, 255), 3)
    
    mask_non_black = frame_hsv[:, :, 2] > 50 

    mask_ = Image.fromarray(mask)

    bbox = mask_.getbbox()

    if bbox is not None:
        x1, y1, x2, y2 = bbox
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        hue_avg = np.mean(frame[y1:y2, x1:x2, 0])
        region_non_black = frame_hsv[y1:y2, x1:x2, :][mask_non_black[y1:y2, x1:x2]]
        
        if region_non_black.size > 0:  
            hue_avg = np.mean(region_non_black[:, 0])
            
        if 2 <= x1 and x1 <= 475 and 120 <= y1 and y1 <= 260:  # check object go out rectangle
            inside = True
        else:
            if inside:  
                if hue_avg <= 15:
                    print("dead cocoon:",hue_avg)
                    count_phe += 1
                else:
                    print("yellow cocoon",hue_avg)
                    count_vang += 1
                inside = False 

    frame_count += 1
    if frame_count % 10 == 0:  
        cTime = time.time()
        fps = 10 / (cTime - pTime)
        pTime = cTime
    
    cv2.putText(frame,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
    cv2.putText(frame, f"count died: {count_phe}", (10, 350), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.putText(frame, f"Count yellow: {count_vang}", (280, 350), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    cv2.imshow('RealTime', frame)
    cv2.imshow('time',frameresize)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
