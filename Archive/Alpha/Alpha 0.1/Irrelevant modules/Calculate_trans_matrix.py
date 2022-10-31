import cv2 as cv
import numpy as np




def Pre_comp_prep(vid_path,crop_reg,crop_dim,keyboard_bounds,hand_bounds):     # Case by case comparison

    a,b = [keyboard_bounds[0][0],keyboard_bounds[0][1]] , [keyboard_bounds[0][2],keyboard_bounds[0][3]] # top_l, top_r vertices

    keyb_bounds_array = np.float32([a,hand_bounds[0],b,hand_bounds[1]])    # origin vertices

    pt2 = np.float32([[0,0],[0,crop_dim[0]],[crop_dim[1],0],[crop_dim[1],crop_dim[0]]])   # target vertices

    matrix = cv.getPerspectiveTransform(keyb_bounds_array,pt2) # outputs transformation matrix


    # cap = cv.VideoCapture(vid_path)
    # _, frame = cap.read()


    # cropped_frame = frame[crop_reg[0]:crop_reg[1],crop_reg[2]:crop_reg[3]]


    # trans_frame = cv.warpPerspective(cropped_frame,matrix,(crop_dim[1],crop_dim[0]))
    return matrix




def main(vid_path,crop_reg,crop_dim,keyboard_bounds,hand_bounds):
    matrix, midi_event_ref_table =  Pre_comp_prep(vid_path,crop_reg,crop_dim,keyboard_bounds,hand_bounds)
    return matrix, midi_event_ref_table

if __name__ == "__main__":
    main()