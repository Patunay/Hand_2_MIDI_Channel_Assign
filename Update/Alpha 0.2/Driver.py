import Set_Crop_Reg
import Keyboard_Area_SetUp_Top
import Keyboard_Area_SetUp_Bot
import Set_bl_wh_Lvls
import Video_Midi_Sync
import Midi_Onset2Frame
# import Compare
import Consolidate_Midi

import contour_debug
import Contour_finetuning

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

def Pre_comp_prep(crop_dim,bl_wh_lvls):     # Case by case comparison
    def preliminary_creation_of_arrays():
        def contour_constructor():
            # Start of Contour constructor
            # White Keys
            split_fac = crop_dim[1]/52
            y_white = bl_wh_lvls[1]
            white_k_contours = []
            contour_temp = []
            cnt = 0 # used for case selection, takes values = [0,1,2]
            for i in range(53):
                if cnt == 0:    # For first white key only  # Left Bound
                    i *= split_fac 
                    l_b, l_t = (i,y_white), (i,0)
                    contour_temp.append(l_b)    # LB_vortex  [0]
                    contour_temp.append(l_t)    # LT_vortex  [1]
                    cnt += 1
                elif cnt == 1:  # For first white key only    # Right Bound  and calculate other
                    i *= split_fac
                    r_t, r_b = (i,0), (i,y_white)   # Inverse order to fullfill Clockwise order of contour vertices
                    contour_temp.append(r_t)    # RT_vortex  [2]
                    contour_temp.append(r_b)    # RB_vortex  [3]
                    # Commit Contour
                    white_k_contours.append(contour_temp)
                    cnt += 1
                else:   # For all other white Keys
                    l_b,l_t = contour_temp[3],contour_temp[2] # Grab right bounds of previous key # Inverted fullfill Clockwise order of contour vertices
                    contour_temp = []   # Empty temp. array
                    i *= split_fac 
                    r_t, r_b = (i,0), (i,y_white)
                    contour_temp = [l_b,l_t,r_t,r_b]    # Join
                    white_k_contours.append(contour_temp)   #   Commit

            # White keys finetuning:
            contour_temp = []   # Empty temp. array
            fine_tuning_white_countours = []
            cnt = 0 # used for case selection, takes values = [0,1,2]

            for i in range(53):
                if cnt == 0:    # For first white key only  # Left Bound
                    i *= split_fac 
                    l_b, l_t = (i,crop_dim[0]), (i,y_white)
                    contour_temp.append(l_b)    # LB_vortex  [0]
                    contour_temp.append(l_t)    # LT_vortex  [1]
                    cnt += 1
                elif cnt == 1:  # For first white key only    # Right Bound  and calculate other
                    i *= split_fac
                    r_t, r_b = (i,y_white), (i,crop_dim[0])   # Inverse order to fullfill Clockwise order of contour vertices
                    contour_temp.append(r_t)    # RT_vortex  [2]
                    contour_temp.append(r_b)    # RB_vortex  [3]
                    # Commit Contour
                    fine_tuning_white_countours.append(contour_temp)
                    cnt += 1
                else:   # For all other white Keys
                    l_b,l_t = contour_temp[3],contour_temp[2] # Grab right bounds of previous key # Inverted fullfill Clockwise order of contour vertices
                    contour_temp = []   # Empty temp. array
                    i *= split_fac 
                    r_t, r_b = (i,y_white), (i,crop_dim[0])
                    contour_temp = [l_b,l_t,r_t,r_b]    # Join
                    fine_tuning_white_countours.append(contour_temp)   #   Commit

            # Black Keys
            split_fac = crop_dim[1]/89  # New split fact
            y_black = bl_wh_lvls[0]
            skip_list = [0,3,8,15,20,27,32,39,44,51,56,63,68,75,80,87] # Works but there must be better "more intelligent method"
            mode_flag = True
            black_k_contours = []
            contour_temp = []   # Reset temp array
            for i in range(88):
                if i in skip_list:
                    continue
                else:   # [lft_bot, lft_top]
                    if mode_flag == True:    # First case handle
                        i *= split_fac
                        l_b, l_t = (i,y_black), (i,0)
                        contour_temp.append(l_b)    
                        contour_temp.append(l_t)
                        mode_flag = False

                    else:   # [rgt_top, rgt_bot]
                        i *= split_fac
                        r_t,r_b = (i,0),(i,y_black)
                        contour_temp.append(r_t)
                        contour_temp.append(r_b)
                        # Commit to big container
                        black_k_contours.append(contour_temp)
                        # Empty temp container
                        contour_temp = []
                        # Reset mode
                        mode_flag = True

            white_k_count_Array = np.array(white_k_contours).reshape((-1,1,2)).astype(np.int32)
            white_k_count_Array = np.split(white_k_count_Array,52)

            fine_tuning_white_countours = np.array(fine_tuning_white_countours).reshape((-1,1,2)).astype(np.int32)
            fine_tuning_white_countours = np.split(fine_tuning_white_countours,52)

            black_k_count_Array = np.array(black_k_contours).reshape((-1,1,2)).astype(np.int32)
            black_k_count_Array = np.split(black_k_count_Array,36)
            return white_k_count_Array, black_k_count_Array, fine_tuning_white_countours

        def midi_note_creation(white_k_count_Array,black_k_count_Array,fine_tuning_white_countours):
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
            tem = []
            finetuning_white_out = []
            finetuning_black_out = []
            white_out = []
            w_cnt = 0
            b_cnt = 0
            for i in range(88):
                i += 21 
                if i in white_midi_notes:
                    try:
                        tem.append(white_k_count_Array[w_cnt])
                        finetuning_white_out.append(fine_tuning_white_countours[w_cnt]) # for finteuning out
                        white_out.append(white_k_count_Array[w_cnt])
                        w_cnt +=1
                    except:
                        pass

                elif i in black_midi_notes:
                    try:
                        tem.append(black_k_count_Array[b_cnt])
                        finetuning_black_out.append(black_k_count_Array[b_cnt]) # for finteuning out
                        b_cnt +=1
                    except:
                        pass

            comp_midi_array = np.array(tem)
            finetuning_white_out = np.array(finetuning_white_out)
            white_out = np.array(white_out)
            return comp_midi_array,finetuning_white_out,finetuning_black_out,white_out

        white_countours,black_countours, white_fine_countours = contour_constructor()
        reference_midi_table_contours, finetuning_white_out, finetuning_black_out,white_out = midi_note_creation(white_countours,black_countours,white_fine_countours)
        return reference_midi_table_contours, finetuning_white_out, finetuning_black_out, white_out

    midi_event_ref_table, finetuning_white_out, finetuning_black_out, white_out = preliminary_creation_of_arrays()
    return midi_event_ref_table, finetuning_white_out, finetuning_black_out, white_out

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



