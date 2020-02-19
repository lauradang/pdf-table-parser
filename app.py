#!/usr/bin/python3
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from pdf_to_jpg import pdf_to_jpg, resize_image
from crop import crop
import cv2

UPLOAD_FOLDER = "pdf"
IMAGE_FOLDER = "jpg"
VISUALIZE_FOLDER = os.path.join("static", "images")
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["IMAGE_FOLDER"] = IMAGE_FOLDER
app.config["VISUALIZE_FOLDER"] = VISUALIZE_FOLDER

app.config["TEMPLATES_AUTO_RELOAD"] = True

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            return redirect(url_for("upload_file", filename=filename))

    return render_template(
        "upload_pdf.html"
    )

@app.route("/edit-image", methods=["GET", "POST"])
def edit_image():  
    pdf_files = os.listdir(app.config["UPLOAD_FOLDER"])
    jpg_files = os.listdir(app.config["IMAGE_FOLDER"])

    if request.method == "GET":
        if not pdf_files:
            return redirect(url_for("upload_file"))

        pdf_to_jpg(os.path.join(app.config["UPLOAD_FOLDER"], pdf_files[0]))

        for jpg in jpg_files:
            image = crop(os.path.join(app.config["IMAGE_FOLDER"], jpg), False)
            cv2.imwrite(os.path.join(app.config["VISUALIZE_FOLDER"], jpg), image)    
    
    elif request.method == "POST":
        dilation = int(request.form["dilation"])
        erosion = int(request.form["erosion"])
        min_width = int(request.form["min_width"])
        min_height = int(request.form["min_height"])
        max_width = int(request.form["max_width"])
        max_height = int(request.form["max_height"])
        old_image = os.path.basename(request.form["image"])

        print(old_image)
        new_image = crop(
            os.path.join(app.config["IMAGE_FOLDER"], old_image), 
            False,
            dilation=dilation,
            erosion=erosion,
            min_height=min_height,
            min_width=min_width,
            max_height=max_height,
            max_width=max_width
        )

        print(request.form)
        cv2.imwrite(os.path.join(app.config["VISUALIZE_FOLDER"], old_image), new_image)    
   
    visualize = [os.path.join(app.config["VISUALIZE_FOLDER"], file) for file in os.listdir(app.config["VISUALIZE_FOLDER"])]
    print(visualize)
    return render_template(
        "edit_image.html",
        visualize=visualize
    )
