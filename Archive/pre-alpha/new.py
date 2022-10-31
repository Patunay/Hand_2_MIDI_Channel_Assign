import cv2 as cv
import numpy as np
import math
import Midi_Module

# import matplotlib.pyplot as plt
# import mediapipe
# trackbars are broken...

# Verify video strightness
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



def Primary_processing(vidPath):
    cap = cv.VideoCapture(vidPath)
    def empty(a):
        pass
    width, height = int(cap.get(3)),int(cap.get(4))

    cv.namedWindow("Piano Reference Set-Up")
    cv.resizeWindow("Parameters",640,240)
    cv.createTrackbar("Ya","Piano Reference Set-Up",0,width,empty)   
    cv.createTrackbar("Yb","Piano Reference Set-Up",0,width,empty)   

    while True:
        isTrue, frame = cap.read()  
        Y_a = cv.getTrackbarPos("Ya","Piano Reference Set-Up")
        Y_b = cv.getTrackbarPos("Yb","Piano Reference Set-Up")
        cv.line(frame,(0,Y_a),(width,Y_b),(0,255,0), thickness=2) # Lines
        cv.imshow("Piano Reference",frame)

        if cv.waitKey(20) & 0xFF==ord("d"): # print result to console
            pia_ref = [Y_a,Y_b]
            # pia_ref = [724,744]
            pia_ref = [724,900]
            # cap.release()
            cv.destroyAllWindows()

            slope = pia_ref[1]-pia_ref[0]
            angle = math.atan(slope)
            # print(angle)
            # cap = cv.VideoCapture(vid)
            while True:
                isTrue, frame = cap.read()

                rotated = rotate_image(frame,angle/2)   # Angle /2 to compensate for new size in rotation????
                # Y_a = cv.getTrackbarPos("Ya","Piano Reference Set-Up")
                # cv.line(rotated,(0,Y_a),(original_dimensions[0],Y_a),(0,255,0), thickness=2) # Lines
                # print(rotated.shape)
                rotated_width,rotated_height = rotated.shape[0],rotated.shape[1]
                # cv.imshow("origin", frame)

                cv.imshow("rotated", rotated)

                if cv.waitKey(20) & 0xFF==ord("d"): # print result to console
                    cv.destroyAllWindows()
                    cv.namedWindow("Crop Set-Up")
                    cv.resizeWindow("Crop Set-Up",640,240)
                    cv.createTrackbar("Xa","Crop Set-Up",0,rotated_width,empty)   
                    cv.createTrackbar("Xb","Crop Set-Up",rotated_width,rotated_width,empty)   
                    cv.createTrackbar("Ya","Crop Set-Up",0,rotated_height,empty)   
                    cv.createTrackbar("Yb","Crop Set-Up",rotated_height,rotated_height,empty)  

                    while True:
                        isTrue, frame = cap.read()
                        rotated = rotate_image(frame,angle/2)   # Angle /2 to compensate for new size in rotation????

                        xaCrop = cv.getTrackbarPos("Xa","Crop Set-Up")
                        xbCrop = cv.getTrackbarPos("Xb","Crop Set-Up")
                        yaCrop = cv.getTrackbarPos("Ya","Crop Set-Up")
                        ybCrop = cv.getTrackbarPos("Yb","Crop Set-Up")

                        frameCropped = rotated[xaCrop:xbCrop,yaCrop:ybCrop]

                        cv.imshow("Cropped", frameCropped)

                        if cv.waitKey(20) & 0xFF==ord("d"): # Break loop when done
                            out_size = (frameCropped.shape[1],frameCropped.shape[0])
                            cropped_dimensions = (xaCrop,yaCrop,xbCrop,ybCrop)
                            cap.release()
                            cv.destroyAllWindows()
                            return angle/2, cropped_dimensions, out_size

def Framerescale(frame,angle,cropped_axis):
    def rescaleFrame(frame, scale=0.75):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        dimensions = (width, height)
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    vid_rotated = rotate_image(frame,angle)
    vidCropped = vid_rotated[cropped_axis[0]:cropped_axis[2],cropped_axis[1]:cropped_axis[3]]   # Correct crop axis definition
    vid_processed = rescaleFrame(vidCropped,scale=0.6)
    return vid_processed

