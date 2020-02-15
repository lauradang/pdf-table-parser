import os
import re
import shutil

def move_images():
	cropped_images = [file for file in os.listdir("cropped_images") if ".jpg" in file]

	x_top_left_coords = list(
		set([re.findall(r"(.*?)\_", img)[0] for img in cropped_images])
	)

	for coord in x_top_left_coords:
		dir = os.path.join("output_{}".format(coord))
		if not os.path.exists(dir):
			os.mkdir(dir)

	for img in cropped_images:
		num = re.findall(r"(.*?)\_", img)[0].replace("_", "")
		shutil.move("cropped_images/{}".format(img), "output_{}/{}".format(num, img))