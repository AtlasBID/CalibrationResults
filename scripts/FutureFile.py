#
# A file that will exist in the future
#

import os
from sfObject import sfObject

class FutureFile (sfObject):
    def __init__ (self):
        sfObject.__init__(self)
        self._fname = "<not configured>"

    def SetFName (self, name):
        self._fname = name

    # Return the one file
    def ResolveToFiles (self, html):
        if not os.path.exists(self._fname):
            raise "File '%s' was to be set but never was seen" % self._fname
        return [self._fname]
    
