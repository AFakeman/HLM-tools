import os
import sys
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

def create_directories(name):
    if not os.path.exists(name):
        os.makedirs(name)

def get_wad_metadata(file, version):
    if version == 1:
        global_offset = readInt32(file)
    else:
        global_offset = 0
    file_count = readInt32(file)
    files = []
    for i in range(file_count):
        file_obj = {}
        name_length = readInt32(file)
        file_obj['name'] = readString(file, name_length)
        if version == 1:
            file_obj['length'] = readInt32(file)
            file_obj['offset'] = readInt32(file)
        else:
            file_obj['length'] = readInt64(file)
            file_obj['offset'] = readInt64(file)
        files.append(file_obj)
    if not global_offset:
        global_offset = file.tell()
    return global_offset, files

def set_wad_metadata(file, version, offset, files):
    if version == 1:
        writeInt32(file, offset)
    writeInt32(file, len(files))
    for file_obj in files:
        writeInt32(file, len(file_obj['name']))
        writeString(file, file_obj['name'])
        if version == 1:
            writeInt32(file, file_obj['length'])
            writeInt32(file, file_obj['offset'])
        else:
            writeInt64(file, file_obj['length'])
            writeInt64(file, file_obj['offset'])

def copy_from_file(file, files, offset):
    for file_obj in files:
        file.seek(file_obj['offset']+offset)
        create_directories(os.path.split(file_obj['name'])[0])
        output_file = open(file_obj['name'],'wb')
        output_file.write(file.read(file_obj['length']))
        output_file.close()

def copy_to_file(file, files, offset):
    for file_obj in files:
        file.seek(file_obj['offset']+offset)
        input_file = open(file_obj['name'],'rb').read()
        file.write(input_file)

def create_metadata(directory,version):
    if version == 1:
        global_offset = 8
    else:
        global_offset = 4
    local_offset = 0
    files = []
    for subdir, _, files_iter in os.walk(os.getcwd()):
        for file_name in files_iter:
            file_obj = {}
            file_obj['name'] = os.path.relpath(os.path.join(subdir, file_name), os.getcwd())
            file_obj['length'] = os.path.getsize(file_obj['name'])
            file_obj['offset'] = local_offset
            if (file_obj['length']>0)and(file_name != '.DS_Store'):
                local_offset += file_obj['length']
                if version == 1:
                    global_offset += len(file_obj['name']) + 12
                else:
                    global_offset += len(file_obj['name']) + 20
                files.append(file_obj)
    return global_offset, files

if len(sys.argv) == 5:
    action = sys.argv[1]
    version = int(sys.argv[2])
    filename = sys.argv[3]
    inputDir = sys.argv[4]

else:
    action = raw_input("Pack or unpack?")
    version = int(raw_input("Part 1 or 2?"))
    filename = raw_input("Filename: ")
    inputDir = raw_input("Directory: ")

create_directories(inputDir)

if action == 'pack':
    wad_file = open(filename, 'wb')
    os.chdir(inputDir)
    offset, files = create_metadata(inputDir, version)
    set_wad_metadata(wad_file, version, offset, files)
    copy_to_file(wad_file, files, offset)
if action == 'unpack':
    wad_file = open(filename, 'rb')
    os.chdir(inputDir)
    offset, files = get_wad_metadata(wad_file, version)
    copy_from_file(wad_file, files, offset)
wad_file.close()