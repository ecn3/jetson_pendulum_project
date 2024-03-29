import cv2 as cv
import math
import numpy as np
 
 
class Target:
    def __init__(self):
        self.capture = cv.VideoCapture("/dev/video1")
        cv.namedWindow("Target", 1)
        cv.namedWindow("Threshold1",1)
        cv.namedWindow("Threshold2",1)
        cv.namedWindow("hsv",1)
        
        
     
    def run(self):
        #initiate font
        font = cv.FONT_HERSHEY_SIMPLEX
        
        frame_height = int(self.capture.get(cv.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(self.capture.get(cv.CAP_PROP_FRAME_WIDTH))
        
        #instantiate images
        #hsv_img=cv.CreateImage(cv.GetSize(cv.QueryFrame(self.capture)),8,3)
        hsv_img = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
        threshold_img1 = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        threshold_img1a = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        threshold_img2 = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
        i=0
        
        fourcc = cv.VideoWriter_fourcc('M','J','P','G')
        writer=cv.VideoWriter("angle_tracking.avi",fourcc,30,(frame_height, frame_width),1)
 
        while True:
            #capture the image from the cam
            ret, img=self.capture.read()
 
            #convert the image to HSV
            hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        
 
            #threshold the image to isolate two colors
            cv.inRange(hsv_img,(165,145,100),(250,210,160),threshold_img1) #red
            cv.inRange(hsv_img,(0,145,100),(10,210,160),threshold_img1a)   #red again
            cv.add(threshold_img1,threshold_img1a,threshold_img1)          #this is combining the two limits for red
            cv.inRange(hsv_img,(105,180,40),(120,260,100),threshold_img2)  #blue
 
 
            #determine the moments of the two objects
            #threshold_img1=cv.getMat(threshold_img1)
            #threshold_img2=cv.getMat(threshold_img2)
            moments1=cv.moments(threshold_img1)
            moments2=cv.moments(threshold_img2)
            area1 = moments1['m00'] 
            area2 = moments2['m00'] 
             
            #initialize x and y
            x1,y1,x2,y2=(1,2,3,4)
            coord_list=[x1,y1,x2,y2]
            for x in coord_list:
                x=0
             
            #there can be noise in the video so ignore objects with small areas
            if (area1 >200000):
                #x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
                x1=int(moments1['m10']/area1)
                y1=int(moments1['m01']/area1)
 
                #draw circle
                cv.circle(img,(x1,y1),2,(0,255,0),20)
 
                #write x and y position
                cv.putText(img,str(x1)+","+str(y1),(x1,y1+20),font, 1,(255,255,255)) #Draw the text
 
            if (area2 >100000):
                #x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
                x2=int(moments1['m10']/area2)
                y2=int(moments1['m01']/area2)
 
                #draw circle
                cv.circle(img,(x2,y2),2,(0,255,0),20)
 
                cv.putText(img,str(x2)+","+str(y2),(x2,y2+20),font, 1,(255,255,255)) #Draw the text
                cv.line(img,(x1,y1),(x2,y2),(0,255,0),4,cv.LINE_AA)
                #draw line and angle
                cv.line(img,(x1,y1),(frame_height, frame_width, y1),(100,100,100,100),4,cv.LINE_AA)
            x1=float(x1)
            y1=float(y1)
            x2=float(x2)
            y2=float(y2)
            angle = int(math.atan((y1-y2)/(x2-x1))*180/math.pi)
            cv.putText(img,str(angle),(int(x1)+50,(int(y2)+int(y1))/2),font, 4,(255,255,255))
 
            #cv.writeFrame(writer,img)
 
          
            #display frames to users
            cv.imshow("Target",img)
            #cv.imshow("Threshold1",threshold_img1)
            #cv.imshow("Threshold2",threshold_img2)
            #cv.imshow("hsv",hsv_img)
            # Listen for ESC or ENTER key
            c = cv.waitKey(7) % 0x100
            if c == 27 or c == 10:
                break
        cv.destroyAllWindows()
             
if __name__=="__main__":
    t = Target()
    t.run()        
