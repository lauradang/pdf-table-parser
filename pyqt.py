import sys
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QWidget, 
    QVBoxLayout, 
    QPushButton, 
    QFileDialog, 
    QLabel, 
    QTextEdit
)
from PyQt5.QtCore import QRect
from pdf2image import convert_from_path
from convert_pdf import pdf_to_jpg
from crop import crop

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PDF Parser"
        self.top = 50
        self.left = 450
        self.width = 400
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create layout
        vbox = QVBoxLayout()

        # Select and display image
        self.open_img_btn = QPushButton("Open Image")
        self.open_img_btn.clicked.connect(self.get_image_files)
        vbox.addWidget(self.open_img_btn)
    
        # Create label
        self.label = QLabel()
        vbox.addWidget(self.label)

        # Set layout
        self.setLayout(vbox)
        self.show()

    def get_image_files(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, 
            "Open file",
            "", 
            "Image files (*.pdf *.gif)"
        )
        pdf_to_jpg(fname)
        self.files = [os.path.join("jpg", file) for file in os.listdir("jpg") if ".jpg" in file]

        self.pixmap = QPixmap(self.files[0])
        if self.pixmap.width() > self.pixmap.height():
            self.pixmap = self.pixmap.scaledToWidth(500)
        else:
            self.pixmap = self.pixmap.scaledToHeight(700)

        self.label.setPixmap(QPixmap(self.pixmap))


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    app.exec_()
