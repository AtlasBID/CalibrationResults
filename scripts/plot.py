#
# Plot the input files
#

from comboFitCommands import dumpCommandResult, listToString, dumpFile, rerunCommand
import comboGlobals

import shutil

#
# The plot operator, called on an sfObject
#
def plot(sfobj, name):
    comboGlobals.Commands += [Plot(sfobj, name)]
    return sfobj

#
# Plot our input files
#
class Plot:
    # Plot a bunch of inputs with a certian name
    def __init__(self, sfinfo, name):
        self._sf = sfinfo
        self._name = name

    # Run the plotter!
    def Execute(self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        outFile = "%s-plots-%s.root" % (configInfo.name, self._name)
        cmdLog = "%s-plots-%s-cmd-log.txt" % (configInfo.name, self._name)

        title = "Plots for %s" % self._name

        if rerunCommand(fList, outFile):
            errcode = dumpCommandResult(html, "FTPlot.exe %s" % files, title, store=cmdLog)
            if errcode == 0:
                shutil.copy ("plots.root", outFile)
            else:
                print >> html, "<b>Plotting failed with error code %s</b>" % errcode
                print >> html, "Command line arguments: %s" % files
        
        else:
            dumpFile(html, cmdLog, title)
            print >> html, "<p>Inputs have not changed, resuing results from last run</p>"

        print >> html, '<a href="%s">Scale Factor Plots</a>' % outFile
