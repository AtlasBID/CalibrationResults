#
# Dump something about the inputs.
#

from comboFitCommands import dumpCommandResult, listToString
from FutureFile import FutureFile
import comboGlobals

#
# We will filter out input files on some criteria
#

def dump(sfObj, check=False, linage=False, sysErrors = False, metadata = False, name="", cnames=None):
    fc = Dump(sfObj, check, linage, sysErrors, name, metadata, cnames)
    comboGlobals.Commands += [fc]
    return sfObj

#
# Command object to actually perform the dump
#

class Dump:
    def __init__ (self, sfinfo, check, linage, sysErrors, name, metadata, cnames):
        self._sf = sfinfo
        self._linage = linage
        self._check = check
        self._sysErrors = sysErrors
        self._name = name
        self._metadata = metadata
        self._cnames = cnames

    def Execute (self, html, configInfo):
        files = listToString(self._sf.ResolveToFiles(html))

        ftype = ""
        args = ""
        title = ""

        if self._check:
            ftype = ".txt"
            title = "Names of anslyses in input files"
            args = "--names --check"

        if self._sysErrors:
            ftype = ".html"
            title = "systematic error table"
            args = "--sysErrorTable"

        if self._metadata:
            ftype = ".txt"
            title = "metadata"
            args = "--meta"
			
        if self._linage:
            ftype = "txt"
            title = "linage"
            args = "--linage"

        if self._cnames:
            title = "Check OPs"
            ftype = ".txt"
            args = "--cnames --inputfile=%s" % self._cnames

        # Run it

        if len(self._name) > 0:
            title += " (%s)" % self._name

        outputFileCmd = ""
        outputFile = ""
        if len(self._name) > 0:
            outputFileCmd = "output %s-%s.%s" % (configInfo.name, self._name, ftype)
            outputFile = "%s-%s.%s" % (configInfo.name, self._name, ftype)

        errcod = dumpCommandResult(html, "FTDump.exe %s %s %s" % (args, files, outputFileCmd), title)
        if errcod != 0:
            print >> html, "Failed to run check! Command line: %s" % files
        else:
            if len(outputFile) > 0:
                print >> html, '<a href="%s">%s</a>' % (outputFile, title)

