import cv2
import os

# ap = argparse.ArgumentParser()

# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image to be OCR'd")

# args = vars(ap.parse_args())

def crop(img_path, make_temp):
    img = cv2.imread(img_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray,5)

    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)

    thresh = cv2.dilate(thresh, None, iterations=10)
    thresh = cv2.erode(thresh, None, iterations=5)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    dir = os.path.join("cropped_images")
    if not os.path.exists(dir):
        os.mkdir(dir)
        
    for i, cnt in enumerate(contours):
        x,y,w,h = cv2.boundingRect(cnt)
        
        if h < 200:
            continue

        if w > 2000:
            continue
        
        x_top_left_corner = x
        y_top_left_corner = y
        x_bottom_right_corner = x + w
        y_bottom_right_corner = y + h

        rectangle = [
            x_top_left_corner,
            y_top_left_corner,
            x_bottom_right_corner,
            y_bottom_right_corner
        ]

        cv2.rectangle(
            img,
            (x_top_left_corner, y_top_left_corner),
            (x_bottom_right_corner, y_bottom_right_corner),
            (0,255,0),
            5
        )

        if make_temp:
            crop_img = img[
                y_top_left_corner:y_bottom_right_corner, 
                x_top_left_corner:x_bottom_right_corner
            ]

            temp_file = "cropped_images/{}.jpg".format(
                str(rectangle).replace("[", "").replace("]", "").replace(", ", "_")
            )

            print("{}: {}, {}".format(temp_file, x_top_left_corner, y_top_left_corner))
            cv2.imwrite(temp_file, crop_img) 

    cv2.imwrite('visualize.jpg',img)
