
import numpy as np
import cv2

#specify the path to the image file
img_path = 'img/test.jpg'
#specify the path to the background image file
background_path = 'img/background.jpg'
#specify the path to which the new image is saved
save_path = 'test.jpg'

if __name__=='__main__':
	#load image
	img = cv2.imread(img_path, 1)

	#convert to pencil sketch
	sigma_s = 60
	sigma_r = 0.07
	shade_factor = 0.02
	#img_gray, img_color = cv2.pencilSketch(img, sigma_s, sigma_r, shade_factor)
	#stylize
	sigma_s = 60
	sigma_r = 0.45
	#img_style = cv2.stylization(img, sigma_s, sigma_r)

	# the proper way
	# 1. convert to grayscale
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# 2. invert the grayscale image
	img_inv = 255 - img_gray
	# 3. apply gaussian blur
	img_blur = cv2.GaussianBlur(img_inv, (21, 21), 0, 0)
	# 4. blend the blurred image
	img_blend = cv2.divide(img_gray, 255 - img_blur, scale=256)
	# 5. blend the blended image with the original to get color
	alpha = 0.8
	beta = 1.0 - alpha
	img_blend = cv2.cvtColor(img_blend,cv2.COLOR_GRAY2RGB)
	img_blend = cv2.addWeighted(img_blend, alpha, img, beta, 0.0)
	# 6. add a sketch book background
	img_bg = cv2.imread(background_path, 1)
	img_bg = cv2.resize(img_bg, (img_blend.shape[1], img_blend.shape[0]))
	img_canvas = cv2.multiply(img_blend, img_bg, scale = 1/256)

	#save image
	cv2.imwrite(save_path, img_canvas)
