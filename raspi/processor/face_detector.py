from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import cv2
import baby

first_read = True
prev_read = False
cur_read = False

class FaceDetector(object):
    def __init__(self, flip = True):
        self.vs = PiVideoStream(resolution=(800, 608)).start()
        self.flip = flip
        time.sleep(2.0)

        # opencvの顔分類器(CascadeClassifier)をインスタンス化する
        self.face_cascade = cv2.CascadeClassifier('processor/model/haarcascades/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('processor/model/haarcascades/haarcascade_eye.xml')

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame
    

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        frame = self.process_image(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def process_image(self, frame):

        global first_read
        global prev_read

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 3)

        if len(faces) == 0:
            cv2.putText(frame, "No detection", (70, 70), cv2.FONT_HERSHEY_TRIPLEX, 1, (255,0,255), 2)
            baby.eye_list = baby.eye_list[1:]
            baby.eye_list.append(2)
            # print(baby.eye_list) 

        for (x,y,w,h) in faces:
            face_rec = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            face_gray=gray[y:y+h,x:x+w]
            face_color=frame[y:y+h,x:x+w]
            eyes = self.eye_cascade.detectMultiScale(face_gray,1.1,3)
        
            for(ex,ey,ew,eh) in eyes:
                cv2.rectangle(face_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                if len(eyes) >= 2:
                    cur_read = True
                    if first_read:
                        cv2.putText(frame, "Eye's detected!", (70, 70), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 2)
                        baby.eye_list = baby.eye_list[1:]
                        baby.eye_list.append(0)
                        # print(baby.eye_list)  
                        prev_read = 1
                    else:
                        if prev_read != cur_read:
                            cv2.putText(frame, "Blink Detected", (70, 70), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 2)
                            baby.eye_list = baby.eye_list[1:]
                            baby.eye_list.append(2)
                            # print(baby.eye_list) 
                            prev_read = 1 
                        else:
                            cv2.putText(frame, "Eye's Open", (70, 70), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 255), 2)
                            baby.eye_list = baby.eye_list[1:]
                            baby.eye_list.append(0)
                            # print(baby.eye_list) 
                            prev_read = 1
                else:
                    cur_read = False
                    if first_read:
                        cv2.putText(frame, "Sleeping", (70, 70), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 255), 2)
                        baby.eye_list = baby.eye_list[1:]
                        baby.eye_list.append(1)
                        # print(baby.eye_list) 
                        #baby.baby = 'CLOSED'                            prev_read = 0
                    else:
                        if prev_read != cur_read:
                            cv2.putText(frame, "Blink Detected", (70, 70), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 2)
                            baby.eye_list = baby.eye_list[1:]
                            baby.eye_list.append(2)
                            # print(baby.eye_list) 
                            #baby.baby = 'BLINKED'
                            prev_read = 0  

        return frame
