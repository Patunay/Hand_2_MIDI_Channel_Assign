from tkinter import *
import tkinter
import cv2 as cv
import PIL.Image, PIL.ImageTk
from tkmacosx import Button
import numpy as np
import cv2 as cv

# Output variables
key_levels = ()



class contourfinetuning_black:
    def __init__(self,root,vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out):
        self.root=root
        self.root.title("Set Key Levels")
        self.vid = self.VideoCapture(vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out)


        self.finetuning_black_out = np.array(finetuning_black_out)
        print(self.finetuning_black_out.shape)

        # print(self.finetuning_black_out)
        # print(self.finetuning_black_out[0,:,:]) # dim, col, row # gets individual contour

        self.handles_contours = [0,5,10,15,20,25,30,35]

        for i,x in enumerate(self.handles_contours):
            print(f"Bb{i}")
            print(self.finetuning_black_out[x,:,:]) # dim, col, row # gets individual contour
            # print(self.finetuning_black_out[5,0,0,1]) # dim, col, row # gets individual contour [a,b,c,d] a = contour group | b = row | c = ? | d = column
            print()



        # 8 trackbars for Bbs[:]
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



    def update(self):
        ret, frame = self.vid.get_frame(self.trackbar_Bb0.get(),self.trackbar_Bb1.get(),self.trackbar_Bb2.get(),self.trackbar_Bb3.get(),self.trackbar_Bb4.get(),self.trackbar_Bb5.get(),self.trackbar_Bb6.get(),self.trackbar_Bb7.get())  # Call function
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor = tkinter.NW)
        self.root.after(self.delay, self.update)

    def end_process(self):
        global key_levels
        key_levels = (self.trackbar_Bb0.get(),self.trackbar_Bb1.get(),self.trackbar_Bb2.get(),self.trackbar_Bb3.get(),self.trackbar_Bb4.get(),self.trackbar_Bb5.get(),self.trackbar_Bb6.get(),self.trackbar_Bb7.get())
        self.root.destroy()






    class VideoCapture:
        def __init__(self,vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out):
            self.crop_reg = crop_reg
            self.crop_dim = crop_dim
            self.trans_matrix = trans_matrix
            self.finetuning_black_out = finetuning_black_out
            # print(len(self.finetuning_black_out))

            self.height = crop_dim[0]
            self.width = crop_dim[1]

            self.cap = self.cap = cv.VideoCapture(vid_path)


        def get_frame(self,Bb0,Bb1,Bb2,Bb3,Bb4,Bb5,Bb6,Bb7):

            
            bl_l = [0,5,10,15,20,25,30,35]



            if self.cap.isOpened():
                ret, frame = self.cap.read()
                cropped_frame = frame[self.crop_reg[0]:self.crop_reg[1],self.crop_reg[2]:self.crop_reg[3]]
                trans_frame = cv.warpPerspective(cropped_frame,self.trans_matrix,(self.crop_dim[1],self.crop_dim[0]))


                if ret:
                    for i in np.arange(len(self.finetuning_black_out)):
                        if i in bl_l:
                            cv.drawContours(trans_frame,[self.finetuning_black_out[i]],0,(0,255,0),-1)
                        else:
                            cv.drawContours(trans_frame,[self.finetuning_black_out[i]],0,(255,255,0),-1)




                    return (ret, cv.cvtColor(trans_frame, cv.COLOR_BGR2RGB))
                else:
                    return (ret, None)
            else:
                return (ret, None)
        def __del__(self):
            if self.cap.isOpened():
                self.cap.release()









def main(vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out,finetuning_white_out):
    flag = input("Do you wish to modify the contours? [Y/N] ")
    if flag == "N": # Skip entire module
        return
    elif flag == "Y":
        selector = int(input("Modify Black[0] or White[1]? "))
        if selector == 0:   # Black finetuner
            root = Tk()
            contourfinetuning_black(root,vid_path,crop_reg,crop_dim,trans_matrix,finetuning_black_out)
            return # store new black contour array
        elif selector == 1: # White finetuner
            pass
        else:   # Exception error
            return
    else:   # Exception error
        return       





if __name__ == "__main__":
    main()