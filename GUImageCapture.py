import sys
import numpy as np

#  RUN THIS IN CMD IN THE PARENT FOLDER TO MAKE THE .PY FILE pyuic5 -m untitled.ui -o untitled.py

import cv2
from PyQt5 import QtCore
from PyQt5.QtCore  import pyqtSlot
import subprocess
from PyQt5.QtGui import QImage , QPixmap
from PyQt5.QtWidgets import QDialog , QApplication
from PyQt5.uic import loadUi
import numpy as np
from matplotlib import pyplot as plt

class werun(QDialog):
	def __init__(self):
		super(werun,self).__init__()
		loadUi("untitled2.ui",self)
		
		self.logic = 0
		self.value = 0
		self.SHOW.clicked.connect(self.onClicked)
		self.TEXT.setText("Kindly Press 'Connect Webcam' to connect with webcam.")
		self.CAPTURE.clicked.connect(self.CaptureClicked)
		

	@pyqtSlot()
	def onClicked(self):
		self.TEXT.setText('Kindly Press "Capture Image" to take input')
		cap =cv2.VideoCapture(0)
		#while (True):
		#print(cap.read())
		while(cap.isOpened()):
			ret, frame=cap.read()

			if ret==True:
				
				print('here')
				self.displayImage(frame,1)
				cv2.waitKey()
				if (self.logic==2):
					self.value=self.value+1
					


					cv2.imwrite('C:/Users/gurpr/OneDrive/Desktop/venv/inputs/%s.png'%(self.value),frame)
					img_bgr: np.array = cv2.imread('C:/Users/gurpr/OneDrive/Desktop/venv/inputs/%s.png'%(self.value), cv2.IMREAD_COLOR)
					img_rgb: np.array = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
					img_gray: np.array = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
					
					blurred_img = cv2.blur(img_rgb,(4,4)) 
					
					img_gray: np.array = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)
# --
					gauss_blur_mask = np.array([[0,0,0,0,0,0,0],
                            [0,0,0.01,0.01,0.01,0,0],
                            [0,0.01,0.05,0.11,0.05,0.01,0],
                            [0,0.01,0.11,0.25,0.11,0.01,0],
                            [0,0.01,0.05,0.11,0.05,0.01,0],
                            [0,0,0.01,0.01,0.01,0,0],
                            [0,0,0,0,0,0,0],])*1.02
					
					img_gray = cv2.filter2D(img_gray, -1, gauss_blur_mask)
# --
					# Y- KERNEL
					mask_y = np.array([[ -0.5, -1, -0.5], [ 0, 0, 0], [ 0.5, 1, 0.5]])
					# X- KERNEL
					mask_x = np.array([[-0.5, 0, 0.5],[-1,0,1],[-0.5, 0, 0.5]])
					

					after_ymask_filter = cv2.filter2D(img_gray, -1, mask_y)

					after_xmask_filter = cv2.filter2D(img_gray, -1, mask_x)

					frame = ((after_xmask_filter)**2+(after_ymask_filter)**2)**0.5
					
					# cv2.imwrite('C:/Users/gurpr/OneDrive/Desktop/venv/outputs/%s.jpeg'%(self.value),frame)
					plt.imsave('C:/Users/gurpr/OneDrive/Desktop/venv/outputs/%s.jpeg'%(self.value),frame, cmap = 'gray')
					self.TEXT.setText("Edges extracted! File is saved in the Out folder \n Original File saved in In folder ")
					self.logic= 1
			else:
				print('not found')
		cap.release()
		cv2.destroyAllWindows()
	def CaptureClicked(self):
		self.logic=2
	def detectClicked(self):
		self.logic= 9
	
	# make file selection logic 
	
	# pass filepath as argument to image save folder 

	def displayImage(self,img,window=1):
		qformat=QImage.Format_Indexed8
		if len(img.shape)==3:
			if(img.shape[2])==4:
				qformat=QImage.Format_RGBA888
			else:
				qformat=QImage.Format_RGB888
		img = QImage(img,img.shape[1],img.shape[0],qformat)
		img = img.rgbSwapped()
		self.imgLabel.setPixmap(QPixmap.fromImage(img))
		self.imgLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

		


app =  QApplication(sys.argv)
window=werun()
window.show()
try:
	sys.exit(app.exec_())
except:
	print('excitng')
