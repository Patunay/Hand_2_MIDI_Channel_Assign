from tkinter import *
import tkinter
import cv2 as cv
import PIL.Image, PIL.ImageTk
from tkmacosx import Button

# Output variables
out_angle = 0
out_croped_area = ()


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


def out_dimension_Get(vid_path,cropped_area):
    cap = cv.VideoCapture(vid_path)
    _, frame = cap.read()
    while True:
        rotated = rotate_image(frame,out_angle)
        Cropped = rotated[cropped_area[0]:cropped_area[1],cropped_area[2]:cropped_area[3]]
        out_w,out_h = Cropped.shape[0],Cropped.shape[1]
        return (out_w,out_h)





class Set_Crop_Reg:
    def __init__(self,root,vid_p):
        self.root=root
        self.root.title("Initial Processing")

        self.vid = self.VideoCapture(vid_p)

        self.trackbar_Xa = Scale(self.root, from_=0, to=self.vid.width,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2)
        self.trackbar_Xa.pack(anchor=W)
        self.trackbar_Xa.set(0)

        self.trackbar_Xb = Scale(self.root, from_=0, to=self.vid.width,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2)
        self.trackbar_Xb.pack(anchor=W)
        self.trackbar_Xb.set(self.vid.width)

        self.trackbar_Ya = Scale(self.root, from_=0, to=self.vid.height,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2)
        self.trackbar_Ya.pack(anchor=W)
        self.trackbar_Ya.set(0)

        self.trackbar_Yb = Scale(self.root, from_=0, to=self.vid.height,orient=HORIZONTAL,sliderlength=15,length=self.vid.width/2)
        self.trackbar_Yb.pack(anchor=W)
        self.trackbar_Yb.set(self.vid.height)

        self.submit_button = Button(self.root, text="Set",bg="Green",fg="black",relief=RAISED,command=self.end_process)
        self.submit_button.pack(anchor=W)

        self.canvas = tkinter.Canvas(self.root,width=self.vid.width,height=self.vid.height)
        self.canvas.pack()

        self.delay = 15
        self.update()
        self.root.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame(self.trackbar_Xa.get(),self.trackbar_Xb.get(),self.trackbar_Ya.get(),self.trackbar_Yb.get())  # Call function
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor = tkinter.NW)
        self.root.after(self.delay, self.update)

    def end_process(self):
        global out_croped_area, out_angle
        out_croped_area = (self.trackbar_Ya.get(),self.trackbar_Yb.get(),self.trackbar_Xa.get(),self.trackbar_Xb.get())
        self.root.destroy()

    class VideoCapture:
        def __init__(self,vid_path):
            self.cap = self.cap = cv.VideoCapture(vid_path)
            self.width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)

        def get_frame(self,X_a,X_b,Y_a,Y_b):
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                
                if ret:
                    frameCropped = frame[Y_a:Y_b,X_a:X_b]
                    return (ret, cv.cvtColor(frameCropped, cv.COLOR_BGR2RGB))
                else:
                    return (ret, None)
            else:
                return (ret, None)
        def __del__(self):
            if self.cap.isOpened():
                self.cap.release()

def main(vid_path):
    root = Tk()
    Set_Crop_Reg(root,vid_path)

    cropped_dim = out_dimension_Get(vid_path,out_croped_area)
    return out_croped_area, cropped_dim

if __name__ == "__main__":
    main()