from turtle import width
import cv2 as cv
import cvzone
import math
import numpy as np

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

def Framerescale(frame,angle,cropped_axis):
    def rescaleFrame(frame, scale=0.75):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        dimensions = (width, height)
        return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    vid_rotated = rotate_image(frame,angle)
    vidCropped = vid_rotated[cropped_axis[0]:cropped_axis[2],cropped_axis[1]:cropped_axis[3]]   # Correct crop axis definition
    vid_processed = rescaleFrame(vidCropped,scale=0.6)
    return vid_processed

# Map keyboard layout to original video
video_path = "Development/Assets/Video_assets/video.MOV"
keyb_layout_path =cv.imread("Development/Assets/Layout/layout-01.png")



angle, cropped_dim, new_dimensions = 0.7825572848770246, (531, 78, 917, 1825), (1759,422)
keyb_bounds = ((3, 7, 1043, 0), (16, 129, 1030, 128), (3, 7, 16, 129), (1043, 0, 1030, 128))    # Lines

# create vertices and then convert them to cartesian coordenates
# keyb_bounds_vert = [(3,122),(16,0),(1030,1),(1043,129)]
keyb_bounds_vert = [(3,122),(16,0),(1030,1),(1043,129)]

step_1= (keyb_bounds_vert[0][0] * keyb_bounds_vert[1][1]) + (keyb_bounds_vert[1][0] * keyb_bounds_vert[2][1]) + (keyb_bounds_vert[2][0] * keyb_bounds_vert[3][1]) + (keyb_bounds_vert[3][0] * keyb_bounds_vert[0][1])
step_2= (keyb_bounds_vert[1][0] * keyb_bounds_vert[0][1]) + (keyb_bounds_vert[2][0] * keyb_bounds_vert[1][1]) + (keyb_bounds_vert[3][0] * keyb_bounds_vert[2][1]) + (keyb_bounds_vert[0][0] * keyb_bounds_vert[3][1])
origin_area = (step_1-step_2)/2

est_height =int( (122/2) + (128/2))
est_width =  int( origin_area / est_height)





keyb_bounds_array = np.float32([[3,7],[16,129],[1043,0],[1030,128]])    # origin

pt2 = np.float32([[0,0],[0,est_height],[est_width,0],[est_width,est_height]])   # target
# pt2 = np.float32([[0,0],[0,est_height],[est_width,0],[1759,422]])   # target


matrix = cv.getPerspectiveTransform(keyb_bounds_array,pt2)



cap = cv.VideoCapture(video_path)
while True:
    _, frame = cap.read()
    pre_process_video = Framerescale(frame,angle,cropped_dim)

    out = cv.warpPerspective(pre_process_video, matrix, (est_width,est_height))


    cv.imshow("simplified",out)
    cv.imshow("control",pre_process_video)


    if cv.waitKey(20) & 0xFF==ord("d"): # print result to console
        cv.destroyAllWindows()
        cap.release()
        break
