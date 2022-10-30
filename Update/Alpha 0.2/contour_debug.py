import cv2 as cv
from numpy import arange

def check_black_k(vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours):  # Case by case comparison
    cap = cv.VideoCapture(vid_path)

    while True:
        _, frame = cap.read()
        cropped_frame = frame[crop_reg[0]:crop_reg[1],crop_reg[2]:crop_reg[3]]
        trans_frame = cv.warpPerspective(cropped_frame,trans_matrix,(crop_dim[1],crop_dim[0]))
        bl_l = [1,4,6,9,11,13,16,18,21,23,25,28,30,33,35,37,40,42,45,47,49,52,54,57,59,61,64,66,69,71,73,76,78,81,83,85]
        for i in bl_l:
            cv.drawContours(trans_frame,[midi_event_with_contours[i]],0,(0,255,0),-1)
        cv.imshow("Black key check",trans_frame)
        if cv.waitKey(20) & 0xFF==ord("d"): # print result to console
            cap.release()
            cv.destroyAllWindows()
            return 


def check_white_k(vid_path,crop_reg,crop_dim,trans_matrix,contours):  # Case by case comparison
    cap = cv.VideoCapture(vid_path)

    while True:
        _, frame = cap.read()
        cropped_frame = frame[crop_reg[0]:crop_reg[1],crop_reg[2]:crop_reg[3]]
        trans_frame = cv.warpPerspective(cropped_frame,trans_matrix,(crop_dim[1],crop_dim[0]))
        bl_l = [1,4,6,9,11,13,16,18,21,23,25,28,30,33,35,37,40,42,45,47,49,52,54,57,59,61,64,66,69,71,73,76,78,81,83,85]
        colors = [(0,255,0),(255,255,0),(0,0,255)]
        a_locator = [0,7,14,21,28,35,42,49,51]
        cl_sl = 0

        for i in arange(len(contours)):
            if i not in bl_l:
                if i in a_locator:
                    cl_sl = 2
                    cv.drawContours(trans_frame,[contours[i]],0,colors[cl_sl],-1)
                    cl_sl = 0
                else:
                    cv.drawContours(trans_frame,[contours[i]],0,colors[cl_sl],-1)
                    if cl_sl == 0:
                        cl_sl = 1
                    else:
                        cl_sl = 0
            else:
                pass


        cv.imshow("White key check",trans_frame)
        if cv.waitKey(20) & 0xFF==ord("d"): # print result to console
            cap.release()
            cv.destroyAllWindows()
            return 



def main(vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours):
    check_black_k(vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours)
    check_white_k(vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours)
    cv.destroyAllWindows
    return

if __name__ == "__main__":
    main()