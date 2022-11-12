import cv2 as cv
import numpy as np
import mediapipe as mp
from tqdm import tqdm

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, min_detection_confidence=0.2)
mpDraw = mp.solutions.drawing_utils

def Compare(synqued_midi_data,vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours):     # Case by case comparison
    cap = cv.VideoCapture(vid_path)
    def vid_mid_comp(cap,onset,midi_event):
        # Preliminar video preparations
        index = midi_event-21   # To account for offset
        cap.set(cv.CAP_PROP_POS_MSEC,onset) # Set video position to exact moment
        _, frame = cap.read()
        cropped_frame = frame[crop_reg[0]:crop_reg[1],crop_reg[2]:crop_reg[3]]
        trans_frame = cv.warpPerspective(cropped_frame,trans_matrix,(crop_dim[1],crop_dim[0]))

        hand_detection_raw = trans_frame

        out_rgb = cv.cvtColor(hand_detection_raw, cv.COLOR_BGR2RGB)
        
        # Call contour corresponding to relevant case
        contour_border = midi_event_with_contours[index]    # Coordiantes need to be inverted?!!!!!!!!!
        # cv.drawContours(out_rgb,[midi_event_with_contours[index]],0,(0,255,0),-1)   # for Debugging viewer only

        _h, _w, _c = out_rgb.shape

        # Hand Detection
        def get_hand_data(img):
            lft_hand_lms = []
            rgt_hand_lms = []

            interest_lms = [4,8,12,16,20]   # Lnadmark ids for finguertips

            
            results = hands.process(img)
            if results.multi_hand_landmarks:    # If hand is detected
                # Get Handedness
                for hand_id, hand_Lms in enumerate(results.multi_hand_landmarks):  # For each hand | hand_id = Hand Index, hand_Lms = Compound Hand landmark
                    # print(f"HandId:{hand_id}_{results.multi_handedness[hand_id].classification[0].label}")  # Gets associated data?
                    if results.multi_handedness[hand_id].classification[0].label == "Left":   
                        for id, lms in enumerate(hand_Lms.landmark): # id = landmark index, lms = individual landmark data
                            # print(id)
                            # print(lms)
                            if id in interest_lms:  # Get tips of fingers
                                cx,cy = int(lms.x*_w),int(lms.y*_h)
                                # cv.circle(out_fliped,(cx,cy), 3,(0,255,0),cv.FILLED)   # green = Left
                                fng_tips = (cx,cy)
                                lft_hand_lms.append(fng_tips)
                    elif results.multi_handedness[hand_id].classification[0].label == "Right":
                        for id, lms in enumerate(hand_Lms.landmark): # id = landmark index, lms = individual landmark data
                            # print(id)
                            # print(lms)
                            if id in interest_lms:  # Get tips of fingers
                                cx,cy = int(lms.x*_w),int(lms.y*_h)
                                # cv.circle(out_fliped,(cx,cy), 3,(255,255,255),cv.FILLED)    # blanco = Right
                                fng_tips = (cx,cy)
                                rgt_hand_lms.append(fng_tips)
            else:
                relevant_data = None
 
            relevant_data = (lft_hand_lms,rgt_hand_lms) # Conbine output [0] = left, [1] = right | Keep in mind img is mirrored
            return relevant_data

        finger_handedness_data = get_hand_data(out_rgb)  # Gets relevant data

        # Draw relevant landmarks (debug only)
        # for idx ,i in enumerate(finger_handedness_data):    # for each hand
        #     if idx == 0:    # right = Red
        #         color = (0,0,255)
        #     elif idx == 1:  # left = White
        #         color = (255,255,255)

        #     for k in i: # for each landmark in hand
        #         cv.circle(out_rgb, k, 3, color,cv.FILLED)    # blanco = Right

        # Calculate a Guess
        def guess_logic_driver(relevant_landmark_data):
            # Inner function definitions
            def one_hand_detected(data):
                if data[0] != []:   # Only left hand info
                    return "Left"
                else:
                    return "Right"
            def inside_contour_check(data):
                flag = False
                for idx, hand_lms in enumerate(data):
                    # print("IDx:",idx)
                    for lms in hand_lms:
                        if cv.pointPolygonTest(contour_border, lms, False) in [0,1]:
                            flag = True
                            # cv.circle(out_rgb, lms, 3,(50,100,55),cv.FILLED)
                            # print("Found IDx:", idx)
                            if idx == 0:
                                guess = "Left"
                            else:
                                guess = "Right"
                            return flag, guess
                if flag == False:
                    return flag, None 
            def closest_contour_check(data):
                compound_distances = [None,None]    # [0] = left, [1]= right
                temp_dist = []
                for idx, hand_lms in enumerate(data):
                    for lms in hand_lms:
                        distance = abs(cv.pointPolygonTest(contour_border, lms, True))
                        temp_dist.append(distance)
                    compound_distances[idx] = temp_dist
                    temp_dist = []

                # print(compound_distances)
                min_left = min(compound_distances[0])
                min_rgt = min(compound_distances[1])
                min_list = [min_left,min_rgt]
                # print(min_list)

                min_value = min(min_list)
                min_index = min_list.index(min_value)

                # print(min_index)
                if min_index == 0:
                    guess = "Left"
                else:
                    guess = "Right"
                return guess

            # Logic Driver
            if relevant_landmark_data == None:
                # print("Option 0")
                return None
            elif relevant_landmark_data[0] == [] or relevant_landmark_data[1] == []:
                # print("Option 1")
                guess = one_hand_detected(relevant_landmark_data)
                return guess
            else:
                flag, guess = inside_contour_check(relevant_landmark_data)
                if flag != False:
                    # print("Option 3")
                    return guess
                else:
                    # print("Option 4")
                    guess = closest_contour_check(relevant_landmark_data)
                    return guess
    
        guess = guess_logic_driver(finger_handedness_data)

        def flip_guess(guess):
            if guess == None:
                return None
            elif guess == "Left":
                guess = "Right"
                return guess
            elif guess == "Right":
                guess = "Left"
                return guess

        guess = flip_guess(guess)
        # print(guess)
        
        # Debug viewer
        # cv.imshow("Compare Debug",out_rgb)
        return guess

        # Hand assigner code
        # while True: # Press scape to quit
        #     ch = 0xFF & cv.waitKey(1)
        #     if ch == ord("d"):
        #         cv.destroyAllWindows()
        #         cv.waitKey(1)  
        #         # cap.release()
        #         return guess
        

    handness_list = []
    pre_proc_list = []
    total_events = len(synqued_midi_data)

    midi_pairing_buffer = []
    hand_guess_buffer = []

    with tqdm(total=total_events, desc="Processing...",unit="Event") as pbar:
        for id, event in enumerate(synqued_midi_data):
            pre_proc_list.append(id)
            type_check = event[0]
            if type_check == "control_change": 
                pre_proc_list.append(-1)    # -1 flags pedal
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
                    hand_guess = vid_mid_comp(cap,onset,midi_event)

                    hand_guess_buffer.append(hand_guess)
                    midi_pairing_buffer.append(midi_event)  # index location for midi event and guess are the same

                    pre_proc_list.append(hand_guess)
                    handness_list.append(pre_proc_list)

                    pre_proc_list = []
                    pbar.update(1)

                else:   # Midi Note_Off
                    if midi_event in midi_pairing_buffer:   # if in regular buffer            
                        pair_indx = midi_pairing_buffer.index(midi_event)   # get index
                        pre_proc_list.append(hand_guess_buffer[pair_indx])  # add element
                        handness_list.append(pre_proc_list) # wrap element in a list

                        midi_pairing_buffer.pop(pair_indx)  # delete from buffers
                        hand_guess_buffer.pop(pair_indx)

                        pre_proc_list = []  # reset temporal container
                        pbar.update(1)
    return handness_list

def main(synqued_midi_data,vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours):
    handness_list = Compare(synqued_midi_data,vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours)
    return handness_list

if __name__ == "__main__":
    main()