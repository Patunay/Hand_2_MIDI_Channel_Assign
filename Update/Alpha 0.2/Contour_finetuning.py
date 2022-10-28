from tkinter import *
import tkinter
import cv2 as cv
import PIL.Image, PIL.ImageTk
from tkmacosx import Button
import numpy as np
import cv2 as cv

# Output variables
key_levels = ()
updated_black_k_contours = []


class contourfinetuning_black:
    def __init__(self,root,vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out):
        self.root=root
        self.root.title("Set Key Levels")
        self.finetuning_black_out = np.array(finetuning_black_out)
        self.vid = self.VideoCapture(vid_path,crop_reg,crop_dim,trans_matrix,self.finetuning_black_out)

        self.handles_contours = [0,5,10,15,20,25,30,35]

        # 8 trackbars for Bbs[:]    # Any possibility for non literal definition of Tk().scale objects?
        self.trackbar_Bb0 = Scale(self.root, from_=0, to=self.finetuning_black_out[5,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb0")
        self.trackbar_Bb0.set(self.finetuning_black_out[0,0,0,0])
        self.trackbar_Bb0.pack(anchor=W)

        self.trackbar_Bb1 = Scale(self.root, from_=self.finetuning_black_out[0,0,0,0]+1, to=self.finetuning_black_out[10,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb1")
        self.trackbar_Bb1.set(self.finetuning_black_out[5,0,0,0])
        self.trackbar_Bb1.pack(anchor=W)

        self.trackbar_Bb2 = Scale(self.root, from_=self.finetuning_black_out[5,0,0,0]+1, to=self.finetuning_black_out[15,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb2")
        self.trackbar_Bb2.set(self.finetuning_black_out[10,0,0,0])
        self.trackbar_Bb2.pack(anchor=W)

        self.trackbar_Bb3 = Scale(self.root, from_=self.finetuning_black_out[10,0,0,0]+1, to=self.finetuning_black_out[20,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb3")
        self.trackbar_Bb3.set(self.finetuning_black_out[15,0,0,0])
        self.trackbar_Bb3.pack(anchor=W)

        self.trackbar_Bb4 = Scale(self.root, from_=self.finetuning_black_out[15,0,0,0]+1, to=self.finetuning_black_out[25,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb4")
        self.trackbar_Bb4.set(self.finetuning_black_out[20,0,0,0])
        self.trackbar_Bb4.pack(anchor=W)

        self.trackbar_Bb5 = Scale(self.root, from_=self.finetuning_black_out[20,0,0,0]+1, to=self.finetuning_black_out[30,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb5")
        self.trackbar_Bb5.set(self.finetuning_black_out[25,0,0,0])
        self.trackbar_Bb5.pack(anchor=W)

        self.trackbar_Bb6 = Scale(self.root, from_=self.finetuning_black_out[25,0,0,0]+1, to=self.finetuning_black_out[35,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb6")
        self.trackbar_Bb6.set(self.finetuning_black_out[30,0,0,0])
        self.trackbar_Bb6.pack(anchor=W)

        self.trackbar_Bb7 = Scale(self.root, from_=self.finetuning_black_out[30,0,0,0]+1, to=self.vid.width,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb7")
        self.trackbar_Bb7.set(self.finetuning_black_out[35,0,0,0])
        self.trackbar_Bb7.pack(anchor=W)


        self.submit_button = Button(self.root, text="Set",bg="Green",fg="black",relief=RAISED,command=self.end_process)
        self.submit_button.pack(anchor=W)

        self.canvas = tkinter.Canvas(self.root, width = self.vid.width,height =  self.vid.height)
        self.canvas.pack()

        self.delay = 15
        self.update()
        self.root.mainloop()



    def update(self):   # needs to send current state of contours
        ret, frame = self.vid.get_frame(self.trackbar_Bb0.get(),self.trackbar_Bb1.get(),self.trackbar_Bb2.get(),self.trackbar_Bb3.get(),self.trackbar_Bb4.get(),self.trackbar_Bb5.get(),self.trackbar_Bb6.get(),self.trackbar_Bb7.get())  # Call function
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor = tkinter.NW)
        self.root.after(self.delay, self.update)

    def end_process(self):
        global updated_black_k_contours
        updated_black_k_contours = self.vid.updated_array
        self.root.destroy()

    class VideoCapture:
        def __init__(self,vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out):
            self.crop_reg = crop_reg
            self.crop_dim = crop_dim
            self.trans_matrix = trans_matrix
            self.ORIGINAL_finetuning_black_out = finetuning_black_out   # TO BE USED FOR COMPARISON

            self.finetuning_black_out = finetuning_black_out    # Delete when realtime state recognition is done

            self.key_notes_indexes = [0,5,10,15,20,25,30,35]
            self.height = crop_dim[0]
            self.width = crop_dim[1]

            self.total_distances = self.calculate_total_distances(self.ORIGINAL_finetuning_black_out)
            self.total_inner_percentage = self.calculate_inner_distances_percentages(self.ORIGINAL_finetuning_black_out,self.total_distances)   

            self.cap = cv.VideoCapture(vid_path)

        def calculate_total_distances(self,array):
            a = 0
            b = 5
            total_distances = []  
            for i in range(7):
                total_distance = array[b,2,0,0] - array[a,2,0,0]
                total_distances.append(total_distance)
                a += 5
                b += 5
            return total_distances

        def calculate_inner_distances_percentages(self,array,total_distances_array):
            stage_counter = 0
            index_substractor_factor = 0
            macro_distance_container = []
            tep_d_container = []

            for i in range(42):
                if i == 0:  # 1st case handle
                    prev_x = array[i,0,0,0] # get x pos of key note
                    stage_counter += 1
                    continue

                elif stage_counter == 0:  # 1st case handle
                    i = i - index_substractor_factor    # compensation for repeated contours
                    prev_x = array[i,0,0,0] # get x pos of key note
                    stage_counter += 1
                    continue


                elif i == 41:   # Last commit case handle
                    i = i - index_substractor_factor    # compensation for repeated contours
                    d = array[i,0,0,0] - prev_x
                    tep_d_container.append(d)

                    macro_distance_container.append(tep_d_container)    # commit to macro container
                    index_substractor_factor
                    tep_d_container = []    # reset temporal container
                    stage_counter = 0   # reset counter
                    continue 


                elif stage_counter == 5:  # last case handle
                    i = i - index_substractor_factor    # compensation for repeated contours
                    d = array[i,0,0,0] - prev_x
                    tep_d_container.append(d)

                    macro_distance_container.append(tep_d_container)    # commit to macro container
                    index_substractor_factor += 1
                    tep_d_container = []    # reset temporal container
                    stage_counter = 0   # reset counter
                    continue

                else:
                    i = i - index_substractor_factor    # compensation for repeated contours
                    d = array[i,0,0,0] - prev_x
                    tep_d_container.append(d)
                    prev_x = array[i,0,0,0] # update new substraction factor
                    stage_counter += 1
                    continue

            # now convert it to %
            temp_percent = []
            final_percent = []
            for i,k in zip(macro_distance_container,total_distances_array):
                # print(i,k)
                for e in i: # for each individual element in i
                    percentage = (e * 100)/k
                    temp_percent.append(percentage)
                final_percent.append(temp_percent)
                temp_percent = []
            return final_percent

        def calculate_inner_distances(self,array):
            stage_counter = 0
            index_substractor_factor = 0
            macro_distance_container = []
            tep_d_container = []

            for i in range(42):
                if i == 0:  # 1st case handle
                    prev_x = array[i,0,0,0] # get x pos of key note
                    stage_counter += 1
                    continue

                elif stage_counter == 0:  # 1st case handle
                    i = i - index_substractor_factor    # compensation for repeated contours
                    prev_x = array[i,0,0,0] # get x pos of key note
                    stage_counter += 1
                    continue


                elif i == 41:   # Last commit case handle
                    i = i - index_substractor_factor    # compensation for repeated contours
                    d = array[i,0,0,0] - prev_x
                    tep_d_container.append(d)

                    macro_distance_container.append(tep_d_container)    # commit to macro container
                    index_substractor_factor
                    tep_d_container = []    # reset temporal container
                    stage_counter = 0   # reset counter
                    continue 


                elif stage_counter == 5:  # last case handle
                    i = i - index_substractor_factor    # compensation for repeated contours
                    d = array[i,0,0,0] - prev_x
                    tep_d_container.append(d)

                    macro_distance_container.append(tep_d_container)    # commit to macro container
                    index_substractor_factor += 1
                    tep_d_container = []    # reset temporal container
                    stage_counter = 0   # reset counter
                    continue

                else:
                    i = i - index_substractor_factor    # compensation for repeated contours
                    d = array[i,0,0,0] - prev_x
                    tep_d_container.append(d)
                    prev_x = array[i,0,0,0] # update new substraction factor
                    stage_counter += 1
                    continue

            return macro_distance_container

        def update_display_contours(self, original_contour_array, current_state):   # outside update loop, no need to initialize the function evey update.
            # First update x position of key notes, then update inner content bassed on that
            canvas_array = original_contour_array   # make copy of array

            # Key Notes update            
            for x,i in enumerate(self.key_notes_indexes):
                width = canvas_array[i,2,0,0] - canvas_array[i,0,0,0]    # Calculate width:
                canvas_array[i,0:2,0,0] = current_state[x]    # Update x position
                canvas_array[i,2:4,0,0] = canvas_array[i,0,0,0] + width # Mantain original width

            # Inner Notes update:
            # calcualte updated key_note distances
            new_key_notes_distances = self.calculate_total_distances(canvas_array)

            # correlate outer sector distances with percentages and create percentages
            new_distances = []
            temp_new_d = []
            for i,k in zip(new_key_notes_distances,self.total_inner_percentage):
                
                for j in k:
                    update_d = (i*j)/100
                    temp_new_d.append(update_d)
                new_distances.append(temp_new_d)
                temp_new_d = []

            # Update inner_keys based on outer distances per sector (total of 7 sectors)
            cnt_1 = 0
            cnt_2 = 0
            for i in np.arange(36): 
                if i not in (self.key_notes_indexes):
                    width = canvas_array[i,2,0,0] - canvas_array[i,0,0,0]    # Calculate width:
                    new_x = canvas_array[i-1,0,0,0] + new_distances[cnt_1][cnt_2] # Calcualte new x
                    canvas_array[i,0:2,0,0] = new_x    # Update x position
                    canvas_array[i,2:4,0,0] = canvas_array[i,0,0,0] + width # Mantain original width

                    cnt_2 += 1
                    if cnt_2 == 4:
                        cnt_1 += 1  # next subarray
                        cnt_2 = 0   # reset suubarray index
            return canvas_array

        def get_frame(self,Bb0,Bb1,Bb2,Bb3,Bb4,Bb5,Bb6,Bb7):      # read current x values of contours and calculate other contours based on that, then, draw contours  
            current_state = (Bb0,Bb1,Bb2,Bb3,Bb4,Bb5,Bb6,Bb7)  # reads current state
            self.updated_array = self.update_display_contours(self.ORIGINAL_finetuning_black_out,current_state)   # modify display array according to current_state

            if self.cap.isOpened():
                ret, frame = self.cap.read()
                cropped_frame = frame[self.crop_reg[0]:self.crop_reg[1],self.crop_reg[2]:self.crop_reg[3]]
                trans_frame = cv.warpPerspective(cropped_frame,self.trans_matrix,(self.crop_dim[1],self.crop_dim[0]))

                if ret:
                    for i in np.arange(len(self.updated_array)):
                        if i in self.key_notes_indexes:
                            cv.drawContours(trans_frame,[self.updated_array[i]],0,(0,255,0),-1)
                        else:
                            cv.drawContours(trans_frame,[self.updated_array[i]],0,(255,255,0),-1)
                    return (ret, cv.cvtColor(trans_frame, cv.COLOR_BGR2RGB))
                else:
                    return (ret, None)
            else:
                return (ret, None)
        def __del__(self):
            if self.cap.isOpened():
                self.cap.release()

class contourfinetuning_white:  # needs to be adjusted for white keys
    def __init__(self,root,vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out):   # import both finetuning and literal white contours?
        self.root=root
        self.root.title("Set Key Levels")
        self.finetuning_black_out = np.array(finetuning_black_out)
        self.vid = self.VideoCapture(vid_path,crop_reg,crop_dim,trans_matrix,self.finetuning_black_out)

        self.handles_contours = [0,5,10,15,20,25,30,35]


        # Modify trackbars with As + last C [9 in total]
        # 8 trackbars for Bbs[:]    # Any possibility for non literal definition of Tk().scale objects?
        self.trackbar_Bb0 = Scale(self.root, from_=0, to=self.finetuning_black_out[5,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb0")
        self.trackbar_Bb0.set(self.finetuning_black_out[0,0,0,0])
        self.trackbar_Bb0.pack(anchor=W)

        self.trackbar_Bb1 = Scale(self.root, from_=self.finetuning_black_out[0,0,0,0]+1, to=self.finetuning_black_out[10,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb1")
        self.trackbar_Bb1.set(self.finetuning_black_out[5,0,0,0])
        self.trackbar_Bb1.pack(anchor=W)

        self.trackbar_Bb2 = Scale(self.root, from_=self.finetuning_black_out[5,0,0,0]+1, to=self.finetuning_black_out[15,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb2")
        self.trackbar_Bb2.set(self.finetuning_black_out[10,0,0,0])
        self.trackbar_Bb2.pack(anchor=W)

        self.trackbar_Bb3 = Scale(self.root, from_=self.finetuning_black_out[10,0,0,0]+1, to=self.finetuning_black_out[20,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb3")
        self.trackbar_Bb3.set(self.finetuning_black_out[15,0,0,0])
        self.trackbar_Bb3.pack(anchor=W)

        self.trackbar_Bb4 = Scale(self.root, from_=self.finetuning_black_out[15,0,0,0]+1, to=self.finetuning_black_out[25,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb4")
        self.trackbar_Bb4.set(self.finetuning_black_out[20,0,0,0])
        self.trackbar_Bb4.pack(anchor=W)

        self.trackbar_Bb5 = Scale(self.root, from_=self.finetuning_black_out[20,0,0,0]+1, to=self.finetuning_black_out[30,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb5")
        self.trackbar_Bb5.set(self.finetuning_black_out[25,0,0,0])
        self.trackbar_Bb5.pack(anchor=W)

        self.trackbar_Bb6 = Scale(self.root, from_=self.finetuning_black_out[25,0,0,0]+1, to=self.finetuning_black_out[35,0,0,0]-1,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb6")
        self.trackbar_Bb6.set(self.finetuning_black_out[30,0,0,0])
        self.trackbar_Bb6.pack(anchor=W)

        self.trackbar_Bb7 = Scale(self.root, from_=self.finetuning_black_out[30,0,0,0]+1, to=self.vid.width,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Bb7")
        self.trackbar_Bb7.set(self.finetuning_black_out[35,0,0,0])
        self.trackbar_Bb7.pack(anchor=W)


        self.submit_button = Button(self.root, text="Set",bg="Green",fg="black",relief=RAISED,command=self.end_process)
        self.submit_button.pack(anchor=W)

        self.canvas = tkinter.Canvas(self.root, width = self.vid.width,height =  self.vid.height)
        self.canvas.pack()

        self.delay = 15
        self.update()
        self.root.mainloop()



    def update(self):   # needs to send current state of contours   # Adjust sends
        ret, frame = self.vid.get_frame(self.trackbar_Bb0.get(),self.trackbar_Bb1.get(),self.trackbar_Bb2.get(),self.trackbar_Bb3.get(),self.trackbar_Bb4.get(),self.trackbar_Bb5.get(),self.trackbar_Bb6.get(),self.trackbar_Bb7.get())  # Call function
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor = tkinter.NW)
        self.root.after(self.delay, self.update)

    def end_process(self):
        global updated_black_k_contours
        updated_black_k_contours = self.vid.updated_array
        self.root.destroy()




def main(vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out,finetuning_white_out):
    flag = input("Do you wish to modify the contours? [Y/N] ")
    if flag == "N": # Skip entire module
        return
    elif flag == "Y":
        selector = int(input("Modify Black[0] or White[1]? "))
        if selector == 0:   # Black finetuner
            root = Tk()
            contourfinetuning_black(root,vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out)
            global updated_black_k_contours
            return updated_black_k_contours
        elif selector == 1: # White finetuner
            pass
        else:   # Exception error
            return
    else:   # Exception error
        return       

if __name__ == "__main__":
    main()

# after both are set, recompile in order and all set for Compare.py