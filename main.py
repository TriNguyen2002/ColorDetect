# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Hust_project.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QTimer
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import color_detect as cd
import mask


class VideoThread(QThread):
    change_pixmap_signal_video = pyqtSignal(np.ndarray)
    change_pixmap_signal_img  = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self._run_flag = False
        self._cap_flag = False
    def stop(self): 
        self._run_flag = True

    def capture(self):
        self._cap_flag = True
    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(1)
        while True:
            ret, cv_img = cap.read()
            hsv = cv2.cvtColor(cv_img,cv2.COLOR_BGR2HSV)
            red = mask.rmask(hsv)
            green = mask.gmask(hsv)
            yellow = mask.ymask(hsv)
            self.r = cd.getContour(red, cv_img,(0,0,255),"red")
            self.g = cd.getContour(green, cv_img,(0,255,0),"green")
            self.y = cd.getContour(yellow, cv_img,(0,255,255),"yellow")
            if ret:
                self.change_pixmap_signal_video.emit(cv_img)             
            if self._cap_flag:
                cv2.imwrite("Resources/result.jpg",cv_img)
                pic = cv2.imread("Resources/result.jpg")
                self.change_pixmap_signal_img.emit(pic)
                self._cap_flag = False
            if self._run_flag :
                self._run_flag = False
                break
        cap.release()




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        font = QtGui.QFont()
        font.setPointSize(16)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: rgb(177, 195, 200);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(80, 440, 293, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.startButton.setStyleSheet("background-color: rgb(255, 120, 120);")
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        self.startButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.startButton_2.setStyleSheet("background-color: rgb(255, 120, 120);")
        self.startButton_2.setObjectName("startButton_2")
        self.horizontalLayout.addWidget(self.startButton_2)
        self.saveButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.saveButton.setStyleSheet("background-color: rgb(255, 120, 120);")
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.stopButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.stopButton.setStyleSheet("background-color: rgb(255, 120, 120);")
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setGeometry(QtCore.QRect(600, 430, 591, 101))
        self.info_label.setStyleSheet("color :rgb(0, 0, 0);\n"
                                        "background-color:rgb(255, 255, 255); font-size :24px")
        self.info_label.setText(" ")
        self.info_label.setScaledContents(True)
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_label.setObjectName("info_label")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(6, -1, 1191, 421))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.camera_label = QtWidgets.QLabel(self.widget)
        self.camera_label.setStyleSheet("background-color: rgb(91, 96, 127);")
        self.camera_label.setText("")
        self.camera_label.setObjectName("camera_label")
        self.horizontalLayout_2.addWidget(self.camera_label)
        self.result_label = QtWidgets.QLabel(self.widget)
        self.result_label.setStyleSheet("background-color: rgb(91, 96, 127);")
        self.result_label.setText("")
        self.result_label.setObjectName("result_label")
        self.horizontalLayout_2.addWidget(self.result_label)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.thread1 = VideoThread()
        self.thread1.change_pixmap_signal_video.connect(self.update_video)
        self.thread1.change_pixmap_signal_img.connect(self.show_picture)

        self.retranslateUi(MainWindow)

        # start the video
        self.startButton.clicked.connect(self.thread1.start)
        # Stop the camera
        self.timer = QTimer(MainWindow)
        self.timer.timeout.connect(self.update)

        self.stopButton.clicked.connect(self.thread1.stop) 
        self.startButton_2.clicked.connect(self.update) 
        self.stopButton.clicked.connect(self.info_label.clear) # type: ignore
        self.saveButton.clicked.connect(self.thread1.capture) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def update(self):
            if self.thread1.r == "red":
                self.info_label.setText("red")
            if self.thread1.g == "green":
                self.info_label.setText("green")       
            if self.thread1.y == "yellow":
                self.info_label.setText("yellow")   
            self.timer.start(30)
            
    def show_picture(self,img):
        qt_img = self.convert_cv_qt(img)
        self.result_label.setPixmap(qt_img)
    def update_video(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.camera_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(761, 421, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.saveButton.setText(_translate("MainWindow", "Take Picture"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.startButton_2.setText(_translate("MainWindow", "Update"))


import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
