from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from pdf_to_jpg import pdf_to_jpg, resize_image
from crop import crop

UPLOAD_FOLDER = "pdfs"
VISUALIZE_FOLDER = "visualize"
IMAGE_FOLDER = "jpg"
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["IMAGE_FOLDER"] = IMAGE_FOLDER
app.config["VISUALIZE_FOLDER"] = VISUALIZE_FOLDER

# for folder in app
# dir = os.path.join("visualize")
# if not os.path.exists(dir):
#     os.mkdir(dir)

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

        pdf_to_jpg(pdf_files[0])

        for jpg in jpg_files:
            image = crop("jpg/{}".format(jpg), False)
            image.save(os.path.join(app.config["VISUALIZE_FOLDER"], jpg))

    return render_template(
        "edit_image.html",
        visualize=os.listdir(app.config["VISUALIZE_FOLDER"])
    )
