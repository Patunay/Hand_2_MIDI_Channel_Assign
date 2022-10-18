from tkinter import *
import tkinter
import cv2 as cv
import PIL.Image, PIL.ImageTk
from tkmacosx import Button
import numpy as np
import cv2 as cv

# Output variables
key_levels = ()



class Keyboard_Area_SetUp_Top:
    def __init__(self,root,vid_path,crop_reg,crop_dim,trans_matrix):
        self.root=root
        self.root.title("Set Key Levels")
        self.vid = self.VideoCapture(vid_path,crop_reg,crop_dim,trans_matrix)

        self.trackbar_bl = Scale(self.root, from_=0, to=self.vid.height,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="Black keys Level")
        self.trackbar_bl.pack(anchor=W)

        self.trackbar_wh= Scale(self.root, from_=0, to=self.vid.height,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2,label="White keys Level")
        self.trackbar_wh.pack(anchor=W)

        self.submit_button = Button(self.root, text="Set",bg="Green",fg="black",relief=RAISED,command=self.end_process)
        self.submit_button.pack(anchor=W)

        self.canvas = tkinter.Canvas(self.root, width = self.vid.width,height =  self.vid.height)
        self.canvas.pack()

        self.delay = 15
        self.update()
        self.root.mainloop()



    def update(self):
        ret, frame = self.vid.get_frame(self.trackbar_bl.get(),self.trackbar_wh.get())  # Call function
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor = tkinter.NW)
        self.root.after(self.delay, self.update)

    def end_process(self):
        global key_levels
        key_levels = (self.trackbar_bl.get(),self.trackbar_wh.get())
        self.root.destroy()






    class VideoCapture:
        def __init__(self,vid_path,crop_reg,crop_dim,trans_matrix):
            self.crop_reg = crop_reg
            self.crop_dim = crop_dim
            self.trans_matrix = trans_matrix

            self.height = crop_dim[0]
            self.width = crop_dim[1]

            self.cap = self.cap = cv.VideoCapture(vid_path)


        def get_frame(self,bl_lvl,wh_lvl):
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                cropped_frame = frame[self.crop_reg[0]:self.crop_reg[1],self.crop_reg[2]:self.crop_reg[3]]
                trans_frame = cv.warpPerspective(cropped_frame,self.trans_matrix,(self.crop_dim[1],self.crop_dim[0]))


                if ret:
                    cv.line(trans_frame,(0,bl_lvl),(int(self.width),bl_lvl),(255,0,0), thickness=2) 
                    cv.line(trans_frame,(0,wh_lvl),(int(self.width),wh_lvl),(255,0,0), thickness=2) 

                    return (ret, cv.cvtColor(trans_frame, cv.COLOR_BGR2RGB))
                else:
                    return (ret, None)
            else:
                return (ret, None)
        def __del__(self):
            if self.cap.isOpened():
                self.cap.release()









def main(vid_path,crop_reg,crop_dim,trans_matrix):
    root = Tk()
    Keyboard_Area_SetUp_Top(root,vid_path,crop_reg,crop_dim,trans_matrix)
    return key_levels

if __name__ == "__main__":
    main()