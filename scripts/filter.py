#
# Filter the input for some set of criteria.
#

from comboFitCommands import dumpCommandResult, listToString, rerunCommand, dumpFile, dumpTitle
from FutureFile import FutureFile
import comboGlobals
import os # For AFT186
#
# We will filter out input files on some criteria
#

def filter(sfObj, analyses = [], taggers=[], ignore=[], jets=[]):
    if len(analyses) == 0 and len(taggers) == 0 and len(ignore) == 0 and len(jets) == 0:
        print "Filtering nothing. Will pass everythign on"
        return sfObj
    
    rf = FutureFile()
    fc = Filter(sfObj, analyses, taggers, ignore, jets, rf)
    comboGlobals.Commands += [fc]
    return rf

#
# Command object to actually perform the filter.
#

class Filter:
    def __init__ (self, sfinfo, analyses, taggers, ignore, jets, futureFile):
        self._sf = sfinfo
        self._anas = analyses
        self._taggers = taggers
        self._ignore = ignore
        self._ff = futureFile
        self._jets = jets

    def Execute (self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)
#
# Implementation of AFT-186: If input list is empty, print Warning message
#
        if files == "":                
            print >> html, "<p><b> Warning: empty list of input files passed to the function filter.</b></p>"
#
# End of modification
#
        for a in self._anas:
            files += " --analysis '%s'" % a

        for t in self._taggers:
            files += " --tagger '%s' --operatingPoint '%s'" % (t[0], t[1])

        for i in self._ignore:
            files += " --ignore '%s'" % i

        for j in self._jets:
            files += " --jetAlgorithm '%s'" % j

        files += " --asInput"

        baseOutputName = "%s-%s" % (configInfo.name, hash(files))
        outputName = "%s-sf.txt" % baseOutputName
        cmdLog = "%s-cmd-log.txt" % baseOutputName
        files += " output %s" % outputName

        title = "Filtering for %s" % listToString(self._anas + self._taggers + self._ignore + self._jets)

        dumpTitle(html, title)
        print >> html, "<b>Command line: FTDump %s</b>" % files
        if rerunCommand(fList, outputName, files, html):
            errcod = dumpCommandResult(html, "FTDump %s" % files, store=cmdLog)
            if errcod != 0:
                print >> html, "Failed to filter! Command line: %s" % files
                raise BaseException("Unable to filter")

        else:
            print >> html, "<p>Using results of last filter command as no inputs have changed.</p>"
            dumpFile(html, cmdLog)
#
# Implemtnation of AFT-186: If output file doesn't exist or has a size less or equal to 1B (corresponding to 1 character inside the file), then print a warning message.
#
        if not (os.path.isfile(outputName) and os.path.getsize(outputName) > 1):
            print >> html, "<p><b> Warning: output file of the filtering doesn't exsit or is empty.</b></p>"
#
# End of modification
#


        print >> html, '<p><a href="%s">Scale Factor File</a></p>' % outputName
        
        self._ff.SetFName(outputName)