# video_asset_container = ["Assets/Video_assets/video1.MOV","Assets/Video_assets/video2.mov","Assets/Video_assets/video3.mov","Assets/Video_assets/video4.MOV"]
# midi_paths_container = ["Assets/Midi_assets/midi_asset1.mid","Assets/Midi_assets/midi_asset2.mid","Assets/Midi_assets/midi_asset3.mid","Assets/Midi_assets/midi_asset4.mid"]



def Hand2MIDIChannelAssign():
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
    midi_event_with_contours, finetuning_white_out = Pre_comp_prep(crop_dim,bl_wh_lvls)



    contour_debug.main(vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours,finetuning_white_out)    # takes combined contours + midi note index

    # Finetuning module




    # Main Algorithm
    # handAsign_list = Compare.main(synqued_midi_data,vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours)

    # Create Output
    # Consolidate_Midi.main(midi_path,handAsign_list)
    return

def TEST_Hand2MIDIChannelAssign():
    vid_path = "Assets/Video_assets/video2.mov"
    midi_path = "Assets/Midi_assets/midi_asset2.mid"

    # Initial Video preparation
    # crop_reg, crop_dim = Set_Crop_Reg.main(vid_path)    # Works
    crop_reg, crop_dim = (684, 1080, 12, 1908), (396, 1896)




    # tp_kb_bound = Keyboard_Area_SetUp_Top.main(vid_path,crop_reg,crop_dim) # Sets Top Bound # Works
    # bt_kb_bound = Keyboard_Area_SetUp_Bot.main(vid_path,crop_reg,crop_dim,tp_kb_bound) # Sets Bot Bound # Works
    # hand_bound = crop_reg[1]-crop_reg[0]    # Y_b - Y_a = Y axis value of "bt_kb_bound"
    # keyboard_bounds = complete_keyboard_bounds(tp_kb_bound,bt_kb_bound) # Calculates Keyboard Bounds
    # print(keyboard_bounds)
    keyboard_bounds = ((37, 19, 1855, 7), (4, 247, 1892, 250), (37, 19, 4, 247), (1855, 7, 1892, 250))

    # hand_bounds = calc_hand_bounds(keyboard_bounds,hand_bound)  # Calculates Hand Bounds in respect to Keyboard bounds
    hand_bounds = ((-17.565789473684212, 396), (1914.2304526748972, 396))

    trans_matrix = trans_matrix_calc(crop_dim,keyboard_bounds,hand_bounds)

    # bl_wh_lvls = Set_bl_wh_Lvls.main(vid_path,crop_reg,crop_dim,trans_matrix)
    bl_wh_lvls = (166, 250)

    # Video-MIDI sync
    # sync_onsets = Video_Midi_Sync.main(vid_path)
    sync_onsets = (13033,137267)

    synqued_midi_data = Midi_Onset2Frame.main(sync_onsets,midi_path)


    # Final preparations:
    midi_event_with_contours, finetuning_white_out, finetuning_black_out, white_out = Pre_comp_prep(crop_dim,bl_wh_lvls)



    # contour_debug.main(vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours,finetuning_white_out)    # takes combined contours + midi note index

    Contour_finetuning.main(vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out,finetuning_white_out, white_out)

    # Finetuning module




    # Main Algorithm
    # handAsign_list = Compare.main(synqued_midi_data,vid_path,crop_reg,crop_dim,trans_matrix,midi_event_with_contours)

    # Create Output
    # Consolidate_Midi.main(midi_path,handAsign_list)
    return


# def test():
#     assets = 
#     Hand2MIDIChannelAssign(assets)


TEST_Hand2MIDIChannelAssign()