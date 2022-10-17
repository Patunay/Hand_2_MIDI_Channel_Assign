import cv2 as cv
import numpy as np
import mediapipe as mp
from tqdm import tqdm
# import tqdm

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False)
mpDraw = mp.solutions.drawing_utils


def Framerescale(frame,angle,cropped_axis):
    def rescaleFrame(frame, scale=0.75):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        dimensions = (width, height)
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    vid_rotated = rotate_image(frame,angle)
    vidCropped = vid_rotated[cropped_axis[0]:cropped_axis[1],cropped_axis[2]:cropped_axis[3]]   # Correct crop axis definition
    # vid_processed = rescaleFrame(vidCropped,scale=0.6)
    return vidCropped

def rotate_image(mat, angle):
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """

    height, width = mat.shape[:2] # image shape has 3 dimensions
    image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat


def Compare(synqued_events, vidPath,angle,crop_region,trans_mat,stock_contours):     # Case by case comparison
    cap = cv.VideoCapture(vidPath)
    _, frame = cap.read()
    out_size = Framerescale(frame,angle,crop_region)
    h,w,_ = out_size.shape

    def img_viewer2(cap,onset,midi_event):
        # Preliminar preparations
        index = midi_event-21
        cap.set(cv.CAP_PROP_POS_MSEC,onset)
        _, frame = cap.read()
        pre_process_video = Framerescale(frame,angle,crop_region)
        out = cv.warpPerspective(pre_process_video, trans_mat, (w,h))
        hand_detection_raw = out
        # Call contour corresponding to relevant case
        cv.drawContours(out,[stock_contours[index]],0,(0,255,0),-1)
        contour_border = stock_contours[index]  

# Hand Detection
        def get_hand_data(img):
            handnessList = []
            landmarkList = []

            results = hands.process(img)
            if results.multi_hand_landmarks:    # If hand is detected
                handnesscont = results.multi_handedness
                for i in handnesscont:
                    handType = i
                    handType = str(handType)
                    handType = handType.split("\n")
                    handType = handType[3]
                    handType = handType.replace(" ","")
                    handType = handType.split(":")
                    handType = handType[1]
                    handType = handType.replace("\"","")      
                    if handType =="Left":   # fixes mirror issue
                        handType = "Right"
                    else:
                        handType ="Left"
                    handnessList.append(handType)
    
                    for handLms in results.multi_hand_landmarks:    # for each hand?
                        landmarkList.append(handLms)

                        for id, lm in enumerate(handLms.landmark):  # id=landmark, 
                            _h, _w, _c = hand_detection_raw.shape
                            cx,cy = int(lm.x*_w),int(lm.y*_h)
                            # print(id, cx,cy) 
                            # if id ==0:  # find location of individual landmark
                            #     cv.circle(frame,(cx,cy), 25,(0,255,0),cv.FILLED)
                        mpDraw.draw_landmarks(out, handLms, mpHands.HAND_CONNECTIONS)
            return handnessList,landmarkList




        out_rgb = cv.cvtColor(hand_detection_raw, cv.COLOR_BGR2RGB)
        handness_list, landmarks = get_hand_data(out_rgb)
        # print(handness_list)
        # print(len(landmarks))
        # print(landmarks)
        _h, _w, _c = hand_detection_raw.shape
        
        def check_if_only_one_hand(landmarks):
            if len(handness_list) == 1:
                guess = handness_list[0]
                return True, guess
            else:
                return False, None

        def check_if_inside_contour(landmarks):
            # 1) Check if landmark inside contour
            for hand_id, ind_hand in enumerate(landmarks):  # For each hand
                for id, lms in enumerate(ind_hand.landmark): #id = landmark index
                    cx,cy = int(lms.x*_w),int(lms.y*_h)
                    if cv.pointPolygonTest(contour_border, (cx,cy), False) in [0,1]:
                        # print("FOUND!") 
                        # print("Current hand id", hand_id)
                        if hand_id in (0,2):
                            hand_id = 0
                        else:
                            hand_id = 1
                        cv.circle(out,(cx,cy), 3,(0,255,255),cv.FILLED)
                        guess = handness_list[hand_id]
                        return  True, guess
            return False, None

        def check_last_resource(landmarks):
            left_distances = []
            right_distances = []
            compare = []
            for hand_id, ind_hand in enumerate(landmarks):  # For each hand

                for id, lms in enumerate(ind_hand.landmark): #id = landmark index
                    cx,cy = int(lms.x*_w),int(lms.y*_h)
                    dist = cv.pointPolygonTest(contour_border, (cx,cy), True)
                    dist = abs(dist)

                    if hand_id in (0,2):    # left
                        left_distances.append(dist)
                    else:
                        right_distances.append(dist)
            if len(left_distances) != 0:
                left_distances = min(left_distances)
            if len(right_distances) != 0:
                right_distances = min(right_distances)

            compare.append(left_distances)
            compare.append(right_distances)
            if len(compare) != 0:
                value = min(compare)
                min_index = compare.index(value)
                # print(compare)
                if min_index == 0:
                    guess = "Left"
                    return guess
                else:
                    guess = "Right"
                    return guess
            else:
                guess = None
                return guess

        def guess_logic_driver(landmarks):
            flag,guess = check_if_only_one_hand(landmarks)
            if flag != False:
                return guess

            else:
                flag, guess = check_if_inside_contour(landmarks)
                if flag != False:
                    return guess  

                else:
                    guess = check_last_resource(landmarks)
                    return guess
        
        guess = guess_logic_driver(landmarks)

        # cv.imshow("Keyboard contours",out)

        # Hand assigner code
        # cv.imshow("Pair Check",out)
        # while True: # Press scape to quit
        #     ch = 0xFF & cv.waitKey(1)
        #     if ch == ord("d"):
        #         cv.destroyAllWindows()
        #         cv.waitKey(1)  
        #         return guess
        # cap.release()
        return guess

    handness_list = []
    pre_proc_list = []
    total_events = len(synqued_events)


    midi_pairing_buffer = []
    hand_guess_buffer = []

    with tqdm(total=total_events, desc="Processing...",unit="Event") as pbar:
        for id, event in enumerate(synqued_events):
            # print(event)
            pre_proc_list.append(id)
            type_check = event[0]
            if type_check == "control_change": 
                pre_proc_list.append(-1)    # -1 flags pedal
                # print("Pedal index:",pre_proc_list)
                handness_list.append(pre_proc_list)
                pre_proc_list = []
                pbar.update(1)
                continue
            else:
                onset = event[6]    # gives onset
                midi_event = event[2]   
                midi_event = midi_event.split("=")
                midi_event = int(midi_event[1]) # Gives Midi note value

                midi_vel = event[3]
                midi_vel = midi_vel.split("=")
                midi_vel = int(midi_vel[1])

                if midi_vel != 0:   # Midi Note_On
                    hand_guess = img_viewer2(cap,onset,midi_event)

                    midi_pairing_buffer.append(midi_event)  # index location for midi event and guess are the same
                    hand_guess_buffer.append(hand_guess)

                    pre_proc_list.append(hand_guess)
                    handness_list.append(pre_proc_list)

                    pre_proc_list = []
                    pbar.update(1)
                else:   # Midi Note_Off
                    pair_indx = midi_pairing_buffer.index(midi_event)

                    pre_proc_list.append(hand_guess_buffer[pair_indx])
                    handness_list.append(pre_proc_list)
                    midi_pairing_buffer.pop(pair_indx)
                    hand_guess_buffer.pop(pair_indx)

                    pre_proc_list = []
                    pbar.update(1)

    return handness_list




def main(synqued_events, vidPath,angle,crop_region,trans_mat,stock_contours):
    handness_list = Compare(synqued_events, vidPath,angle,crop_region,trans_mat,stock_contours)
    return handness_list

if __name__ == "__main__":
    main()