def Canny_SetUp(vid,angle,cropped_dim):
    cap = cv.VideoCapture(vid)
    def empty(a):
        pass
    cv.namedWindow("Parameters")
    cv.resizeWindow("Parameters",640,240)
    cv.createTrackbar("Threshold1","Parameters",0,255,empty)   
    cv.createTrackbar("Threshold2","Parameters",0,255,empty)   

    while True:
        isTrue, frame = cap.read()
        pre_process_video = Framerescale(frame,angle,cropped_dim)

        threshold1 = cv.getTrackbarPos("Threshold1","Parameters")
        threshold2 = cv.getTrackbarPos("Threshold2","Parameters")

        imgCanny = cv.Canny(pre_process_video,threshold1,threshold2)

        cv.imshow("simplified",imgCanny)

        if cv.waitKey(20) & 0xFF==ord("d"): # print result to console
            print(f"Thr1: {threshold1}\nThr2: {threshold2}")
            cap.release()
            cv.destroyAllWindows()
            keyboard_area = 0
            return threshold1, threshold2

def Recognize_Genreal_Keyboard_Area(vid_path,angle,crop_region,can_thr1,can_thr2):  # stil very rough
    cap = cv.VideoCapture(vid_path)
    while True:
        isTrue, frame = cap.read()
        pre_process_video = Framerescale(frame,angle,crop_region)
        vidBLur = cv.GaussianBlur(pre_process_video,(7,7),1)
        vidGray = cv.cvtColor(vidBLur,cv.COLOR_BGR2GRAY)
        imgCanny = cv.Canny(vidGray,can_thr1,can_thr2)

        contours, hierarchy = cv.findContours(imgCanny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        for i, contour in enumerate(contours):
            area = cv.contourArea(contour)
            if area > 5:
                cv.drawContours(pre_process_video, contour,-1, (0,255,0),3)
                if i == 0:
                    continue

                epsilon = 0.01 * cv.arcLength(contour,True)
                approx = cv.approxPolyDP(contour,epsilon,True)
                x,y,w,h = cv.boundingRect(approx)
                x_mid = int(x + w/3)
                y_mid = int(y + h/1.5)
                coords = (x_mid, y_mid)
                colour = (0,255,0)
                font = cv.FONT_HERSHEY_DUPLEX

                if len(approx) == 4:
                    cv.putText(pre_process_video, "Rectangle", coords, font, 1, colour,1)

        cv.imshow("simplified",pre_process_video)
        if cv.waitKey(20) & 0xFF==ord("d"): # print result to console
            # print(f"Thr1: {threshold1}\nThr2: {threshold2}")
            cap.release()
            cv.destroyAllWindows()
            keyboard_area = 0
            return 

def Simple_Keyboard_Area_SetUp(vidPath,new_Dimensions,angle,crop_region):
    cap = cv.VideoCapture(vidPath)
    width, height = new_Dimensions[0],new_Dimensions[1]
    print(width,height)

    def empty(a):
        pass
    cv.namedWindow("Keyboard Area Set-Up[TOP_BOUND]")
    cv.resizeWindow("Keyboard Area Set-Up[TOP_BOUND]",640,240)
    cv.createTrackbar("Xa","Keyboard Area Set-Up[TOP_BOUND]",0,width,empty)   
    cv.createTrackbar("Ya","Keyboard Area Set-Up[TOP_BOUND]",0,height,empty)   
    cv.createTrackbar("Xb","Keyboard Area Set-Up[TOP_BOUND]",0,width,empty)   
    cv.createTrackbar("Yb","Keyboard Area Set-Up[TOP_BOUND]",0,height,empty)  

    while True:
        isTrue, frame = cap.read()
        pre_process_video = Framerescale(frame,angle,crop_region)

        X_a = cv.getTrackbarPos("Xa","Keyboard Area Set-Up[TOP_BOUND]")
        Y_a = cv.getTrackbarPos("Ya","Keyboard Area Set-Up[TOP_BOUND]")
        X_b = cv.getTrackbarPos("Xb","Keyboard Area Set-Up[TOP_BOUND]")
        Y_b = cv.getTrackbarPos("Yb","Keyboard Area Set-Up[TOP_BOUND]")
        cv.line(pre_process_video,(X_a,Y_a),(X_b,Y_b),(0,255,0), thickness=2) # Lines


        cv.imshow("lines", pre_process_video)

        if cv.waitKey(20) & 0xFF==ord("d"): # Break loop when done
            top_line = (X_a,Y_a,X_b,Y_b)
            # cap.release()
            cv.destroyAllWindows()

            cv.namedWindow("Keyboard Area Set-Up[BOT_BOUND]")
            cv.resizeWindow("Keyboard Area Set-Up[BOT_BOUND]",640,240)
            cv.createTrackbar("Xa","Keyboard Area Set-Up[BOT_BOUND]",0,width,empty)   
            cv.createTrackbar("Ya","Keyboard Area Set-Up[BOT_BOUND]",0,height,empty)   
            cv.createTrackbar("Xb","Keyboard Area Set-Up[BOT_BOUND]",0,width,empty)   
            cv.createTrackbar("Yb","Keyboard Area Set-Up[BOT_BOUND]",0,height,empty)  

            while True:
                isTrue, frame = cap.read()
                pre_process_video = Framerescale(frame,angle,crop_region)

                cv.line(pre_process_video,(top_line[0],top_line[1]),(top_line[2],top_line[3]),(0,255,0), thickness=2)

                X_a = cv.getTrackbarPos("Xa","Keyboard Area Set-Up[BOT_BOUND]")
                Y_a = cv.getTrackbarPos("Ya","Keyboard Area Set-Up[BOT_BOUND]")
                X_b = cv.getTrackbarPos("Xb","Keyboard Area Set-Up[BOT_BOUND]")
                Y_b = cv.getTrackbarPos("Yb","Keyboard Area Set-Up[BOT_BOUND]")
                cv.line(pre_process_video,(X_a,Y_a),(X_b,Y_b),(0,255,0), thickness=2) # Lines

                cv.imshow("lines", pre_process_video)

                if cv.waitKey(20) & 0xFF==ord("d"): # Break loop when done
                    bot_line = (X_a,Y_a,X_b,Y_b)
                    l_line, r_line = (top_line[0],top_line[1],bot_line[0],bot_line[1]),(top_line[2],top_line[3],bot_line[2],bot_line[3])
                    bounds = (top_line,bot_line,l_line, r_line)
                    cv.destroyAllWindows()

                    while True:
                        isTrue, frame = cap.read()
                        pre_process_video = Framerescale(frame,angle,crop_region)
                        for i in bounds:
                            cv.line(pre_process_video,(i[0],i[1]),(i[2],i[3]),(0,255,0), thickness=2)
                        
                        cv.imshow("lines", pre_process_video)

                        if cv.waitKey(20) & 0xFF==ord("d"): # Break loop when done
                            cv.destroyAllWindows()
                            cap.release()
                            return bounds

def Hand_Recognition():
    """
    Using mediapipe (ideal)
    or
    By pixel diference:
        mask the entire keyboard area as white
        convert a

    #####
    save screenshot of nul state keyboard, then for every midi event, compare nul state keyboard with
    corresponding screenshot of the midi event happening

    recognize the hands l and r and assign them to notes based on which one is the closest to the inuqired event

    """
    return

def Video_Midi_Sync(vidPath,new_Dimensions,angle,crop_region): # Returns frame which corresponds to first midi event
    # Set Frame location on first midi event
    cap = cv.VideoCapture(vidPath)
    # width, height = new_Dimensions[0],new_Dimensions[1]
    fps = cap.get(cv.CAP_PROP_FPS)
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))-1
    duration = frame_count/fps
    print("FPS: ",fps)
    print("Total Frames[From 0]: ",frame_count)
    minutes = int(duration/60)
    seconds = duration%60
    print('Total duration (M:S): ' + str(minutes) + ' : ' + str(seconds))
    print()

    first_event_location_ms = int(input("Enter location(ms) that corresponds to 1st midi event: "))  # Input inquiry frame
    last_event_location_ms = int(input("Enter location(ms) that corresponds to last midi event: "))  # Input inquiry frame

    # cap.set(cv.CAP_PROP_POS_FRAMES,frame_no)
    cap.set(cv.CAP_PROP_POS_MSEC,first_event_location_ms)

    _, frame = cap.read()
    pre_process_video = Framerescale(frame,angle,crop_region)

    
    cv.imshow("Set First",pre_process_video)

    while True: # Press scape to quit
        ch = 0xFF & cv.waitKey(1)
        if ch == ord("d"):
            cv.destroyAllWindows()
            cv.waitKey(1)  
            cap.release()
            return first_event_location_ms, last_event_location_ms

