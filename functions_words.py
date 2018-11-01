import cv2
import numpy as np

def findSpaces(line, thres_space):
	
	# making vertical projections
	
	verProj = cv2.reduce(line, 0, cv2.REDUCE_AVG)

	# make hist - same dimension as horProj - if 0 (space), then True, else False
	th = 0; # black pixels threshold value. this represents the space lines
	hist = verProj <= th;

	#Get mean coordinate of white white pixels groups
	xcoords = []
	x = 0
	count = 0
	isSpace = False

	for i in range(0, line.shape[1]):
		if (not isSpace):
			if (hist[0][i]): #if space is detected, get the first starting x-coordinates and start count at 1
				isSpace = True
				count = 1
				x = i
		else:
			if (not hist[0][i]):
				isSpace = False
				#when smoothing, thin letters will breakdown, creating a new blank lines or pixel columns, but the count will be small, so we set a threshold.
				#print count,"\t",
				if (count > thres_space):
					xcoords.append(x // count)
			else:
				x = x + i
				count = count + 1
	

	xcoords.append(x // count)
	
	return xcoords

def SpacesMedian(line):
	
	# making vertical projections
	
	verProj = cv2.reduce(line, 0, cv2.REDUCE_AVG)

	# make hist - same dimension as horProj - if 0 (space), then True, else False
	th = 0; # black pixels threshold value. this represents the space lines
	hist = verProj <= th;

	#Get mean coordinate of white white pixels groups
	xcoords = []
	x = 0
	count = 0
	isSpace = False
	median_count = []
	for i in range(0, line.shape[1]):
		if (not isSpace):
			if (hist[0][i]): #if space is detected, get the first starting x-coordinates and start count at 1
				isSpace = True
				count = 1
				#x = i
		else:
			if (not hist[0][i]):
				isSpace = False
				#when smoothing, thin letters will breakdown, creating a new blank lines or pixel columns, but the count will be small, so we set a threshold.
				#print count,"\t",
				
				#append each count of rows of blank gaps found
				median_count.append(count)
				
				#if (count > 15):
					#xcoords.append(x / count)
			else:
				#x = x + i
				count = count + 1
	
	median_count.append(count)
	xcoords.append(x // count)
	
	#returns x-coordinates of the spaces found in the line
	return median_count
	
def get_spaces_threshold(ycoords, img_for_det) :

	## Find Median for setting threshold
	medianList = []
	for i in range ( 0, len(ycoords)-1 ):
		line = img_for_det[range(ycoords[i],ycoords[i+1])]
		medianList.append(SpacesMedian(line))
	
	#medianList contains count of each blank columns found in all lines
	#including spaces found between each characters too
	
	#find the row among medianList[] with maximum length
	max_len = len(medianList[0])
	max_in = 0 #for index number
	for i in range (0, len(medianList)):
		if max_len < len(medianList[i]):
			max_len = len(medianList[i])
			max_in = i

	#sort the row  having the maximum no. of elements (decending order)
	mList = sorted(medianList[max_in],reverse=True)
	
	#delete elements produced from the page's margin
	mList = np.delete(mList, [0,1,2])
	#print('mList',mList)
	
	firstItem = mList[0]
	for i in range (len(mList)-1, 0, -1):
		if mList[i] < firstItem/2:
			mList = np.delete(mList,i)

	mean = np.mean(mList)
	threshold_space = mean/2
	
	return threshold_space
