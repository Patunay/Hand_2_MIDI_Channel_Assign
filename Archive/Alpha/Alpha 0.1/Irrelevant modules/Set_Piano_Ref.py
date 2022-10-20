from tkinter import *
import tkinter
import cv2 as cv
import PIL.Image, PIL.ImageTk
from tkmacosx import Button
import math

angle = 0
class Set_Piano_Ref:
    def __init__(self,root,vid_p):
        self.root=root
        self.root.title("Initial Processing")

        # Development/Assets/Video_assets/vid_asset2.mov
        self.vid = self.VideoCapture(vid_p)
        # print(Y_a,Y_b)
        # print(self.vid.width,self.vid.height)
        self.macro_w = self.vid.width

        self.trackbar_Ya = Scale(self.root, from_=0, to=self.vid.height,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2)
        self.trackbar_Ya.pack(anchor=W)
        self.trackbar_Yb = Scale(self.root, from_=0, to=self.vid.height,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2)
        self.trackbar_Yb.pack(anchor=W)

        self.submit_button = Button(self.root, text="Set",bg="Green",fg="black",relief=RAISED,command=self.end_process)
        self.submit_button.pack(anchor=W)


        self.canvas = tkinter.Canvas(self.root, width = self.vid.width,height =  self.vid.height)
        self.canvas.pack()
        # hbar = Scrollbar(self.canvas,orient=HORIZONTAL)
        # hbar.pack(side=TOP,fill=X)
        # hbar.config(command=self.canvas.xview)
        # self.canvas.config(xscrollcommand=hbar.set)

        self.delay = 15
        self.update()
        self.root.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame(self.macro_w,self.trackbar_Ya.get(),self.trackbar_Yb.get())
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor = tkinter.NW)
        self.root.after(self.delay, self.update)

    def end_process(self):
        piano_ref = (self.trackbar_Ya.get(),self.trackbar_Yb.get())
        # print(piano_ref)
        self.root.destroy()
        slope = (piano_ref[1]-piano_ref[0])/self.macro_w
        global angle
        angle = math.atan(slope)
        return

    class VideoCapture:
        def __init__(self,vid_path):
            self.cap = self.cap = cv.VideoCapture(vid_path)
            self.width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)

        def get_frame(self,mcw,Y_a,Y_b):
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret:
                    cv.line(frame,(0,Y_a),(int(mcw),Y_b),(0,255,0), thickness=2) # Lines
                    # Return a boolean success flag and the current frame converted to BGR
                    return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
                else:
                    return (ret, None)
            else:
                return (ret, None)

        def __del__(self):
            if self.cap.isOpened():
                self.cap.release()



def main(vid_path):
    root = Tk()
    Set_Piano_Ref(root,vid_path)
    return angle

if __name__ == "__main__":
    main()