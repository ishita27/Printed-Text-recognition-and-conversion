import cv2
import numpy as np

from before_segmentation import image_for_detection
from before_segmentation import image_for_extraction
from before_segmentation import getTransformationMatrix
from before_segmentation import rotate


from functions_lines import findLines
from functions_lines import get_lines_threshold

from functions_words import findSpaces
from functions_words import get_spaces_threshold


def get_words(raw_image):
	
	#Returns a list/array of all the words found along with the number of words on each line.
	
	#preprocessing of the image
	
	#img_for_det used for detecting the character and lines boundaries
	img_for_det = image_for_detection(raw_image)
	
	#img_for_ext used for the actual extraction of the characters
	img_for_ext = image_for_extraction(raw_image)
	
	#get the rotated angle of the tilt
	M = getTransformationMatrix(img_for_det) # M is transformation matrix
	#rotate the iamge with M
	img_for_det = rotate(img_for_det,M)
	#rotate image that will be used for extraction too
	img_for_ext = rotate(img_for_ext,M)
	
	#for debugging purpose, we also write the images to files
	cv2.imwrite('img_for_detection.png', img_for_det)
	cv2.imwrite('img_for_extraction.png', img_for_ext)

	#get threshold to determine how much gap should be considered as the line gap
	LinesThres = get_lines_threshold(40, img_for_det)
	ycoords = findLines(img_for_det, LinesThres)

	# save image with lines printed ==========
	img_with_lines = img_for_ext.copy()
	for i in ycoords:
		cv2.line(img_with_lines,(0,i),(img_with_lines.shape[1],i),255,1)
	cv2.imwrite('img_with_lines.png', img_with_lines)
	#==========

	### =========== lines detection finish - ===========================
	
	#calculate max_line_height on each line
	max_height_on_line = []
	for i in range ( 0, len(ycoords)-1 ): #iterate line
		
		line = img_for_ext[range(ycoords[i],ycoords[i+1])]

		# to find max_line_height of each line we find contours again in this line only
		_,contour0,__ = cv2.findContours(line.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		contours = [cv2.approxPolyDP(cnt,2,True) for cnt in contour0[0]]

		# === Extract Bounding Rectangles
		maxArea = 0
		rect=[]
		for ctr in contours:
			maxArea = max(maxArea,cv2.contourArea(ctr))

		areaRatio = 0.008

		for ctr in contours:
			if cv2.contourArea(ctr) > maxArea * areaRatio: 
				rect.append(cv2.boundingRect(cv2.approxPolyDP(ctr,1,True)))
		
		#Find max_line_height and width
		max_line_height = 0

		for i in rect:
			x = i[0]
			y = i[1]
			w = i[2]
			h = i[3]
			
			if(h>max_line_height):
				max_line_height = h
		
		max_height_on_line.append(max_line_height)
	
	### =========== space in a line detection begins ===================

	#get the threshold to determine how much gap should be considered as the space between the words
	threshold_space = get_spaces_threshold(ycoords, img_for_det)

	#split lines based on the ycoords of the detected lines
	#each line is put into the var 'line' and the words are found
	#based on the threshold_space value.

	words_on_line=[]
	all_words=[]
	count = 0
	number_of_words = 0

	for i in range ( 0, len(ycoords)-1 ): #iterate line

		line = img_for_det[range(ycoords[i],ycoords[i+1])]
		cv2.imwrite('img/'+str(i)+'.png', line)
		
		#finding the x-coordinates of the spaces
		xcoords = findSpaces(line, threshold_space)
		
		#print len(xcoords)
		for x in xcoords:
			cv2.line(line, (x,0), (x,line.shape[0]), 255, 1)
		cv2.imwrite('img/'+str(i)+'.png', line)
		
		count = 0
		
		for j in range (0, len(xcoords)-1 ): #iterate words
			
			#use image with no smoothing
			line = img_for_ext[range(ycoords[i],ycoords[i+1])]
			
			word = line[:, xcoords[j]: xcoords[j+1]]
			all_words.append(word)
			cv2.imwrite('img/words/'+str(number_of_words)+'.png', word)
			
			count = count + 1
			number_of_words = number_of_words + 1
			#Generate space here
		
		words_on_line.append(count)
		# Line Change
	
	return all_words, words_on_line, max_height_on_line
