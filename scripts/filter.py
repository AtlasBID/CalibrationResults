from comboFitCommands import dumpCommandResult, listToString
from FutureFile import FutureFile
import comboGlobals

#
# We will filter out input files on some criteria
#

def filter(sfObj, analyses = []):
    if len(analyses) == 0:
        print "Filtering nothing. Will pass everythign on"
        return sfObj
    
    rf = FutureFile()
    fc = Filter(sfObj, analyses, rf)
    comboGlobals.Commands += [fc]
    return rf

#
# Command object to actually perform the filter.
#

class Filter:
    def __init__ (self, sfinfo, analyses, futureFile):
        self._sf = sfinfo
        self._anas = analyses
        self._ff = futureFile

    def Execute (self, html, configInfo):
        files = listToString(self._sf.ResolveToFiles(html))
        for a in self._anas:
            files += " --analysis %s" % a
        files += " --asInput"

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        files += " output %s-sf.txt" % baseOutputName

        errcod = dumpCommandResult(html, "FTDump.exe %s" % files, "Filtering for %s" % self._anas)
        if errcod != 0:
            print >> html, "Failed to filter! Command line: %s" % files
            raise BaseException("Unable to filter")

        self._ff.SetFName("%s-sf.txt" % baseOutputName)
