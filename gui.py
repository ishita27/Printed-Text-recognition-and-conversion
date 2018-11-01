#Starting point of the program.

import sys
from PyQt4 import QtGui, QtCore
from PyQt4 import *
import cv2
from PIL import Image
from ocr import perform_ocr
import gtts as gTTS
from PyQt4.QtGui import QMessageBox
import os
import time
from PyQt4.QtCore import QObject, pyqtSignal
from text2speech import textPlay

class Window(QtGui.QMainWindow):

	upload_complete_signal = QtCore.pyqtSignal()
	loc_qlabel_signal = QtCore.pyqtSignal()
	img_crop_signal = QtCore.pyqtSignal()
	extract_start_signal = QtCore.pyqtSignal()
	extract_complete_signal = QtCore.pyqtSignal()
	original_width = 0
	original_height = 0
	is_crop = False
	boundary_xy = (0, 0, 0, 0)
	location_name = "Unknown"

	def __init__(self):
		super(Window, self).__init__()
		self.setStyleSheet("background-color: rgb(33,33,33);")
		self.setGeometry(50, 50, 1128, 554)
		self.setWindowTitle("Optical Character Recognintion")
		self.setWindowIcon(QtGui.QIcon("progicon.png"))
		#QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("windows"))

		#============================Menu Bar=============================================
		extractAction = QtGui.QAction("&Exit program",self)
		extractAction.setShortcut("Ctrl+Q")
		extractAction.setStatusTip("Quit Program")
		extractAction.triggered.connect(self.close_app)

		self.statusBar()

		mainMenu = self.menuBar()

		fileMenu = mainMenu.addMenu("&Home")
		fileMenu.addAction(extractAction)

		popup = QtGui.QAction("&How it works?",self)
		editMenu = mainMenu.addMenu("&Help")
		editMenu.addAction(popup)

		self.lbl3 = QtGui.QLabel("Sketch pad",self)
		pic = QtGui.QLabel(self.lbl3)
		pic.setPixmap(QtGui.QPixmap("file_upload.png"))
		pic.show()
		self.lbl3.move(96,46)
		self.lbl3.setGeometry(QtCore.QRect(100, 46, 700, 480))
		self.lbl3.setScaledContents(True)
		#self.SketchPad.resize(250,80)
		#self.SketchPad.move(0,220)

		mainMenu.setStyleSheet("""QMenuBar {
                                background-color: rgb(0,0,0);
                                }
                        QMenuBar::item {
                                background-color: rgb(0,0,0);
                                color: rgb(255,255,255);
                                }

                        QMenuBar::item::selected {
                                background-color: orange;
                                }""")





		self.home()

	def home(self):

	#Quit Button Right
		quitbtn = QtGui.QPushButton("Quit",self)
		quitbtn.clicked.connect(self.close_app)
		quitbtn.setStatusTip("Quit Program")
		quitbtn.resize(quitbtn.sizeHint())
		quitbtn.setStyleSheet("background-color: orange;border-radius: 15px; border-color: orange;padding: 20px; border-top: 10px transparent;border-bottom: 10px transparent;border-right: 10px transparent;border-left: 10px transparent;");
		#quitbtn.move(100, 100)


	#Select Image
		loadimgbtn = QtGui.QPushButton("Load image",self)
		loadimgbtn.clicked.connect(self.load_image)
		loadimgbtn.setStatusTip("Browse for image")
		loadimgbtn.resize(loadimgbtn.sizeHint())
		loadimgbtn.setStyleSheet("background-color: orange;border-radius: 15px; border-color: orange;padding: 20px; border-top: 10px transparent;border-bottom: 10px transparent;border-right: 10px transparent;border-left: 10px transparent;");
		#quitbtn.move(100, 100)


	#Extract Image
		extracttxtbtn = QtGui.QPushButton("Extract text",self)

		extracttxtbtn.setStatusTip("Extract image from text")
		extracttxtbtn.resize(extracttxtbtn.sizeHint())
		extracttxtbtn.setEnabled(False);
		extracttxtbtn.clicked.connect(self.emitSignal)
		# extracttxtbtn.clicked.connect(onClick)
		self.upload_complete_signal.connect(lambda: extracttxtbtn.setEnabled(True))
		#QtCore.QCoreApplication.processEvents()
		extracttxtbtn.clicked.connect(self.extract_text)
		extracttxtbtn.setStyleSheet("background-color: orange;border-radius: 15px; border-color: orange;padding: 20px; border-top: 10px transparent;border-bottom: 10px transparent;border-right: 10px transparent;border-left: 10px transparent;");

		#quitbtn.move(100, 100)


	#Play Text
		cropimgbtn = QtGui.QPushButton("Play Text",self)
		cropimgbtn.clicked.connect(self.playText)
		cropimgbtn.setStatusTip("Browse for image")
		cropimgbtn.setEnabled(False);
		self.extract_complete_signal.connect(lambda: cropimgbtn.setEnabled(True))

		cropimgbtn.resize(cropimgbtn.sizeHint())
		cropimgbtn.setStyleSheet("background-color: orange;border-radius: 15px; border-color: orange;padding: 20px; border-top: 10px transparent;border-bottom: 10px transparent;border-right: 10px transparent;border-left: 10px transparent;");
		#quitbtn.move(100, 100)

	#File location QLabel
		loc_qlabel = QtGui.QLabel(self)
		loc_qlabel.hide()
		[self.loc_qlabel_signal.connect(x) for x in [lambda: loc_qlabel.setText(self.location_name), lambda: loc_qlabel.show()]]
		loc_qlabel.move(925,150)
		#self.loc_qlabel_signal.connect(lambda: loc_qlabel.show())
		loc_qlabel.setStyleSheet("QLabel {  color : white; }");

	#Crop boundary QLabel
		img_bound_qlabel = QtGui.QLabel(self)
		img_bound_qlabel.hide()
		#myString = ",".join(str(v) for v in self.boundary_xy)
		#[self.extract_start_signal.connect(x) for x in [lambda: img_bound_qlabel.setText("Extracting..."),lambda: img_bound_qlabel.show()]]
		img_bound_qlabel.move(925,248)
		img_bound_qlabel.setStyleSheet("QLabel { color : white; }");
		[self.extract_complete_signal.connect(x) for x in [lambda: img_bound_qlabel.setText("Done"),lambda: img_bound_qlabel.show()]]


	#Vertical Box Right
		v_but_box = QtGui.QVBoxLayout()
		v_but_box.addWidget(loadimgbtn)
		v_but_box.addWidget(extracttxtbtn)
		v_but_box.addWidget(cropimgbtn)
		v_but_box.addWidget(quitbtn)

		v_but_box.setGeometry(QtCore.QRect(900,46,150,450))


	#Insert OCR image
		#pic = QtGui.QLabel(self)
		#pic.setGeometry(200, 22, 800, 100)
		#use full ABSOLUTE path to the image, not relative
		#pic.setPixmap(QtGui.QPixmap("nn2.png"))



		self.show()


	# def onClick(checked):
	#     print( checked #<- only used if the button is checkeable)

	def playText(self):
		textPlay()



	def close_app(self):
		#choice = QtGui.QMessageBox.question(self,"Exit","Are you sure you want to quit?",QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		choice = QtGui.QMessageBox()
		choice.setText('Are you sure you want to quit?')
		#choice = QtGui.QMessageBox.question(self,"Exit","Are you sure you want to quit?")
		a=QtGui.QPushButton('Yes')
		a.setStyleSheet("background-color: orange;border-radius: 15px; border-color: orange;padding: 20px; border-top: 10px transparent;border-bottom: 10px transparent;border-right: 10px transparent;border-left: 10px transparent;");
		choice.addButton(a, QtGui.QMessageBox.YesRole)
		b=QtGui.QPushButton('No')
		b.setStyleSheet("background-color: orange;border-radius: 15px; border-color: orange;padding: 20px; border-top: 10px transparent;border-bottom: 10px transparent;border-right: 10px transparent;border-left: 10px transparent;");
		choice.addButton(b, QtGui.QMessageBox.NoRole)
		choice.setStyleSheet("background-color: rgb(189,189,189);""font:Comic Sans MS")
		ret = choice.exec_()

		if QtGui.QMessageBox.Yes:
			print("Program Quit!!")
			sys.exit()
		else:
			pass
			#print "This is the end"
			#sys.exit()

	def emitSignal(self):
		self.extract_start_signal.emit()
		print('Signal emitted')
	def extract_text(self):
		if self.is_crop == False:
			self.extract_message()


	def extract_message(self):
		perform_ocr("original_img.jpg")
		print (self.boundary_xy)
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Text file saved")
		msg.setWindowTitle("Information")
		#msg.setStandardButtons(QMessageBox.Ok)
		a=QtGui.QPushButton('Ok')
		a.setStyleSheet("background-color: orange;border-radius: 15px; border-color: orange;padding-left: 20px;padding-right: 20px;padding-top: 10px;padding-bottom: 10px; border-top: 10px transparent;border-bottom: 10px transparent;border-right: 10px transparent;border-left: 20px transparent;");
		msg.addButton(a,QtGui.QMessageBox.YesRole)
		msg.setStyleSheet("background-color: rgb(189,189,189);")
		#msg.buttonClicked.connect(msgbtn)
		retval = msg.exec_()
		self.extract_complete_signal.emit()
		#os.startfile("output.txt")
		#w = QWidget()
		#QMessageBox.information(w, "Message", "Text file saved ")



	def load_image(self):


		name = QtGui.QFileDialog.getOpenFileName(self,"Select image","C:\\","Image files (*.jpg *.gif *.png)")
		self.location_name = name
		self.loc_qlabel_signal.emit()
		input_img = cv2.imread(str(name))
		#input_img = cv2.cvtColor(input_img, cv2.cv.CV_BGR2RGB)
		cv2.imwrite("original_img.jpg",input_img)
		#cv2.imshow('image',input_img)
		#cv2.waitKey(0)
		print ("Image Load Complete........")
		self.store_orgimg_data(input_img.shape)
		self.is_crop = False
		self.upload_complete_signal.emit()

		'''img = 'original_img.jpg'
		im1 = Image.open('original_img.jpg')
		img2 = im1.resize((600, 434), Image.ANTIALIAS)
		img2.save('original_img2.jpg')

		QtGui.QMainWindow.lbl3 = QtGui.QLabel("Sketch pad",QtGui.QMainWindow)
		pic = QtGui.QLabel(QtGui.QMainWindow.lbl3)
		pic.setPixmap(QtGui.QPixmap("original_img2.jpg"))
		pic.show()
		QtGui.QMainWindow.lbl3.move(96,46)
		QtGui.QMainWindow.lbl3.setGeometry(QtCore.QRect(100, 46, 700, 480))
		QtGui.QMainWindow.lbl3.setScaledContents(True)
		#self.SketchPad.resize(250,80)
		#self.SketchPad.move(0,220)'''

		input_image = cv2.imread('original_img.jpg')
		height,width,channels = input_image.shape
		bytesPerLine = channels * width
		qImg = QtGui.QImage(input_image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
		pixmap01 = QtGui.QPixmap.fromImage(qImg)
		pixmap_image = QtGui.QPixmap(pixmap01)
		label_imageDisplay = QtGui.QLabel(self)
		label_imageDisplay.setPixmap(pixmap_image)
		label_imageDisplay.setAlignment(QtCore.Qt.AlignCenter)
		label_imageDisplay.setScaledContents(True)
		label_imageDisplay.setMinimumSize(1,1)
		label_imageDisplay.setGeometry(QtCore.QRect(100, 46, 700, 480))
		label_imageDisplay.show()


		# resized_img = self.resizeimg(input_img,1024,576)
		# cv2.imwrite("to_crop.jpg",resized_img)
		#
		# res_height, res_width = resized_img.shape[0], resized_img.shape[1]
		# #qImg = QtGui.QImage(resized_img.data, res_width, res_height, res_width*3, QtGui.QImage.Format_RGB888)
		# qImg = QtGui.QImage(cv2.cvtColor(resized_img, cv2.BGR2RGB), res_width, res_height, res_width*3, QtGui.QImage.Format_RGB888)
		# pix = QtGui.QPixmap(qImg)
		# inputimg_label = QtGui.QLabel(self)
		# inputimg_label = QtGui.QLabel(self)
		# inputimg_label.setGeometry(20, 120, 1024, 576)#900,46,150,450
		# inputimg_label.setPixmap(pix)
		#
		#
		#
		# #inputimg_label.clear()
		#
		# #file = open(name,'r')
		# #print name
		# #input_img.setPixmap(QtGui.QPixmap(name))
		# inputimg_label.show()
		# self.upload_complete_signal.connect(inputimg_label.hide)


	#============openCV input picture resize to 1024 * 576 for display

	# def resizeimg(self,input_img,w,h):
	# 	#print "Hello"
	# 	o_height = input_img.shape[0]
	# 	o_width = input_img.shape[1]
	# 	aspect_ratio = o_width/(o_height*1.0)
	#
	# 	if(aspect_ratio < 1.777): # aspect ratio less than 16:9
	# 		#aspectRatio = o_width / (o_height*1.0)
	# 		height = h
	# 		width = int(height * aspect_ratio)
	# 		input_img = cv2.resize(input_img, (width,height))
	#
	# 	elif(aspect_ratio > 1.777): # aspect ratio more than 16:9
	#
	# 		#aspectRatio = o_height / (o_width*1.0)
	# 		width = w
	# 		height = int(width / aspect_ratio)
	# 		input_img = cv2.resize(input_img, (width,height))
	#
	# 	else: # aspect ratio exactly 16:9
	# 		input_img = cv2.resize(input_img, (h,h))
	# 	print (input_img.shape)
	# 	return input_img

	def store_orgimg_data(self, shape):
		self.original_height, self.original_width = shape[0], shape[1]
		self.boundary_xy = (0, 0, shape[1], shape[0])


	# def crop_image(self):
	# 	x1, y1, x2, y2, to_crop_width, to_crop_height = main_run()
	#
	# 	x1_final = x1*self.original_width/to_crop_width
	# 	y1_final = y1*self.original_height/to_crop_height
	# 	x2_final = x2*self.original_width/to_crop_width
	# 	y2_final = y2*self.original_height/to_crop_height
	#
	# 	self.store_crop_coordinates(x1_final, y1_final, x2_final, y2_final)

	def store_crop_coordinates(self,x1, y1, x2, y2):

		self.boundary_xy = (x1, y1, x2, y2)
		#print self.boundary_xy
		#im1 = Image.open('original_img.jpg')
		im1 = Image.open('original_img.jpg')
		box = (x1,y1,x2,y2)
		im1 = im1.crop(box)
		im1.save("original_cropped.jpg")
		print ("Image Crop Complete........")
		self.img_crop_signal.emit()
		self.is_crop = True



def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())


run()
