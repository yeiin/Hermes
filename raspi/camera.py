import baby
import cv2 as cv
import mediapipe as mp
import time
import utils
import math
import numpy as np
# variables 
frame_counter =0
CEF_COUNTER =0
TOTAL_BLINKS =0
# constants
CLOSED_EYES_FRAME =3
FONTS =cv.FONT_HERSHEY_COMPLEX

# face bounder indices 
FACE_OVAL=[ 10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103,67, 109]

# Left eyes
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]

# right eyes indices
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ]  

# mediapipe facemesh
map_face_mesh = mp.solutions.face_mesh

# camera object 
camera = cv.VideoCapture(0)

# landmark detection function 
def landmarksDetection(img, results, draw=False):

    img_height, img_width= img.shape[:2]

    mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
    
if draw :
        [cv.circle(img, p, 2, (0,255,0), -1) for p in mesh_coord]

    return mesh_coord

# to calculate eye's length
def euclaideanDistance(point, point1):
	
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)

    return distance

# Blinking Ratio
def blinkRatio(img, landmarks, right_indices, left_indices):
    # Right eyes 
    # horizontal line 
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    # vertical line 
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]

    # LEFT_EYE 
    # horizontal line 
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]
    # vertical line 
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    rhDistance = euclaideanDistance(rh_right, rh_left)
    rvDistance = euclaideanDistance(rv_top, rv_bottom)

    lvDistance = euclaideanDistance(lv_top, lv_bottom)
    lhDistance = euclaideanDistance(lh_right, lh_left)

    reRatio = rhDistance/rvDistance
    leRatio = lhDistance/lvDistance

    ratio = (reRatio+leRatio)/2

    return ratio 


def main():
    global frame_counter, CEF_COUNTER, TOTAL_BLINKS
    
    try:
        with map_face_mesh.FaceMesh(min_detection_confidence =0.5, min_tracking_confidence=0.5) as face_mesh:

            start_time = time.time()

            while True:
                frame_counter +=1 # frame counter
                ret, frame = camera.read() 
                if not ret: 
                    break # no more frames break
                #  resizing frame
                
                frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_CUBIC)
                frame_height, frame_width= frame.shape[:2]
                rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
                results  = face_mesh.process(rgb_frame)
                if results.multi_face_landmarks:
                    mesh_coords = landmarksDetection(frame, results, False)
                    ratio = blinkRatio(frame, mesh_coords, RIGHT_EYE, LEFT_EYE)
                    utils.colorBackgroundText(frame,  f'Ratio : {round(ratio,2)}', FONTS, 0.7, (30,100),2, utils.PINK, utils.YELLOW)

                    if ratio >4.5: # eye closed
                        CEF_COUNTER +=1
                        utils.colorBackgroundText(frame,  f'Blink', FONTS, 1.7, (int(frame_height/2), 100), 2, utils.YELLOW, pad_x=6, pad_y=6, )
                        baby.eye_list = baby.eye_list[1:]
                        baby.eye_list.append(1)
                    else: # eye opened
                        if CEF_COUNTER>CLOSED_EYES_FRAME:
                            TOTAL_BLINKS +=1
                            CEF_COUNTER =0
                        else:
                            baby.eye_list = baby.eye_list[1:]
                            baby.eye_list.append(0) # eye opened
                    utils.colorBackgroundText(frame,  f'Total Blinks: {TOTAL_BLINKS}', FONTS, 0.7, (30,150),2)
                    
                    cv.polylines(frame,  [np.array([mesh_coords[p] for p in LEFT_EYE ], dtype=np.int32)], True, utils.GREEN, 1, cv.LINE_AA)
                    cv.polylines(frame,  [np.array([mesh_coords[p] for p in RIGHT_EYE ], dtype=np.int32)], True, utils.GREEN, 1, cv.LINE_AA)

                else: # no detection
                    print("no detection")
                    baby.eye_list = baby.eye_list[1:]
                    baby.eye_list.append(2)

                # calculating frame per seconds FPS
                end_time = time.time()-start_time
                fps = frame_counter/end_time

                frame =utils.textWithBackground(frame,f'FPS: {round(fps,1)}',FONTS, 1.0, (30, 50), bgOpacity=0.9, textThickness=2)

                cv.imshow('frame', frame)
                key = cv.waitKey(2)
                if key==ord('q') or key ==ord('Q'):
                    break
		
            cv.destroyAllWindows()
            camera.release()
    except KeyboardInterrupt:
        print(">>>>>>>>>>>>>>>>>>>>>>>>camera interrupt")
        
if __name__ == "__main__":
	main()
