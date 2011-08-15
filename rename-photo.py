#! /usr/bin/python

# 2011 (c) Alexander Danilov <alexander.a.danilov@gmail.com>
#
# To run this application you need to install pyexiv2 python exension.
# For Debian: sudo apt-get install python-pyexiv2

# TODO:
# - [ ] Rename first file in set of files (date_time_X.jpg, ..) with same DateTime
#       from date_time.jpg to date_time_1.jpg
# - [ ] Add check for files before rename
# - [ ] Add option "-n", which will only show how files will be renamed

import sys
import os
import pyexiv2


if sys.argv[1] == '-d':
    def debug(message):
        print >>sys.stderr, message

    origFiles = sys.argv[2:]

else:
    def debug(message):
        pass

    origFiles = sys.argv[1:]

# sort need here to correctly rename files with same DateTime value,
# because usually photo cameras name files 
origFiles.sort()

for origName in origFiles:
    ext = os.path.splitext(origName)[1]

    meta = pyexiv2.ImageMetadata(origName)

    try:
        meta.read()
    except IOError:
        print >>sys.stderr, "Warning: file " + origName + " containts no data, skipped"
    else:
        if 'Exif.Photo.DateTimeOriginal' in meta.exif_keys:
            tagName = 'Exif.Photo.DateTimeOriginal'
    
        elif 'Exif.Image.DateTime' in meta.exif_keys:
            tagName = 'Exif.Image.DateTime'
    
        else:
            print >>sys.stderr, 'Error: date and time not found for "' + origName + '"'
            exit(1)

        dateTime = meta['Exif.Photo.DateTimeOriginal'].value
        dirName = dateTime.strftime('%Y.%m.%d')
    
        fileName = dateTime.strftime('%Y%m%d_%H%M%S') + ext
        fullName = os.path.join(dirName, fileName)

        if os.path.exists(dirName):
            if os.path.isdir(dirName):
                # if file already exists, then add _X to name,
                # where X - unique number for this file name
                if os.path.exists(fullName):
                    idx = 1
                    while True:
                        fullName = os.path.join(dirName,
                                                dateTime.strftime('%Y%m%d_%H%M%S')
                                                + '_' + str(idx) + ext)
                        if not (os.path.exists(fullName)):
                            break
                        else:
                            idx += 1
                # else:
                    # do nothing

                debug("Move " + origName + " to " + fullName)

                os.rename(origName, fullName)

            else:
                print >>sys.stderr, "Error: can't create directory " + dirName + " - exists, but it is not a directory"
                exit(1)
        else:
            debug("Create directory " + dirName)
            os.mkdir(dirName)
            
            debug("Move " + origName + " to " + fullName)
            os.rename(origName, fullName)
