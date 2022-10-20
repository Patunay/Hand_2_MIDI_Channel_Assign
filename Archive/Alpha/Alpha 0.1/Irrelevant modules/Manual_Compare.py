from cProfile import label
from tkinter import *
import tkinter
import cv2 as cv
import PIL.Image, PIL.ImageTk
from tkmacosx import Button
import math

# Output variables
guess = ""


def rotate_image(mat, angle):
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """

    height, width = mat.shape[:2] # image shape has 3 dimensions
    image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat




class Man_Compare:
    def __init__(self,root,synqued_midi_data,vid_path,angle2,croped_Area,trans_matrix,midi_event_with_contours):
        self.root=root
        self.root.title("Manual input")
        self.angle = angle2
        self.vid = self.VideoCapture(vid_path,self.angle)
        self.crop_reg = croped_Area
        self.trans_matrix = trans_matrix

        self.midi_event = synqued_midi_data[2]
        self.midi_event = self.midi_event.split("=")
        self.midi_event = int(self.midi_event[1])

        self.interest_data = synqued_midi_data[6]   # Gets onset
        self.midi_event_with_contours = midi_event_with_contours


        self.manual_entry_label = Label(self.root,text="Left[l] or Right[r]?")
        self.manual_entry_label.pack()
        self.guess_entry = Entry(self.root, width=3, borderwidth=2)
        self.guess_entry.pack()    

        self.submit_button = Button(self.root, text="Set",bg="Green",fg="black",relief=RAISED,command=self.end_process)
        self.submit_button.pack(anchor=W)

        self.canvas = tkinter.Canvas(self.root, width = self.vid.width,height = self.vid.height)
        self.canvas.pack()

        self.delay = 15
        self.update()
        self.root.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame(self.crop_reg,self.trans_matrix,self.interest_data,self.midi_event_with_contours,self.midi_event)  # Call function
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor = tkinter.NW)
        self.root.after(self.delay, self.update)



    def end_process(self):
        global guess
        guess = self.guess_entry.get()
        self.root.destroy()



    class VideoCapture:
        def __init__(self,vid_path,angle):
            self.angle = angle
            self.cap = self.cap = cv.VideoCapture(vid_path)
            self.width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)

        def get_frame(self,crop_reg,trans_mat,onset,midi_event_with_contours,midi_event):
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                self.cap.set(cv.CAP_PROP_POS_MSEC,onset)

                rotated = rotate_image(frame,self.angle)
                frameCropped = rotated[crop_reg[0]:crop_reg[1],crop_reg[2]:crop_reg[3]]
                out = cv.warpPerspective(frameCropped, trans_mat, (int(self.width),int(self.height)))
                cv.drawContours(out,[midi_event_with_contours[midi_event-21]],0,(0,255,0),-1)


                if True:
                    return (ret, cv.cvtColor(out, cv.COLOR_BGR2RGB))

                else:
                    return (ret, None)
            else:
                return (ret, None)
        def __del__(self):
            if self.cap.isOpened():
                self.cap.release()








def main(synqued_midi_data,vid_path,angle2,croped_Area,trans_matrix,midi_event_with_contours):
    root = Tk()
    Man_Compare(root,synqued_midi_data,vid_path,angle2,croped_Area,trans_matrix,midi_event_with_contours)
    return guess

if __name__ == "__main__":
    main()