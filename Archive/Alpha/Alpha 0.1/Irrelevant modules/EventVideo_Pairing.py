import cv2 as cv
import numpy as np


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



def Event_Video_Pairing(synqued_events, vidPath,angle,crop_region,keyb_bounds,hand_bounds):     # Case by case comparison
    def preliminary_creation_of_arrays():
        def contour_constructor():
            # Start of Contour constructor
            # for black
            split_fac = we/88
            # y = 90
            y_black = 130
            skip_list = [0,3,8,15,20,27,32,39,44,51,56,63,68,75,80,87]
            cnt = 0
            black_k_contours = []
            contour_temp = [] 
            for i in range(88):
                if i in skip_list:
                    continue

                else:   # lft lat
                    if cnt == 0:
                        i = int(i * split_fac)
                        xy1,xy2 = (i,0),(i,y_black)
                        # cv.line(out, xy1, xy2, (255,0,0), thickness=1)  # Left

                        contour_temp.append(xy1)
                        contour_temp.append(xy2)
                        cnt += 1

                    else:   # rgt lat + Top + Bot
                        i = int(i * split_fac)
                        xy1,xy2 = (i,0),(i,y_black)
                        # cv.line(out, xy1, xy2, (255,0,0), thickness=1)  # Rgt

                        top1, top2 = contour_temp[0],xy1
                        # cv.line(out, top1, top2, (255,0,0), thickness=1)  # Top

                        bot1, bot2 = contour_temp[1],xy2
                        # cv.line(out, bot1, bot2, (255,0,0), thickness=1)  # Bot

                        contour_temp.reverse()  # For Clockwise order requirement

                        # Commit
                        # Top
                        # contour_temp.append(top1)
                        contour_temp.append(top2)
                        # Rgt
                        # contour_temp.append(xy1)
                        contour_temp.append(xy2)
                        # Bot
                        # contour_temp.append(bot1)
                        # contour_temp.append(bot2)       
                        
                        # Commit to big container
                        black_k_contours.append(contour_temp)

                        # Empty temp container
                        contour_temp = []
                        cnt -= 1

            # White Keys
            split_fac_white = we/52
            # y = 138
            y_white = 170
            white_k_contours = []
            contour_temp = []
            cnt = 0
            for i in range(53):
                if cnt == 0:    # Lft
                    i = int(i * split_fac_white) + 0
                    xy1, xy2 = (i,0), (i,y_white)

                    # cv.line(out, xy1, xy2,(0,255,0), thickness=1) # Lines
                    
                    contour_temp.append(xy1)
                    contour_temp.append(xy2)
                    cnt += 1

                elif cnt == 1:                                # Rgt, Top, Bot
                    i = int(i * split_fac_white) + 0
                    xy1, xy2 = (i,0), (i,y_white)

                    # cv.line(out, xy1, xy2,(0,255,0), thickness=1) # Rgt

                    top1, top2 = contour_temp[0],xy1
                    # cv.line(out, top1, top2,(0,255,0), thickness=1) # Top

                    bot1, bot2 = contour_temp[1],xy2
                    # cv.line(out, bot1, bot2,(0,255,0), thickness=1) # Top

                    contour_temp.reverse()  # For Clockwise order requirement

                    # Commit
                    # Top
                    # contour_temp.append(top1)
                    contour_temp.append(top2)
                    # Rgt
                    # contour_temp.append(xy1)
                    contour_temp.append(xy2)
                    # Bot
                    # contour_temp.append(bot1)
                    # contour_temp.append(bot2)       
                    
                    # Commit to big container
                    white_k_contours.append(contour_temp)

                    # # Empty temp container
                    # contour_temp = []
                    cnt += 1

                else:
                    lft1,lft2 = contour_temp[2],contour_temp[3]
                    contour_temp = []
                    # cv.line(out, lft1, lft2,(0,255,0), thickness=1) # Lft

                    i = int(i * split_fac_white) + 0
                    rgt1, rgt2 = (i,0), (i,y_white)
                    # cv.line(out, rgt1, rgt2,(0,255,0), thickness=1) # Rgt

                    top1, top2 = lft1, rgt1
                    # cv.line(out, top1, top2,(0,255,0), thickness=1) # Top

                    bot1, bot2 = rgt2, lft2
                    # cv.line(out, bot1, bot2,(0,255,0), thickness=1) # Top

                    contour_temp = [lft2,lft1,rgt1,rgt2]
                    white_k_contours.append(contour_temp)

            white_k_count_Array = np.array(white_k_contours).reshape((-1,1,2)).astype(np.int32)
            white_k_count_Array = np.split(white_k_count_Array,52)

            black_k_count_Array = np.array(black_k_contours).reshape((-1,1,2)).astype(np.int32)
            black_k_count_Array = np.split(black_k_count_Array,36)
            return white_k_count_Array, black_k_count_Array
        def midi_note_creation(white_k_count_Array,black_k_count_Array):
            # Midi Note Number constructor [clasified by white/black]
            # Black
            b_k_gen = [22,25,27,30,32]
            l = []
            for i in b_k_gen:
                l.append(i)
            for i in range(1,10):
                b_k_gen[0] = b_k_gen[0]+12
                b_k_gen[1] = b_k_gen[1]+12
                b_k_gen[2] = b_k_gen[2]+12
                b_k_gen[3] = b_k_gen[3]+12
                b_k_gen[4] = b_k_gen[4]+12

                l.append(b_k_gen[0]) 
                l.append(b_k_gen[1])
                l.append(b_k_gen[2])
                l.append(b_k_gen[3])
                l.append(b_k_gen[4])
            black_midi_notes = l

            # White
            w_k_gen = [21,23,24,26,28,29,31]
            l = []
            for i in w_k_gen:
                l.append(i)
            for i in range(1,11):
                w_k_gen[0] = w_k_gen[0]+12
                w_k_gen[1] = w_k_gen[1]+12
                w_k_gen[2] = w_k_gen[2]+12
                w_k_gen[3] = w_k_gen[3]+12
                w_k_gen[4] = w_k_gen[4]+12
                w_k_gen[5] = w_k_gen[5]+12
                w_k_gen[6] = w_k_gen[6]+12

                l.append(w_k_gen[0]) 
                l.append(w_k_gen[1])
                l.append(w_k_gen[2])
                l.append(w_k_gen[3])
                l.append(w_k_gen[4])
                l.append(w_k_gen[5])
                l.append(w_k_gen[6])
            white_midi_notes = l

            # conform both in ascending order
            # Compound_Note_Array = np.array()
            tem = []
            w_cnt = 0
            b_cnt = 0
            for i in range(88):
                i += 21 
                if i in white_midi_notes:
                    try:
                        tem.append(white_k_count_Array[w_cnt])
                        w_cnt +=1
                    except:
                        pass

                elif i in black_midi_notes:
                    try:
                        tem.append(black_k_count_Array[b_cnt])
                        b_cnt +=1
                    except:
                        pass

            comp_midi_array = np.array(tem)
            # print(np.shape(comp_midi_array))
            return comp_midi_array

        white_countours,black_countours = contour_constructor()
        reference_midi_table = midi_note_creation(white_countours,black_countours)
        return reference_midi_table

    cap = cv.VideoCapture(vidPath)
    _, frame = cap.read()
    out_size = Framerescale(frame,angle,crop_region)
    h,w,_ = out_size.shape

    a,b = [keyb_bounds[0][0],keyb_bounds[0][1]] , [keyb_bounds[0][2],keyb_bounds[0][3]] # lft extrem , rgt extreme

    keyb_bounds_array = np.float32([a,hand_bounds[0],b,hand_bounds[1]])    # origin

    pt2 = np.float32([[0,0],[0,h],[w,0],[w,h]])   # target

    matrix = cv.getPerspectiveTransform(keyb_bounds_array,pt2) # outputs transformation matrix

    out = cv.warpPerspective(out_size, matrix, (w,h))
    he,we,_ = out.shape
    cap.release()

    midi_event_ref_table = preliminary_creation_of_arrays()

    # https://stackoverflow.com/questions/14161331/creating-your-own-contour-in-opencv-using-python for reference
    def img_viewer2(cap,onset,trans_mat,midi_event):
        index = midi_event-21
        cap.set(cv.CAP_PROP_POS_MSEC,onset)
        _, frame = cap.read()
        pre_process_video = Framerescale(frame,angle,crop_region)
        out = cv.warpPerspective(pre_process_video, trans_mat, (w,h))

        hand = out  # for hand recog purposes
        hand2 = hand


        blur = cv.GaussianBlur(hand,(5,5),cv.BORDER_DEFAULT)    # Maybe too blurry?

        # lower_black = np.array([0,0,0], dtype = "uint16")
        # upper_black = np.array([80,80,80], dtype = "uint16")
        # black_mask = cv.inRange(blur, lower_black, upper_black)

        # blur[np.where((blur == [0,0,0]).all(axis = 2))] = [0,255,255]     # it works
        # black_mask[np.where((black_mask == [0]).all(axis = 1))] = [0]

        y_fix = 14  # to get exactly at piano level
        interest_area_y_upped_bound = int(keyb_bounds[1][1] + y_fix) 
        tframe = blur[interest_area_y_upped_bound:-1:, :]

        lower_black = np.array([0,0,0], dtype = "uint16")
        upper_black = np.array([100,100,100], dtype = "uint16") # 80 works good
        black_mask = cv.inRange(tframe, lower_black, upper_black)

        






        canny = cv.Canny(black_mask,150,130)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(9,9))
        dilated = cv.dilate(canny,kernel,iterations=1)
        contours, _ = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # find the biggest countour (c) by the area
        # c = max(contours, key = cv.contourArea)
        # _x,_y,_w,_h = cv.boundingRect(c)

        # # draw the biggest contour (c) in green
        # cv.rectangle(hand,(_x,_y),(_x+_w,_y+_h),(0,255,0),2)


        # cv.drawContours(hand,contours,0,(0,255,0),-1)

        cv.drawContours(hand,[midi_event_ref_table[index]],0,(0,255,0),-1)

        cv.imshow("contours",hand)

        cv.imshow("interest area",dilated)


        # for every pixel over Y axis (Piano ref)
        #   if pixel == (255,255,255):
        #       pixel == (0,0,0)

        print(np.shape(black_mask))



        # cv.imshow("control",blur)
        # cv.imshow("black_mask",black_mask)
        # blur = cv.GaussianBlur(hand,(5,5),cv.BORDER_DEFAULT)    # Maybe too blurry?
        # grey = cv.cvtColor(blur,cv.COLOR_BGR2GRAY)
        # print(np.shape(grey))
        # ret, thresh = cv.threshold(grey,75,255, cv.THRESH_BINARY)   # me gusta mas que canny

        # canny = cv.Canny(grey,110,70)
        # dilated = cv.dilate(canny,(7,7),iterations=3)


        contour_border = midi_event_ref_table[index]


        # Hand assigner code


        # cv.imshow("Pair Check",out)
        while True: # Press scape to quit
            ch = 0xFF & cv.waitKey(1)
            if ch == ord("d"):
                cv.destroyAllWindows()
                cv.waitKey(1)  
                return contour_border


    cap = cv.VideoCapture(vidPath)
    for event in synqued_events:
        print(event)
        onset = event[6]
        midi_event = event[2]
        midi_event = midi_event.split("=")
        midi_event = int(midi_event[1])
        midi_contour_border =  img_viewer2(cap,onset,matrix,midi_event)
        print(midi_contour_border)
    return




def main(synqued_events,vidPath,angle,crop_region,keyb_bounds,hand_bounds):
    Event_Video_Pairing(synqued_events, vidPath,angle,crop_region,keyb_bounds,hand_bounds)
    return

if __name__ == "__main__":
    main()