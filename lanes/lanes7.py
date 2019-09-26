#find the average left and right lane lines for greater clarity

import cv2
import numpy as np

def avg_slope_intercept(image,lines):
	left_fit = []
	right_fit = []
	for line in lines:
		x1,y1,x2,y2=line.reshape(4)
		parameters = np.polyfit((x1,x2),(y1,y2),1)
		slope = parameters[0]
		intercept = parameters[1]
		if slope < 0: #remember that y is plotted downwards
			left_fit.append((slope,intercept))
		else:
			right_fit.append((slope,intercept))
	left_fit_average=np.average(left_fit,axis=0) #you want to average along vertical
	right_fit_average=np.average(right_fit,axis=0)
	print("left",left_fit_average)
	print("right",right_fit_average)

def to_canny(image):
	gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY) 
	blur = cv2.GaussianBlur(gray,(5,5),0) #3rd Value is the standard deviation
	canny =cv2.Canny(blur,50,150)
	return canny

def display_lines(img,lines):
	# line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
	line_img=np.zeros_like(img)
	for line in lines:
		for x1,y1,x2,y2 in line:
			cv2.line(line_img, (x1, y1), (x2, y2), [255, 0, 0], 10)
	return line_img

def region_of_interest(image):
	height=image.shape[0] 
	triangle=[np.array([[200,height],[1100,height],[550,250]],dtype=np.int32)]
	mask = np.zeros_like(image) #same shape for mask and image #mask is a black image
	cv2.fillPoly(mask,triangle,255) #that triangle will be white
	masked_image = cv2.bitwise_and(image,mask)
	return masked_image


image = cv2.imread('test_image.jpg')
lane_image = np.copy(image)
canny = to_canny(lane_image)
cropped_image=region_of_interest(canny)
lines = cv2.HoughLinesP(cropped_image,2,np.pi/180, 100, np.array([]), minLineLength=40,maxLineGap=4)
averaged_lines=avg_slope_intercept(lane_image,lines)
line_image=display_lines(lane_image,lines)
blended_image = cv2.addWeighted(lane_image,0.6,line_image,1.5,1)
# cv2.imshow("region",blended_image)
cv2.waitKey(0)