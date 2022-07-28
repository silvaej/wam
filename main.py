# Module Imports
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os
import cv2
import random
import csv
from datetime import datetime
import webbrowser

from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import CustomVideoObjectDetection

# Version 1.0.1.c
# by Efren Q. Silva, Jr.
# CpE 4102, BS Computer Engineering
# Batangas State University
#
# Things to do :
# Add error handling for each operation

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.WIDTH = 800
        self.HEIGHT = 520
        self.THRESHOLD = 50

        self.initUI()

        # Uncomment this for testing components ***TEST***
        # self.popup("video", r"test\sample.mp4", r"csv\single-image.csv")

    def initUI(self):
        # Configuring the main window
        self.setWindowTitle("#wearamask")
        self.statusBar().showMessage("version 1.0.1.c")
        self.statusBar().setFont(QFont("Zen Kurenaido", 8))
        self.setWindowIcon(QtGui.QIcon(r"images\icon.svg"))

        self.setFixedSize(QSize(self.WIDTH, self.HEIGHT))
        self.center()

        # Setting up the background image
        oImage = QImage(r"images\background.png")
        sImage = oImage.scaled(QSize(self.WIDTH, self.HEIGHT))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        # Title of the application shown on the top part of the window
        title = QLabel(self)
        title.setText("#wearamask")
        title.setFont(QFont("Zen Kurenaido", 40))
        title.setGeometry(QRect(96, 56, 368.8, 96.8))

        # Information Icon (link to online public repository)
        infobtn = QPushButton(self)
        infobtn.setGeometry(QRect(430, 96, 40, 40))

        infoIcon = QtGui.QIcon()
        infoIcon.addPixmap(QtGui.QPixmap(
            r"images\information.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        infobtn.setIcon(infoIcon)
        infobtn.setIconSize(QtCore.QSize(40, 40))
        infobtn.setFlat(True)
        infobtn.clicked.connect(lambda : webbrowser.open("https://github.com/silvaej/mask-detection-pyqt5"))

        # Button for identification using image file
        imagebtn = QPushButton(self)
        imagebtn.setGeometry(QRect(145.6, 193.6, 106.4, 106.4))

        imageIcon = QtGui.QIcon()
        imageIcon.addPixmap(QtGui.QPixmap(
            r"images\image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        imagebtn.setIcon(imageIcon)
        imagebtn.setIconSize(QtCore.QSize(106.4, 106.4))
        imagebtn.setFlat(True)

        imagebtn.clicked.connect(self.getImage)

        # Image Label
        imageLabel = QLabel(self)
        imageLabel.setText("UPLOAD IMAGE")
        imageLabel.setFont(QFont("Zen Kurenaido", 12))
        imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        imageLabel.setGeometry(QRect(78.8, 310, 240, 32))

        # Button for identification using video file
        videobtn = QPushButton(self)
        videobtn.setGeometry(QRect(348.8, 193.6, 106.4, 106.4))

        videoIcon = QtGui.QIcon()
        videoIcon.addPixmap(QtGui.QPixmap(
            r"images\video.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        videobtn.setIcon(videoIcon)
        videobtn.setIconSize(QtCore.QSize(106.4, 106.4))
        videobtn.setFlat(True)

        videobtn.clicked.connect(self.getVideo)

        # Video Label
        videoLabel = QLabel(self)
        videoLabel.setText("UPLOAD VIDEO")
        videoLabel.setFont(QFont("Zen Kurenaido", 12))
        videoLabel.setAlignment(QtCore.Qt.AlignCenter)
        videoLabel.setGeometry(QRect(282, 310, 240, 32))

        # Button for identification using video from an input device
        webcambtn = QPushButton(self)
        webcambtn.setGeometry(QRect(552, 193.6, 106.4, 106.4))

        webCamIcon = QtGui.QIcon()
        webCamIcon.addPixmap(QtGui.QPixmap(
            r"images\webcam.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        webcambtn.setIcon(webCamIcon)
        webcambtn.setIconSize(QtCore.QSize(106.4, 106.4))
        webcambtn.setFlat(True)

        webcambtn.clicked.connect(self.useCam)

        # Webcam Label
        webCamLabel = QLabel(self)
        webCamLabel.setText("USE WEBCAM")
        webCamLabel.setFont(QFont("Zen Kurenaido", 12))
        webCamLabel.setAlignment(QtCore.Qt.AlignCenter)
        webCamLabel.setGeometry(QRect(485.2, 310, 240, 32))

        # Profile Icon
        profilebtn = QPushButton(self)
        profilebtn.setGeometry(QRect(665.6, 398.4, 40, 40))

        profileIcon = QtGui.QIcon()
        profileIcon.addPixmap(QtGui.QPixmap(
            r"images\profile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        profilebtn.setIcon(profileIcon)
        profilebtn.setIconSize(QtCore.QSize(40, 40))
        profilebtn.setFlat(True)

        profilebtn.clicked.connect(lambda : webbrowser.open("https://www.linkedin.com/in/efren-silva-jr-b62708227/"))

        # GitHub Icon
        githubbtn = QPushButton(self)
        githubbtn.setGeometry(QRect(605.6, 398.4, 40, 40))

        gitHubIcon = QtGui.QIcon()
        gitHubIcon.addPixmap(QtGui.QPixmap(
            r"images\github.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        githubbtn.setIcon(gitHubIcon)
        githubbtn.setIconSize(QtCore.QSize(40, 40))
        githubbtn.setFlat(True)
        githubbtn.clicked.connect(lambda : webbrowser.open("https://github.com/silvaej"))

        # Twitter Icon
        twitterbtn = QPushButton(self)
        twitterbtn.setGeometry(QRect(545.6, 398.4, 40, 40))

        twitterIcon = QtGui.QIcon()
        twitterIcon.addPixmap(QtGui.QPixmap(
            r"images\twitter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        twitterbtn.setIcon(twitterIcon)
        twitterbtn.setIconSize(QtCore.QSize(40, 40))
        twitterbtn.setFlat(True)

        twitterbtn.clicked.connect(lambda : webbrowser.open("https://twitter.com/zlbss"))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def getImage(self):
        fname = QFileDialog.getOpenFileName(
            self, "Open file", "./", "Image files (*.jpg *.png)")
        self.imagePath = fname[0]

        self.detectImage()

    def detectImage(self):
        timestamp = datetime.now().strftime("%f")

        detector = CustomObjectDetection()
        detector.setModelTypeAsYOLOv3()

        detector.setModelPath("./src/model.h5")
        detector.setJsonPath("./src/model.json")
        detector.loadModel()

        output_name = r"output\{}-{}.jpg".format(timestamp, str(random.randint(0, 10000)).zfill(4))
        csv_file = r"csv\{}-single-image.csv".format(timestamp)

        detections = detector.detectObjectsFromImage(
            input_image=self.imagePath,
            output_image_path=output_name,
            minimum_percentage_probability=self.THRESHOLD)

        # Create CSV File from the image
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            # columns name
            writer.writerow(['CLASS', 'PERCENTAGE'])
            
            for eachObject in detections:
                writer.writerow([eachObject["name"], eachObject["percentage_probability"]])
        self.popup("image", output_name, csv_file)

    def getVideo(self):
        vidname = QFileDialog.getOpenFileName(self, "Open file", "./", "Video files (*.avi *.mp4)")
        self.videoPath = vidname[0]
        self.detectVideo()
    
    def detectVideo(self):
        timestamp = datetime.now().strftime("%f")

        output_name = r"output\{}-{}".format(timestamp, str(random.randint(0, 10000)).zfill(4))
        csv_file = r"csv\{}-video.csv".format(timestamp)

        classid = []
        percentage =[]

        video_detector = CustomVideoObjectDetection()
        video_detector.setModelTypeAsYOLOv3()
        video_detector.setModelPath(r"src\model.h5")
        video_detector.setJsonPath(r"src\model.json")
        video_detector.loadModel()

        def forFrame(_, output_array, __):
            for eachObject in output_array:
                classid.append(eachObject["name"])
                percentage.append(eachObject["percentage_probability"])

        video_detector.detectObjectsFromVideo(
            input_file_path=self.videoPath,
            output_file_path=output_name,
            per_frame_function=forFrame,
            minimum_percentage_probability=self.THRESHOLD,
            frames_per_second=10,
            log_progress=True,
            # For testing purposes
            # detection_timeout=10
            )

        # Create CSV File
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            #columns name
            writer.writerow(["CLASS", "PERCENTAGE"])
            for (classid_x, percentage_x) in zip (classid, percentage):
                writer.writerow([classid_x, percentage_x])

            self.popup("video", output_name+".avi", csv_file)

    def useCam(self):
        timestamp = datetime.now().strftime("%f")

        camera = cv2.VideoCapture(0)

        output_name = r"output\{}-{}".format(timestamp, str(random.randint(0, 10000)).zfill(4))
        csv_file = r"csv\{}-camera.csv".format(timestamp)

        classid = []
        percentage =[]

        video_detector = CustomVideoObjectDetection()
        video_detector.setModelTypeAsYOLOv3()
        video_detector.setModelPath(r"src\model.h5")
        video_detector.setJsonPath(r"src\model.json")
        video_detector.loadModel()

        def forFrame(_, output_array, __):
            for eachObject in output_array:
                classid.append(eachObject["name"])
                percentage.append(eachObject["percentage_probability"])

        video_detector.detectObjectsFromVideo(
            camera_input=camera,
            output_file_path=output_name,
            per_frame_function=forFrame,
            minimum_percentage_probability=self.THRESHOLD,
            frames_per_second=10,
            log_progress=True,
            # For testing purposes
            detection_timeout=10
            )

        # Create CSV File
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            #columns name
            writer.writerow(["CLASS", "PERCENTAGE"])
            for (classid_x, percentage_x) in zip (classid, percentage):
                writer.writerow([classid_x, percentage_x])

        self.popup("webcam", output_name+".avi", csv_file)


    @pyqtSlot(QListWidgetItem)
    def popup(self, type, filename, csv):
        popupWindow = PopupMessage(f"Mask Detection Using {type.capitalize()}", type, f"{type.capitalize()} Detection Done!", filename, csv,  self)
        popupWindow.show()

class PopupMessage(QDialog):

    def __init__(self, name, type, message, file, csv, parent=None):
        super().__init__(parent)
        self.name = name
        self.setWindowTitle(name)
        self.WINDOWSIZE = QSize(266, 140)

        self.setFixedSize(self.WINDOWSIZE)
        
        icons = {
            "image" : r"images\image.png",
            "video" : r"images\video.png",
            "webcam" : r"images\webcam.png"
        }

        self.setWindowIcon(QIcon(icons[type]))

        # Set background image
        oImage = QImage(r"images\background.png")
        sImage = oImage.scaled(self.WINDOWSIZE)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        icon = QLabel(self)
        icon.setPixmap(QtGui.QPixmap(r"images\done.png"))
        icon.setScaledContents(True)
        icon.setGeometry(108, 20, 50, 50)

        label = QLabel(self)
        label.setText(message)
        label.setFont(QFont("Zen Kurenaido", 10))
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setGeometry(58, 60, 150, 50)

        # Button to open the output file (image / video)
        fileIcon = QtGui.QIcon()
        fileIcon.addPixmap(QtGui.QPixmap(r"images\open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        filebtn = QPushButton(self)
        filebtn.setGeometry(210, 100, 25, 25)
        filebtn.setIcon(fileIcon)
        filebtn.setIconSize(QtCore.QSize(25, 25))
        filebtn.setFlat(True)
        filebtn.clicked.connect(lambda : os.startfile(file))

        # Button to open the output CSV file
        csvIcon = QtGui.QIcon()
        csvIcon.addPixmap(QtGui.QPixmap(r"images\csv.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        csvbtn = QPushButton(self)
        csvbtn.setGeometry(175, 100, 25, 25)
        csvbtn.setIcon(csvIcon)
        csvbtn.setIconSize(QtCore.QSize(25, 25))
        csvbtn.setFlat(True)
        csvbtn.clicked.connect(lambda : os.startfile(csv))

def main():
    app = QApplication(sys.argv)
    mainWindow = Window()
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
