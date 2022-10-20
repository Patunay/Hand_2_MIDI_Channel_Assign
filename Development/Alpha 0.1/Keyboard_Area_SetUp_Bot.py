from tkinter import *
import tkinter
import cv2 as cv
import PIL.Image, PIL.ImageTk
from tkmacosx import Button

# Output variables
bot_key_bound = ()

class Keyboard_Area_SetUp_Bot:
    def __init__(self,root,vid_path,crop_reg,cropped_dim,tp_bnd):
        self.root=root
        self.root.title("Set Keyboard Bot Bound")
        self.vid = self.VideoCapture(vid_path,crop_reg,cropped_dim,tp_bnd)

        # Track Bars:
        self.trackbar_Xa = Scale(self.root,from_=0,to=self.vid.width,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2)
        self.trackbar_Xa.pack(anchor=W)
        self.trackbar_Ya = Scale(self.root,from_=0,to=self.vid.height,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2)
        self.trackbar_Ya.pack(anchor=W)

        self.trackbar_Xb = Scale(self.root,from_=0,to=self.vid.width,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2)
        self.trackbar_Xb.pack(anchor=W)
        self.trackbar_Yb = Scale(self.root,from_=0,to=self.vid.height,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2)
        self.trackbar_Yb.pack(anchor=W)

        # Submit Botton:
        self.submit_button = Button(self.root, text="Set",bg="Green",fg="black",relief=RAISED,command=self.end_process)
        self.submit_button.pack(anchor=W)

        # Cavas that displays the video:
        self.canvas = tkinter.Canvas(self.root,width=self.vid.width,height=self.vid.height)
        self.canvas.pack()

        # Update (needs fixing to avoid console update [non fatal] errors)
        self.delay = 15
        self.update()
        self.root.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame(self.trackbar_Xa.get(),self.trackbar_Ya.get(),self.trackbar_Xb.get(),self.trackbar_Yb.get())  # Call function
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor = tkinter.NW)
        self.root.after(self.delay, self.update)

    def end_process(self):
        global bot_key_bound
        bot_key_bound = (self.trackbar_Xa.get(),self.trackbar_Ya.get(),self.trackbar_Xb.get(),self.trackbar_Yb.get())
        self.root.destroy()



    class VideoCapture:
        def __init__(self,vid_path,crop_reg,cropped_dim,tp_bnd):
            self.crop_reg = crop_reg
            self.cropped_dim = cropped_dim
            self.tp_bnd = tp_bnd
            self.cap = self.cap = cv.VideoCapture(vid_path)
            self.height = cropped_dim[0]
            self.width = cropped_dim[1]

        def get_frame(self,X_a,Y_a,X_b,Y_b):
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                cropped_frame = frame[self.crop_reg[0]:self.crop_reg[1],self.crop_reg[2]:self.crop_reg[3]]

                if ret:
                    cv.line(cropped_frame,(self.tp_bnd[0],self.tp_bnd[1]),(self.tp_bnd[2],self.tp_bnd[3]),(0,255,0), thickness=2) # Top static Bound

                    cv.line(cropped_frame,(X_a,Y_a),(X_b,Y_b),(0,255,0), thickness=2) # Bot variable bound

                    return (ret, cv.cvtColor(cropped_frame, cv.COLOR_BGR2RGB))
                else:
                    return (ret, None)
            else:
                return (ret, None)
        def __del__(self):
            if self.cap.isOpened():
                self.cap.release()

def main(vid_path,crop_reg,cropped_dim,tp_bnd):
    root = Tk()
    Keyboard_Area_SetUp_Bot(root,vid_path,crop_reg,cropped_dim,tp_bnd)
    return bot_key_bound

if __name__ == "__main__":
    main()