from crop import crop
import PIL
from PIL import Image, ImageTk
from tkinter import *
import cv2

make_temp = False
file = "visualize.jpg"

root = Tk()

image = PIL.Image.open(file)

zoom = 0.13

#multiple image zise by zoom
pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])

img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y))) # the one-liner I used in my app
label = Label(root, image=img)
label.image = img # this feels redundant but the image didn't show up without it in my app
label.pack()

root.mainloop()

# window = Tk()

# cv_img = cv2.imread(path)
# height, width, no_channels = cv_img.shape

# image = image.resize((250, 250), Image.ANTIALIAS)

# canvas = Canvas(window, width=width, height=height)
# canvas.pack()

# photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
# canvas.create_image(0, 0, image=photo, anchor=NW)

# window.mainloop()