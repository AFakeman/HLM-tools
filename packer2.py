import sys
import os
import struct

def readInt32(file):
    return int(struct.unpack('<i',file.read(4))[0])

def readInt64(file):
    return int(struct.unpack('<q',file.read(8))[0])

def readString(file, length):
    return file.read(length).decode('ASCII')

def readByte(file):
    return file.read(1)

def writeInt32(file, int):
    file.write(struct.pack('<i',int))

def writeInt64(file, int):
    file.write(struct.pack('<q',int))

def writeString(file, str):
    file.write(str)

def writeByte(file, byte):
    file.write(byte)

def main(filename, inputDir):
    if os.path.exists(filename):
        os.remove(filename)
    wadFile = open(filename, 'ab')
    files = []
    os.chdir(inputDir)
    local_offset = 0
    for subdir, _, files_iter in os.walk(os.getcwd()):
        for file_name in files_iter:
            file = {}
            file['name'] = os.path.relpath(os.path.join(subdir, file_name), os.getcwd())
            file['length'] = os.path.getsize(file['name'])
            file['offset'] = local_offset
            if (file['length']>0)and(file_name != '.DS_Store'):
                local_offset += file['length']
                files.append(file)
    writeInt32(wadFile, len(files))
    for file in files:
        writeInt32(wadFile, len(file['name']))
        writeString(wadFile, file['name'])
        writeInt64(wadFile, file['length'])
        writeInt64(wadFile, file['offset'])

    for file in files:
        real_file = open(file['name'],'rb')
        content = real_file.read()
        wadFile.write(content)
        real_file.close()
    wadFile.close()

if len(sys.argv) == 3:
    filename = sys.argv[1]
    inputDir = sys.argv[2]
else:
    filename = raw_input("Filename: ")
    inputDir = raw_input("Output directory: ")
main(filename, inputDir)