import sys
import os
import struct

def readInt32(file):
    return int(struct.unpack('<i',file.read(4))[0])

def readInt64(file):
    return int(struct.unpack('<q',file.read(8))[0])

def readString(file, length):
    return file.read(length).decode('ASCII')

if len(sys.argv) == 3:
    filename = sys.argv[1]
    outputDir = sys.argv[2]
else:
    filename = raw_input("Filename: ")
    outputDir = raw_input("Output directory: ")

if not os.path.exists(os.getcwd()+'/'+outputDir):
    os.makedirs(outputDir)
else:
    print('Directory already exists')

wadFile = open(filename, 'rb')
file_count = readInt32(wadFile)
print(file_count)
files = []

for i in range(0,file_count):
    file = {}
    nameLength = readInt32(wadFile)
    file['name'] = readString(wadFile,nameLength)
    file['length'] = readInt64(wadFile)
    file['offset'] = readInt64(wadFile)
    files.append(file)

os.chdir(outputDir)
    
for file in files:
    if not os.path.exists(os.getcwd()+'/'+os.path.dirname(file['name'])):
        os.makedirs(os.path.dirname(file['name']))
    outputFile = open(file['name'],'ab')
    outputFile.write(wadFile.read(file['length']))
    outputFile.close()
