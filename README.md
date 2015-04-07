# HLM-tools
HLM wad file packer/unpacker, and small sprite cutter
These are used to unpack existing Hotline Miami (1 and 2) files, and to create your compatible .wads
Packer1 and unpacker1 are intended to use for first part, and packer2 and unpacker2 are intended for second.

##Usage
Packers/unpacker now has the following syntax:

    [script_name].py [pack or unpack] [1 or 2, depending on part of the game] [wad file name] [directory for packing or unpacking]

Separator.py is meant to be used to cut sprites using .meta file, and has the following syntax (requires PIL):

    separator.py [sprite_file_name_w/o_ext] [output_folder]

Note: script is made with assertion that in the same folder as `[sprite_name.png]`, there is `[sprite_name.meta]`, then there will be created several files, each containing one sprite.

## Differences between formats
HLM uses the following format to store data (all integers are storred in little-endian format and take up 32 bits):

    * Offset from which begin files' contents (off)
    * Number of files (n)
    Then, repeated n times:
        * length of file name (including path) (l)
        * l bytes containing the name of the file
        * size of file in bytes
        * offset from off from which begins this file's contents

It actually allows for storing some information (steganography) between files' descriptions and contents, and between files, and after them. HLM2, on the other hand, wouldn't allow storing anything between descriptions and contents, and has following scheme:

    * Number of files (n) (32 bits)
    Then, repeated n times:
        * length of file name (including path) (l) (32 bits)
        * l bytes containing name of the file 
        * size of file in bytes (64 bits)
        * offset from end of descriptions from which begins this file's contents (64 bits)`

## .meta file format

HLM2 uses the following format to store sprites' metadata:

    * Magical constant '0F4147544558545552455041434B4552' ([0F]AGTEXTUREPACKER)
    * 01000000 (not sure what it'd do)
    * .png width
    * .png height
    Then, repeated until the end of the file:
        * length of the file name (l) (1 byte)
        * l bytes containing the name of the sprite
        * number of sprites (n) (32 bits)
        Then, repeated n times:
            * Sprite width (32 bits)
            * Sprite height (32 bits)
            * X coordinate of the top left corner
            * Y coordinate of the top left coner
            * Another 16 bytes of unknown information