from imghdr import what
from os.path import isdir, isfile, splitext
from os import mkdir
from shutil import copy2, copyfileobj
from time import time_ns
from requests import get
from validators import url


def copylocalImg(src: str):

    dirname = '.local'

    if isfile('.dev'):
        dirname = '.local_dev'

    if isdir(dirname) is False:
        mkdir(dirname)

    if url(src):
        src = downloadImgHTTP(src)

    fileType = what(src)
    
    if isinstance(fileType, str) == False:
       old_fName, fileType = splitext(src)
       fileType = fileType[1:]
    
    hexVal = time_ns()

    fName = f"{hexVal}.{fileType}"
    rPath = f'{dirname}/{fName}'
    
    
    copy2(src, rPath)
    return rPath

def downloadImgHTTP(url_src:str):
    
    req = get(
        url_src,
        stream=True
    )

    if req.status_code == 200:
        req.raw.decode_content = True
        fname = url_src.split('/')[-1]
        dirname = '.local'

        if isfile('.dev'):
            dirname = '.local_dev'

        dest = f'{dirname}/{fname}'
        with open(dest, 'wb') as f:
            copyfileobj(req.raw, f)

        return dest
        


    
