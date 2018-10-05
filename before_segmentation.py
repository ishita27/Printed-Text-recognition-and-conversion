import cv2
import numpy as np

def image_for_detection(raw_image):

	#remove tiny noises by blurring
	sm_image = cv2.GaussianBlur(raw_image,(5,5),0)
	
	#binarize
	ret, bw_image = cv2.threshold(sm_image,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	
	#dilate
	kernel = np.ones((2,2),np.uint8)
	bw_image = cv2.dilate(bw_image,kernel)
	
	return bw_image
	
def image_for_extraction(raw_image):
	
	raw_image = cv2.GaussianBlur(raw_image,(3,3),0)
	
	ret,no_sm_bw_image = cv2.threshold(raw_image,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	
	return no_sm_bw_image
	
def getTransformationMatrix(img):
	#input should be a binarized image - text white, bg black
	
	#Find all white pixels
	pts = np.empty([0,0])
	pts = cv2.findNonZero(img)

	#Get rotated rect of white pixels
	rect = cv2.minAreaRect(pts)
	
	# rect[0] has the center of rectangle, rect[1] has width and height, rect[2] has the angle
	# To draw the rotated box and save the png image, uncomment below
	drawrect = img.copy()
	drawrect = cv2.cvtColor(drawrect, cv2.COLOR_GRAY2BGR)
	box = cv2.boxPoints(rect)
	box = np.int0(box) # box now has four vertices of rotated rectangle
	cv2.drawContours(drawrect,[box],0,(0,0,255),10)
	cv2.imwrite('rotated_rect.png', drawrect)

	#Change rotation angle if the tilt is in another direction
	rect = list(rect)
	if (rect[1][0] < rect[1][1]): # rect.size.width > rect.size.height
		temp = list(rect[1])
		temp[0], temp[1] = temp[1], temp[0]
		rect[1] = tuple(temp)
		rect[2] = rect[2] + 90.0

	#convert rect back to numpy/tuple
	rect = np.asarray(rect)
	
	#Rotate the image according to the found angle
	rotated_image = np.empty([0,0])
	M = cv2.getRotationMatrix2D(rect[0], rect[2], 1.0)
	#img = cv2.warpAffine(img, M, (img.shape[1],img.shape[0]))

	#returns the transformation matrix for this rotation
	return M

def rotate(image, M):
	return cv2.warpAffine(image, M, (image.shape[1],image.shape[0]))
