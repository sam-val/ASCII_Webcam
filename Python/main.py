import cv2.cv2 as cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

def string_to_image_data(str, width, height):
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 1
    font_thickness = 1

    ### find the largest character's width, aka the '@' char:
    (max_char_w, max_char_h), base_line = cv2.getTextSize("@", font, font_scale, font_thickness)

    # control the new line height:
    new_line_distance = max_char_h*1.5

    # make a plain black image -- as a numpy array
    img = np.zeros((int(new_line_distance*height),max_char_w*width), np.uint8)

    # iterate and draw per character:
    for i in range(height):
        for j in range(width):
            cv2.putText(img,str[i*width+j],(int(j*max_char_w),int(i*new_line_distance)),font,font_scale,255,font_thickness)

    return img

def make_ascii_string(gray_img_data):
    # another_ramp = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

    gray_ramp = ['@','%','#','*','+','=', '-',':','.', ' ']
    ramp_length = len(gray_ramp)

    # convert gray-scale data into one single string:
    rs = ''
    for j in gray_img_data:
        rs += ''.join([gray_ramp[int(j / (256 / ramp_length))]])

    return rs


font = ImageFont.truetype('fonts/CourierScreenplay.ttf', 15) #load the font
capture = cv2.VideoCapture(0)
width, height = 1200, 900
FPS = 24
RESIZE_AMOUNT = 15 # times
width, height = width // RESIZE_AMOUNT, height // RESIZE_AMOUNT
capture.set(3, width)  ## set '3': the width
capture.set(4, height)  ## set '4': the height

while (True):
    # Capture frame by frame
    ret, frame = capture.read()

    # Process the image/frame
    mirror_framed = cv2.flip(frame, 1)
    gray = cv2.cvtColor(mirror_framed, cv2.COLOR_BGR2GRAY) # this an numpy array

    # resize to a smaller resolution to work with ASCII
    resized_gray = cv2.resize(gray, (width,height)).flatten()

    # Display the resulting frame:
        ## convert the RESIZED_GRAY IMAGE DATA => An ascii string
    ascii_string = make_ascii_string(resized_gray)
        ## then turn that string into an image (as an numpy array)
    ascii_img = string_to_image_data(ascii_string, width, height)

        ## then display the result and the gray scale one:
    cv2.imshow(winname='frame', mat=ascii_img)
    cv2.imshow(winname='gray', mat=mirror_framed)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()

