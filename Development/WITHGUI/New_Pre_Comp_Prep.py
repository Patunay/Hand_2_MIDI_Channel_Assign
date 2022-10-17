import cv2 as cv
import numpy as np



def Pre_comp_prep(crop_dim,bl_wh_lvls):     # Case by case comparison
    def preliminary_creation_of_arrays():
        def contour_constructor():
            # Start of Contour constructor

            # White Keys
            split_fac_white = crop_dim[1]/52
            y_white = bl_wh_lvls[1]
            white_k_contours = []
            contour_temp = []
            cnt = 0
            for i in range(53):
                if cnt == 0:    # For first white key only  # Left Bound
                    i *= split_fac_white 
                    print(i)
                    l_b, l_t = (i,y_white), (i,0)

                    contour_temp.append(l_b)    # LB_vortex  [0]
                    contour_temp.append(l_t)    # LT_vortex  [1]
                    cnt += 1

                elif cnt == 1:  # For first white key only    # Right Bound  and calculate other
                    i *= split_fac_white 
                    print(i)

                    r_t, r_b = (i,0), (i,y_white)   # Inverse order to fullfill Clockwise order of contour vertices

                    contour_temp.append(r_t)    # RT_vortex  [2]
                    contour_temp.append(r_b)    # RB_vortex  [3]
                    
                    # Commit Contour
                    white_k_contours.append(contour_temp)
                    cnt += 1

                else:   # For all other white Keys
                    l_b,l_t = contour_temp[3],contour_temp[2] # Grab right bounds of previous key # Inverted fullfill Clockwise order of contour vertices
                    contour_temp = []   # Empty temp. array

                    i *= split_fac_white 
                    print(i)

                    r_t, r_b = (i,0), (i,y_white)

                    contour_temp = [l_b,l_t,r_t,r_b]    # Join
                    white_k_contours.append(contour_temp)   #   Commit




            # Black Keys
            split_fac = crop_dim[1]/89
            y_black = bl_wh_lvls[0]
            skip_list = [0,3,8,15,20,27,32,39,44,51,56,63,68,75,80,87]
            cnt = 0
            black_k_contours = []
            contour_temp = [] 
            for i in range(88):
                if i in skip_list:
                    continue

                else:   # lft lat
                    if cnt == 0:
                        i *= split_fac
                        xy1,xy2 = (i,0),(i,y_black)
                        # cv.line(out, xy1, xy2, (255,0,0), thickness=1)  # Left

                        contour_temp.append(xy1)
                        contour_temp.append(xy2)
                        cnt += 1

                    else:   # rgt lat + Top + Bot
                        i *= split_fac
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
        reference_midi_table_contours = midi_note_creation(white_countours,black_countours)
        return reference_midi_table_contours

    midi_event_ref_table = preliminary_creation_of_arrays()
    return midi_event_ref_table




def main(crop_dim, bl_wh_lvls):
    midi_event_ref_table =  Pre_comp_prep(crop_dim,bl_wh_lvls)
    return midi_event_ref_table

if __name__ == "__main__":
    main()