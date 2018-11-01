import numpy as np
import cv2

def fix_i_j(rect, max_line_height, max_w):
	# ========== correct dots commas
	j = 0
	i_dot_list = []

	for i in rect:
		x = i[0]
		y = i[1]
		w = i[2]
		h = i[3]
		
		
		#if the dot of i is the last element in the rect, the [j+1] index will not work. so we put [j-1] separately here
		if  (j is len(rect)-1 and (h < max_line_height/3)):
			
			if( (h < max_line_height/3) and (abs(rect[j-1][0]+rect[j-1][2] - (x+w)) < max_w/3.5) ):
				#correct i
				#rect[j-1][3] = rect[j-1][3] + (rect[j-1][1] - y)
				rect[j-1] = (rect[j-1][0], rect[j-1][1], rect[j-1][2], rect[j-1][3] + (rect[j-1][1] - y))
				
				#rect[j-1][1] = y
				rect[j-1] = (rect[j-1][0], y, rect[j-1][2], rect[j-1][3])
				i_dot_list.append(j)
			
			elif (h < max_line_height/2.4 and y > (rect[j-1][1] + rect[j-1][3]/3)):
				#rect[j][1] = rect[j][1] - (max_line_height/2)
				rect[j] = [x,y-(max_line_height/2),w,h+(max_line_height/2)]
			
		
		#if the dot of i is not the last element in the rect
		else:
		
			if( (h < max_line_height/3) and (abs(rect[j+1][0]+rect[j+1][2] - (x+w)) < max_w/3.5)):
				#correct i
				#rect[j+1][3] = rect[j+1][3] + (rect[j+1][1] - y)
				rect[j+1] = (rect[j+1][0], rect[j+1][1], rect[j+1][2], rect[j+1][3] + (rect[j+1][1] - y))
				
				#rect[j+1][1] = y
				rect[j+1] = (rect[j+1][0], y, rect[j+1][2], rect[j+1][3])
				
				i_dot_list.append(j)
				
			elif( (h < max_line_height/3) and (abs(rect[j-1][0]+rect[j-1][2] - (x+w)) < max_w/3.5) ):
				#correct i
				#rect[j-1][3] = rect[j-1][3] + (rect[j-1][1] - y)
				rect[j-1] = (rect[j-1][0], rect[j-1][1], rect[j-1][2], rect[j-1][3] + (rect[j-1][1] - y))
				
				#rect[j-1][1] = y
				rect[j-1] = (rect[j-1][0], y, rect[j-1][2], rect[j-1][3])
				
				i_dot_list.append(j)
			
			elif (h < max_line_height/2.4 and y > (rect[j-1][1] + rect[j-1][3]/3)):
				#rect[j][1] = rect[j][1] - (max_line_height/2)
				rect[j] = [x,y-(max_line_height/2),w,h+(max_line_height/2)]
				
		j = j + 1
			
	# ===== end of fixing dots in i and j

	#delete the dots from rect array which belongs to i and j
	rect = np.delete(rect, i_dot_list, axis=0)
	# =======================
	
	return rect