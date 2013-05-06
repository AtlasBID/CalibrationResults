#
# Filter the input for some set of criteria.
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile
from FutureFile import FutureFile
import comboGlobals

#
# We will filter out input files on some criteria
#

def filter(sfObj, analyses = [], taggers=[], ignore=[]):
    if len(analyses) == 0 and len(taggers) == 0 and len(ignore) == 0:
        print "Filtering nothing. Will pass everythign on"
        return sfObj
    
    rf = FutureFile()
    fc = Filter(sfObj, analyses, taggers, ignore, rf)
    comboGlobals.Commands += [fc]
    return rf

#
# Command object to actually perform the filter.
#

class Filter:
    def __init__ (self, sfinfo, analyses, taggers, ignore, futureFile):
        self._sf = sfinfo
        self._anas = analyses
        self._taggers = taggers
        self._ignore = ignore
        self._ff = futureFile

    def Execute (self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        for a in self._anas:
            files += " --analysis %s" % a

        for t in self._taggers:
            files += " --tagger %s --operatingPoint %s" % (t[0], t[1])

        for i in self._ignore:
            files += " --ignore '%s'" % i

        files += " --asInput"

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        outputName = "%s-sf.txt" % baseOutputName
        cmdLog = "%s-cmd-log.txt" % baseOutputName
        files += " output %s" % outputName

        title = "Filtering for %s" % listToString(self._anas + self._taggers + self._ignore)

        if rerunCommand(fList, outputName):
            errcod = dumpCommandResult(html, "FTDump.exe %s" % files, title, store=cmdLog)
            if errcod != 0:
                print >> html, "Failed to filter! Command line: %s" % files
                raise BaseException("Unable to filter")

        else:
            dumpFile(html, cmdLog, title)
            print >> html, "<p>Using results of last filter command as no inputs have changed.</p>"

        print >> html, '<p><a href="%s">Scale Factor File</a></p>' % outputName
        
        self._ff.SetFName(outputName)
