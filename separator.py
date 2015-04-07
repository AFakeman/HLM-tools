import sys
import os
import struct

from PIL import Image

def read_int32(file):
    return int(struct.unpack('<i',file.read(4))[0])

def read_int64(file):
    return int(struct.unpack('<q',file.read(8))[0])

def read_string(file, length):
    return file.read(length).decode('ASCII')

def read_byte(file):
    return int(struct.unpack('<b',file.read(1))[0])

def write_int32(file, int):
    file.write(struct.pack('<i',int))

def write_int64(file, int):
    file.write(struct.pack('<q',int))

def write_string(file, str):
    file.write(str)

def create_directories(name):
    if not os.path.exists(name):
        os.makedirs(name)

name = sys.argv[1]
output_directory = sys.argv[2]
img = Image.open(name+'.png')
pixels = img.load()
file = open(name+'.meta','rb')
length = os.stat(name+'.meta').st_size
file.seek(28)
create_directories(output_directory)
os.chdir(output_directory)
while file.tell()<length:
    name_length = read_byte(file)
    name = read_string(file,name_length)
    sprites = read_int32(file)
    for i in range(sprites):
        size_x = read_int32(file)
        size_y = read_int32(file)
        pos_x = read_int32(file)
        pos_y = read_int32(file)
        file.read(16)
        new_crop = img.crop((pos_x, pos_y, pos_x+size_x, pos_y+size_y))
        new_crop.save("{name}_{number}.png".format(name=name, number=i))
    #os.system('convert -delay 10 -dispose previous -loop 0 {name}*.png {name}.gif'.format(name=name))
    #os.system('rm {name}*.png'.format(name=name))