def Midi_event_onset_2_frame(frst_fram,last_event_location_ms):
    """
    Synchronize midi start with video

    Calculate the corresponding event for each midi event   (consider is ms notation is better or not[in terms of it being more precise])
    """
    # def MsOnset2FrameIndex(onset):
    #     frame_index = onset * (fps/1000)
    #     frame_index = frame_index + frst_fram
    #     return frame_index

    def onset_fix(inquiry,final_max,final_min,inq_max,inq_min): # mapping function: intup_range -> [mapping funciton] -> outpuit_range
        fixed = inquiry - inq_min
        fixed = fixed / (inq_max-inq_min)
        fixed = fixed * (final_max-final_min)
        fixed = fixed + final_min
        return fixed

    full_mid,ped_array, note_array = Midi_Module.main()

    delta = full_mid[0][5]
    print(delta)
    normalized_onsets = []
    for i in full_mid:
        # print(i[5])
        norm_onset = i[5] - delta
        norm_onset = norm_onset + frst_fram
        normalized_onsets.append(norm_onset)

    # print(normalized_onsets)
    inq_max = max(normalized_onsets)
    inq_min = min(normalized_onsets)
    final_max = last_event_location_ms
    final_min = frst_fram
    # print(inq_max,inq_min, final_max, final_min)

    fixed_onsets = []
    for i in normalized_onsets:
        i = onset_fix(i,final_max,final_min,inq_max,inq_min)
        fixed_onsets.append(i)

    norm_ons2 = []
    for i , e in zip(full_mid,fixed_onsets):
        i.append(e)
        norm_ons2.append(i)

    with open("Development/Assets/temp_files/checkonsetconversion.txt","w+") as f: # for debugging only
        for i in norm_ons2:
            i = str(i) + "\n"
            f.write(i)
    return norm_ons2



