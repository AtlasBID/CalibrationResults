#
# Dump something about the inputs.
#

from comboFitCommands import dumpCommandResult, listToString
from FutureFile import FutureFile
import comboGlobals

#
# We will filter out input files on some criteria
#

def dump(sfObj, check=False, sysErrors = False):
    fc = Dump(sfObj, check, sysErrors)
    comboGlobals.Commands += [fc]
    return sfObj

#
# Command object to actually perform the dump
#

class Dump:
    def __init__ (self, sfinfo, check, sysErrors):
        self._sf = sfinfo
        self._check = check
        self._sysErrors = sysErrors

    def Execute (self, html, configInfo):
        files = listToString(self._sf.ResolveToFiles(html))

        if self._check:
            errcod = dumpCommandResult(html, "FTDump.exe --names --check %s" % files, "Checking input files.")
            if errcod != 0:
                print >> html, "Failed to run check! Command line: %s" % files

        if self._sysErrors:
            outputName = "%s-%s.html" % (configInfo.name, hash(files))
            
            errcod = dumpCommandResult(html, "FTDump.exe --sysErrorTable %s output %s" % (files, outputName), "Checking input files.")
            if errcod != 0:
                print >> html, "Failed to run check! Command line: %s" % files
            else:
                print >> html, '<p><a href="%s">Systematic Error Table</a></p>' % outputName
