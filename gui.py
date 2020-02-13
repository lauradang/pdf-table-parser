from tkinter import *
import cv2
import numpy as np
import PIL.Image
import PIL.ImageTk
import argparse

class Editor(Tk):
	def __init__(self, file):
		Tk.__init__(self)
		self.title("PDF Table Editor")
		self.resizable(0,0)

		self.imageLabel = Label(self)
		self.imageLabel.grid(row=0,column=0)

		self.openImage(file)

		self.butFrame = Frame(self)
		self.butFrame.grid(row=0,column=1)

		self.flipLabel 			= Label(self.butFrame)
		self.flipLabel.pack()
		self.flipText			= Label(self.flipLabel, highlightbackground="#3E4149"	, 		text="Flip:"													).pack(fill=BOTH, side="left")
		self.buttonFlipHor 		= Button(self.flipLabel,highlightbackground="#3E4149"	, 		text="Horiz",			command=lambda: self.flip("HORIZONTAL")	).pack(fill=BOTH, side="left")
		self.buttonFlipVer 		= Button(self.flipLabel,highlightbackground="#3E4149"	, 		text="Vert",			command=lambda: self.flip("VERTICAL")	).pack(fill=BOTH, side="right")
		self.brightLabel		= Label(self.butFrame)
		self.brightLabel.pack()
		self.brightText			= Label(self.brightLabel,highlightbackground="#3E4149"	, 		text="Brightness:"												).pack(fill=BOTH, side="left")
		self.buttonBrightUp		= Button(self.brightLabel,highlightbackground="#3E4149"	, 		text="Up",				command=lambda: self.brightness("UP")	).pack(fill=BOTH, side="left")
		self.buttonBrightDown	= Button(self.brightLabel,highlightbackground="#3E4149"	, 		text="Down",			command=lambda: self.brightness("DOWN")	).pack(fill=BOTH, side="right")
		self.contrastLabel		= Label(self.butFrame)
		self.contrastLabel.pack()
		self.contrastText		= Label(self.contrastLabel, highlightbackground="#3E4149"	, 	text="Contrast:"												).pack(fill=BOTH, side="left")
		self.buttonContrastUp	= Button(self.contrastLabel,highlightbackground="#3E4149"	, 	text="Up",				command=lambda: self.contrast("UP")		).pack(fill=BOTH, side="left")
		self.buttonContrastDown	= Button(self.contrastLabel,highlightbackground="#3E4149"	, 	text="Down",			command=lambda: self.contrast("DOWN")	).pack(fill=BOTH, side="right")
		self.buttonGray 		= Button(self.butFrame, highlightbackground="#3E4149"	,  		text="Grayscale", 		command=self.grayscale 					).pack(fill=BOTH)
		self.zoomLabel 			= Label(self.butFrame)
		self.zoomLabel.pack()
		self.zoomText			= Label(self.zoomLabel, highlightbackground="#3E4149"	, 		text="Zoom:"													).pack(fill=BOTH, side="left")
		self.buttonZoomIn		= Button(self.zoomLabel,highlightbackground="#3E4149"	, 		text="In ",				command=lambda: self.zoom("IN")			).pack(fill=BOTH, side="left")
		self.buttonZoomOut		= Button(self.zoomLabel,highlightbackground="#3E4149"	, 		text="Out",				command=lambda: self.zoom("OUT")		).pack(fill=BOTH, side="right")
		self.rotateLabel		= Label(self.butFrame)
		self.rotateLabel.pack()
		self.rotateText			= Label(self.rotateLabel, highlightbackground="#3E4149"	, 		text="Rotate:"													).pack(fill=BOTH, side="left")
		self.buttonRotLeft		= Button(self.rotateLabel,highlightbackground="#3E4149"	, 		text="Left",			command=lambda: self.rotate("LEFT")		).pack(fill=BOTH, side="left")
		self.buttonRotRight		= Button(self.rotateLabel, 	highlightbackground="#3E4149"	, 	text="Right",			command=lambda: self.rotate("RIGHT")	).pack(fill=BOTH, side="right")
		
		self.buttonOpen			= Button(self.butFrame, highlightbackground="#3E4149"	, 		text="Open image", 		command=self.openImage					).pack(fill=BOTH)
		self.buttonSave			= Button(self.butFrame, highlightbackground="#3E4149"	, 		text="Save image", 		command=self.saveImage					).pack(fill=BOTH)
		self.buttonQuit			= Button(self.butFrame, text="Quit", highlightbackground="#3E4149", 	command=self.quit						).pack(fill=BOTH)

	def updateLabel(self, img):
		tempImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
		tempImg = PIL.Image.fromarray(tempImg)
		tempImg = PIL.ImageTk.PhotoImage(image=tempImg)

		self.imageLabel.configure(image=tempImg)
		self.imageLabel.image = tempImg

	def openImage(self, filename=None):
		if filename is None:	# if the filename was not passed as a parameter
			try:
				filename = filedialog.askopenfilename(initialdir="~/Pictures",title="Open image") #, filetypes=(("image files", "*.jpg"),("all files", "*.*")))
			except(OSError, FileNotFoundError):
				messagebox.showerror("Error","Unable to find or open file <filename>")
			except Exception as error:
				messagebox.showerror("Error","An error occurred: <error>")

		if filename:	# if filename is not an empty string
			self.image = cv2.imread(filename)	
			self.updateLabel(self.image)

	def saveImage(self):
		try:
			filename = filedialog.asksaveasfilename(initialdir="~/Pictures",title="Save image")
		except Exception as error:
			messagebox.showerror("Error","An error occurred: <error>")

		if filename:
			cv2.imwrite(filename, self.image)

	def flip(self, option):
		h, w, _ = self.image.shape
		temp = np.zeros((h,w,3), np.uint8)

		if option == "HORIZONTAL":
			for i in range(0,w):
				temp[:,i,:] = self.image[:,w-i-1,:]
		elif option == "VERTICAL":
			for j in range(0,h):
				temp[j,:,:] = self.image[h-j-1,:,:]

		self.image = temp
		self.updateLabel(self.image)

	def grayscale(self):
		b = self.image[:,:,0]
		g = self.image[:,:,1]
		r = self.image[:,:,2]

		gray = 0.114*b + 0.587*g + 0.299*r
		self.image[:,:,0] = self.image[:,:,1] = self.image[:,:,2] = gray
		self.updateLabel(self.image)

	def brightness(self, option):
		if option == "UP":
			bias = 20
		elif option == "DOWN":
			bias = -20

		self.image = cv2.addWeighted(self.image, 1, np.zeros(self.image.shape, self.image.dtype), 0, bias)
		self.updateLabel(self.image)

	def contrast(self, option):
		if option == "UP":
			gain = 1.25
		elif option == "DOWN":
			gain = 0.8

		self.image = cv2.addWeighted(self.image, gain, np.zeros(self.image.shape, self.image.dtype), 0, 0)
		self.updateLabel(self.image)

	def rotate(self, option):
		h, w, _ = self.image.shape
		temp = np.zeros((w,h,3), np.uint8)

		if option == "LEFT":
			for i in range(0,w):
				temp[w-i-1,:,:] = self.image[:,i,:]
		elif option == "RIGHT":
			for j in range(0,h):
				temp[:,h-j-1,:] = self.image[j,:,:]

		self.image = temp
		self.updateLabel(self.image)

if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser(description="A tool used to remove nonsense data and randomize persons and companies that have been removed by pii_cleaner.py.")
	arg_parser.add_argument("file", type=str, help="An image with tables to parse.")
	args = arg_parser.parse_args()

	app = Editor(args.file)
	app.mainloop()
