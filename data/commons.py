from imghdr import what
from os.path import isdir, isfile, splitext
from os import mkdir
from shutil import copy2
from time import time_ns


def copylocalImg(src: str):

    fileType = what(src)
    
    if isinstance(fileType, str) == False:
       old_fName, fileType = splitext(src)
       fileType = fileType[1:]
    
    hexVal = time_ns()

    fName = f"{hexVal}.{fileType}"
    rPath = f'.local/{fName}'
    
    if isdir('.local') is False:
        mkdir('.local')
    
    copy2(src, rPath)
    return rPath



    
