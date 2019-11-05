

from moviepy.editor import VideoFileClip

def main():
	#initial data
	file_name = "test_pixelart"
	file_format = "mp4"
	new_file_appendix = "_gif"
	src = file_name + "." + file_format
	fps = "default"
	#open the video
	try:
		print("Opening video...")
		vid = VideoFileClip(src)
		duration = vid.duration	#duration
		if fps == "default":
			fps = vid.fps	#framerate
		print("Successful!\n")
	except Exception as e:
		print("Failed!")
		print("Error: " + str(e) + "\n")
		print("Program will terminate.")
		return	#end the program
	#save the video as a gif
	try:
		print("Saving video...")
		new_src = file_name + new_file_appendix + ".gif"
		vid.write_gif(new_src)
		print("Successful!\n")
	except Exception as e:
		print("Failed!")
		print("Error: " + str(e) + "\n")
		print("Program will terminate.")
		return	#end the program

main()
