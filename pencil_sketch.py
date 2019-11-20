
import numpy as np
import cv2

def pencilSketch(img):
	# 1. convert to grayscale
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# 2. invert the grayscale image
	img_inv = 255 - img_gray
	# 3. apply gaussian blur
	img_blur = cv2.GaussianBlur(img_inv, (21, 21), 0, 0)
	# 4. blend the blurred image
	img_blend = cv2.divide(img_gray, 255 - img_blur, scale=256)
	# 5. blend the blended image with the original to get color
	#alpha = 0.8
	alpha = 1.0
	beta = 1.0 - alpha
	img_blend = cv2.cvtColor(img_blend,cv2.COLOR_GRAY2RGB)
	img_blend = cv2.addWeighted(img_blend, alpha, img, beta, 0.0)
	# 6. add a sketch book background
	img_bg = cv2.imread(background_path, 1)
	img_bg = cv2.resize(img_bg, (img_blend.shape[1], img_blend.shape[0]))
	img_canvas = cv2.multiply(img_blend, img_bg, scale = 1/256)
	return img_canvas

if __name__=='__main__':

	'''
	METHODS
	1 =
	2 =
	3 =
	4 =
	'''

	image_or_video_str = "\nImage or video?\n\t1 = image\n\t2 = video\n"
	img_or_vid = int(input(image_or_video_str))
	while img_or_vid not in range(1, 3):
		img_or_vid = int(input(image_or_video_str))

	if img_or_vid == 1:

		#specify the path to the image file
		path_select_str = "\nImage path:\n"
		img_path = input(path_select_str)
		#specify the path to the background image file
		background_path = 'img/background.jpg'
		#specify the path to which the new image is saved
		save_path = 'output.jpg'

		#load image
		img = cv2.imread(img_path, 1)

		method_select_str = "\nAvailable methods:\n\t1 = the proper way\n\t2 = pencilSketch() gray\n\t3 = pencilSketch() color\n\t4 = stylize\n\nMethod:\n"
		method = int(input(method_select_str))
		while method not in range(1, 5):
			method = int(input(method_select_str))

		if method == 1:
			img_to_save = pencilSketch(img)
		elif method == 2:
			sigma_s = 60
			sigma_r = 0.07
			shade_factor = 0.02
			img_gray, img_color = cv2.pencilSketch(img, sigma_s, sigma_r, shade_factor)
			img_to_save = img_gray
		elif method == 3:
			sigma_s = 60
			sigma_r = 0.07
			shade_factor = 0.02
			img_gray, img_color = cv2.pencilSketch(img, sigma_s, sigma_r, shade_factor)
			img_to_save = img_color
		elif method == 4:
			sigma_s = 60
			sigma_r = 0.07
			img_style = cv2.stylization(img, sigma_s, sigma_r)
			img_to_save = img_style

		#save image
		cv2.imwrite(save_path, img_to_save)

	elif img_or_vid == 2:

		#specify the path to the video file
		path_select_str = "\nVideo path:\n"
		video_path = input(path_select_str)
		#specify the path to the background image file
		background_path = 'img/background.jpg'
		#specify the path to which the new video is saved
		save_path = 'output.mp4'

		method_select_str = "\nAvailable methods:\n\t1 = the proper way\n\t2 = pencilSketch() gray\n\t3 = pencilSketch() color\n\t4 = stylize\n\nMethod:\n"
		method = int(input(method_select_str))
		while method not in range(1, 5):
			method = int(input(method_select_str))
		print()

		#load video
		cap = cv2.VideoCapture(video_path)

		if not cap.isOpened():
			print("\nCOULDN'T OPEN FILE\n")
			print("\nTERMINATING")

		resize_video = True
		fps = 5.0
		cap.set(cv2.CAP_PROP_FPS, fps)
		frame_width = int(cap.get(3))
		frame_height = int(cap.get(4))
		if resize_video:
			frame_width = 640
			frame_height = 360
		fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
		out = cv2.VideoWriter('output.avi',fourcc, fps, (frame_width, frame_height))

		length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
		counter = 0
		while cap.isOpened():
			ret, frame = cap.read()
			if ret:
				if resize_video:
					frame = cv2.resize(frame, (frame_width, frame_height))
				if method == 1:
					frame = pencilSketch(frame)
				elif method == 2:
					sigma_s = 60
					sigma_r = 0.07
					shade_factor = 0.02
					img_gray, img_color = cv2.pencilSketch(frame, sigma_s, sigma_r, shade_factor)
					frame = img_gray
				elif method == 3:
					sigma_s = 60
					sigma_r = 0.07
					shade_factor = 0.02
					img_gray, img_color = cv2.pencilSketch(frame, sigma_s, sigma_r, shade_factor)
					frame = img_color
				elif method == 4:
					sigma_s = 60
					sigma_r = 0.07
					img_style = cv2.stylization(frame, sigma_s, sigma_r)
					frame = img_style
				out.write(frame)
				counter += 1
				print("Progress:\t"+str(counter)+" / "+str(length), end="\r")
				#cv2.imshow('Frame',frame)
				#if cv2.waitKey(1) & 0xFF == ord('q'):
				#	break
			else:
				break

		cap.release()
		out.release()
		print()

	print("\nTERMINATING")
