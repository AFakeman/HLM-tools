# HLM-tools
HLM wad file packer/unpacker, and small sprite cutter
These are used to unpack existing Hotline Miami (1 and 2) files, and to create your compatible .wads
Packer1 and unpacker1 are intended to use for first part, and packer2 and unpacker2 are intended for second.

#Usage
Packers/unpackers have following syntax:

[script_name].py [directory to store files or directory to take files from] [input or output file]

If you don't provide these arguments, scripts will prompt you for them

Separator.py is meant to be used to cut character faces' sprites, and has the following syntax (requires PIL):

separator.py [sprite_file_name] [number of sprites]

then there will be created several files, each containing one sprite.

# Differences between formats
HLM uses the following format to store data (all integers are storred in little-endian format and take up 32 bits):
1) Offset from which begin files' contents (off)
2) Number of files (n)
Then, repeated n times:

3) length of file name (including path) (l)

4) l bytes containing name of the file

5) size of file in bytes

6) offset from off from which begins this file's contents

It actually allows for storing some information (steganography) between files' descriptions and contents, and between files, and after them.

HLM2, on the other hand, wouldn't allow storing anything between descriptions and contents, and has following scheme:

1) Number of files (n) (32 bits)

Then, repeated n times:

2) length of file name (including path) (l) (32 bits)

3) l bytes containing name of the file 

4) size of file in bytes (64 bits)

5) offset from end of descriptions from which begins this file's contents (64 bits)
