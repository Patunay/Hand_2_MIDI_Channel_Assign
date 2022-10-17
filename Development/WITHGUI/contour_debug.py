from time import sleep
import cv2 as cv
import numpy as np






def Compare(vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours):  # Case by case comparison
    # for i in midi_event_with_contours:
    #     print(i)
    cap = cv.VideoCapture(vid_path)
    print(midi_event_with_contours[87])

    while True:
        _, frame = cap.read()

        cropped_frame = frame[crop_reg[0]:crop_reg[1],crop_reg[2]:crop_reg[3]]
        trans_frame = cv.warpPerspective(cropped_frame,trans_matrix,(crop_dim[1],crop_dim[0]))
        # h, w, c = trans_frame.shape   # Check trans size
        # print(h,w)


        bl_l = [1,4,6,9,11,13,16,18,21,23,25,28,30,33,35,37,40,42,45,47,49,52,54,57,59,61,64,66,69,71,73,76,78,81,83,85]

        for i in bl_l:
            cv.drawContours(trans_frame,[midi_event_with_contours[i]],0,(0,255,0),-1)

        cv.imshow("debug",trans_frame)



        if cv.waitKey(20) & 0xFF==ord("d"): # print result to console
            cap.release()
            cv.destroyAllWindows()
            return 




def main(vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours):
    Compare(vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours)
    return

if __name__ == "__main__":
    main()