def Event_Video_Pairing(synqued_events, vidPath, new_Dimensions,angle,crop_region,keyb_bounds):
    def img_viewer(capture,onset):
        cap.set(cv.CAP_PROP_POS_MSEC,onset)
        _, frame = cap.read()
        pre_process_video = Framerescale(frame,angle,crop_region)

        cv.imshow("Pair Check",pre_process_video)

        while True: # Press scape to quit
            ch = 0xFF & cv.waitKey(1)
            if ch == ord("d"):
                cv.destroyAllWindows()
                cv.waitKey(1)  
                return

    def find_pitch_location(frame,pitch,keyb_bounds):    # Pitch in midi number
        # print(keyb_bounds)
        # Normalize to actual rectangle, then calculate all pitches, then translate normalized coordinates to actual cordinates
        
        return



    def img_viewer2(capture,onset):
        cap.set(cv.CAP_PROP_POS_MSEC,onset)
        _, frame = cap.read()
        pre_process_video = Framerescale(frame,angle,crop_region)
        for i in keyb_bounds:
            cv.line(pre_process_video,(i[0],i[1]),(i[2],i[3]),(0,255,0), thickness=2)

        cv.imshow("Pair Check",pre_process_video)

        while True: # Press scape to quit
            ch = 0xFF & cv.waitKey(1)
            if ch == ord("d"):
                cv.destroyAllWindows()
                cv.waitKey(1)  
                return  



    def calculate_pressed_key(event,onset,capture):
        print(event)
        img_viewer2(capture,onset)
        return

    cap = cv.VideoCapture(vidPath)
    print(keyb_bounds)
    for event in synqued_events:
        # print(event)
        onset = event[6]
        midi_event = event[2]

        # img_viewer(cap,onset)
        # Calculate pressed key on corresponding frame
        calculate_pressed_key(midi_event,onset,cap)
        # Based on that, calculate nearest hand and make the guess
    return



# recognize individual hands and guess deduce channel asignation

















def main():
    video_path = "Development/Assets/Video_assets/video.MOV"
    # angle, cropped_dim, new_dimensions = Primary_processing(video_path)
    # print(angle)
    # print(cropped_dim)
    angle, cropped_dim, new_dimensions = 0.7825572848770246, (531, 78, 917, 1825), (1759,422)
    # canny_thr_1, canny_thr_2 = Canny_SetUp(video_path,angle,cropped_dim)
    # canny_thr_1, canny_thr_2 = 123,255
    # Recognize_Genreal_Keyboard_Area(video_path,angle,cropped_dim,canny_thr_1,canny_thr_2)
    # keyb_bounds = Simple_Keyboard_Area_SetUp(video_path,new_dimensions,angle,cropped_dim)
    # print(keyb_bounds)

    keyb_bounds = ((3, 7, 1043, 0), (16, 129, 1030, 128), (3, 7, 16, 129), (1043, 0, 1030, 128))

    sync_frame, last_frame = Video_Midi_Sync(video_path,new_dimensions,angle,cropped_dim)
    synqued_midi_data =  Midi_event_onset_2_frame(sync_frame, last_frame)
    Event_Video_Pairing(synqued_midi_data,video_path,new_dimensions,angle,cropped_dim,keyb_bounds)
    return

if __name__ == "__main__":
    main()

# Extrapolate hands by either discrimination(pixel comparison of or vs case) or by color matching or by general hand area
# Calculate area of keyboard
# Conect midi with video

