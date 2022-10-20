import Set_Crop_Reg
import Keyboard_Area_SetUp_Top
import Keyboard_Area_SetUp_Bot
import Set_bl_wh_Lvls
import Video_Midi_Sync
import Midi_Onset2Frame
import Pre_Comp_Prep
import Compare
import Consolidate_Midi
# import contour_debug

import numpy as np
from cv2 import getPerspectiveTransform


def complete_keyboard_bounds(top_bnd,bot_bnd):
    lft_bnd, rgt_bnd = (top_bnd[0],top_bnd[1],bot_bnd[0],bot_bnd[1]),(top_bnd[2],top_bnd[3],bot_bnd[2],bot_bnd[3])
    return (top_bnd,bot_bnd,lft_bnd,rgt_bnd)

def calc_hand_bounds(comp_key_bounds,hand_bound):
    lft = comp_key_bounds[2] # (3, 7, 16, 129)
    rgt = comp_key_bounds[3] # (1043, 0, 1030, 128)
    res_y = hand_bound

    slope1 = (lft[3]-lft[1]) / (lft[2]-lft[0])
    b1 = -(slope1*lft[0]-lft[1])
    res_x1 = (res_y - b1)/slope1
    hand_level_r = (res_x1, res_y)

    slope2 = (rgt[3]-rgt[1]) / (rgt[2]-rgt[0])
    b2 = -(slope2*rgt[0]-rgt[1])
    res_x2 = (res_y - b2)/slope2
    hand_level_l = (res_x2, res_y)
    return (hand_level_r,hand_level_l)

def trans_matrix_calc(crop_dim,keyboard_bounds,hand_bounds):
    a,b = [keyboard_bounds[0][0],keyboard_bounds[0][1]] , [keyboard_bounds[0][2],keyboard_bounds[0][3]] # top_l, top_r vertices
    origin_vert = np.float32([a,hand_bounds[0],b,hand_bounds[1]])    # origin vertices
    target_vert = np.float32([[0,0],[0,crop_dim[0]],[crop_dim[1],0],[crop_dim[1],crop_dim[0]]])   # target vertices
    matrix = getPerspectiveTransform(origin_vert,target_vert) # outputs transformation matrix
    return matrix

'''
ASSETS:

TEST 1:

Assets/Video_assets/video1.MOV
Assets/Midi_assets/midi_asset1.mid
Params:
crop_reg: (505, 964, 67, 1818)
start: 3233
end: 249633
-----------------------------------------------
-----------------------------------------------
Test 2:

Assets/Video_assets/video2.mov
Assets/Midi_assets/midi_asset2.mid
start: 13033
end: 137267
-----------------------------------------------
-----------------------------------------------
Test 3:

Assets/Video_assets/video3.mov
Assets/Midi_assets/midi_asset3.mid

start:
end:
-----------------------------------------------
-----------------------------------------------
Test 4:

Assets/Video_assets/video4.MOV
Assets/Midi_assets/midi_asset4.mid

start:
end:
-----------------------------------------------
-----------------------------------------------
'''

vid_path = "Assets/Video_assets/video2.mov"
midi_path = "Assets/Midi_assets/midi_asset2.mid"

# Initial Video preparation
crop_reg, crop_dim = Set_Crop_Reg.main(vid_path)    # Works

tp_kb_bound = Keyboard_Area_SetUp_Top.main(vid_path,crop_reg,crop_dim) # Sets Top Bound # Works
bt_kb_bound = Keyboard_Area_SetUp_Bot.main(vid_path,crop_reg,crop_dim,tp_kb_bound) # Sets Bot Bound # Works
hand_bound = crop_reg[1]-crop_reg[0]    # Y_b - Y_a = Y axis value of "bt_kb_bound"
keyboard_bounds = complete_keyboard_bounds(tp_kb_bound,bt_kb_bound) # Calculates Keyboard Bounds
hand_bounds = calc_hand_bounds(keyboard_bounds,hand_bound)  # Calculates Hand Bounds in respect to Keyboard bounds
trans_matrix = trans_matrix_calc(crop_dim,keyboard_bounds,hand_bounds)
bl_wh_lvls = Set_bl_wh_Lvls.main(vid_path,crop_reg,crop_dim,trans_matrix)


# Video-MIDI sync
sync_onsets = Video_Midi_Sync.main(vid_path)
synqued_midi_data = Midi_Onset2Frame.main(sync_onsets,midi_path)


# Final preparations:
midi_event_with_contours = Pre_Comp_Prep.main(crop_dim,bl_wh_lvls)
# contour_debug.main(vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours)

# Main Algorithm
handAsign_list = Compare.main(synqued_midi_data,vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours)

# Create Output
Consolidate_Midi.main(midi_path,handAsign_list)