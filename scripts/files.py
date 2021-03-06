#
# Class that holds onto a list of files
#

from sfObject import sfObject

import sys
import glob
import os

#
# Given a name, which may be a wildcard, see fi we can find it. First
# on its own, and then relative to everythign in the sys.path variable.
#
def pathglob (name):
    if name == None:
        return []
    path_to_try = ["./"] + sys.path
    for p in path_to_try:
        flist = glob.glob(os.path.join(p, name))
        if len(flist) > 0:
            return flist

    print 'Input file path "%s" had no matching files' % name
    return []

#
# Class to get all the files.
#
class files (sfObject):
    def __init__ (self, files, no_files_ok=False):
        sfObject.__init__(self)
        self._file_list = [f for f in pathglob(files) if os.path.isfile(f)]
        if len(self._file_list) == 0:
            if files != None:
                raise BaseException("no files for %s" % files)
        
    # We hold only files, so when we are called to resovle to files, it is
    # a pretty simple thing.
    def ResolveToFiles (self, thml):
        return self._file_list
    
