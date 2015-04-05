import sys
from PIL import Image

filename = sys.argv[1]
number = int(sys.argv[2])
original = Image.open(filename)
width, height = original.size
step = width // number
top = 0
bottom = height
for i in range(0,number):
  left = 1+step*i
  right = 1+step*(i+1)
  new_crop = original.crop((left,top,right,bottom))
  new_crop.save('img'+str(i)+'.png')