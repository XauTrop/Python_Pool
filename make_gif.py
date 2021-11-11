import os
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import glob
import io

##Edit the frames adding text ##
frames = []
file_list = glob.glob(os.getcwd() + '\\images\\*.png') # Select folder and file extension
list.sort(file_list, key=lambda x: int(x.split('fig')[1].split('.png')[0])) # Sort the images by #, this may need to be tweaked for your use case
for f in file_list:
	print (f)
	image = Image.open(f).convert("RGBA")
	txt = Image.new('RGBA', image.size, (255,255,255,0))
	font = ImageFont.truetype("arial.ttf", 12)
	d = ImageDraw.Draw(txt)    
	d.text((610, 470), "by XXX", fill=(0, 0, 0, 255), font=font)
	combined = Image.alpha_composite(image, txt)
	combined.save(f)

for i in file_list:
	new_frame = Image.open(i)
	frames.append(new_frame)

##Save into a GIF file that loops forever
frames[0].save(os.getcwd() + '\\images\\png_to_gif.gif', format='GIF', #Change output gif name
		append_images=frames[1:],
		save_all=True,
		duration=500, loop=0)
