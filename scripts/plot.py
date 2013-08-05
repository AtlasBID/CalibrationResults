#
# Plot the input files
#

from comboFitCommands import dumpCommandResult, listToString, dumpFile, rerunCommand, dumpTitle
import comboGlobals

import shutil

#
# The plot operator, called on an sfObject
#
def plot(sfobj, name, byCalibEff = False, effOnly = False):
    comboGlobals.Commands += [Plot(sfobj, name, byCalibEff, effOnly)]
    return sfobj

#
# Plot our input files
#
class Plot:
    # Plot a bunch of inputs with a certian name
    def __init__(self, sfinfo, name, byCalibEff, effOnly):
        self._sf = sfinfo
        self._name = name
        self._byCalibEff = byCalibEff
        self._effOnly = effOnly

    # Run the plotter!
    def Execute(self, html, configInfo):
        fList = self._sf.ResolveToFiles(html)
        files = listToString(fList)

        outFile = "%s-plots-%s.root" % (configInfo.name, self._name)
        cmdLog = "%s-plots-%s-cmd-log.txt" % (configInfo.name, self._name)

        title = "Plots for %s" % self._name

        if self._byCalibEff:
            files += " --ByCalibEff"

        if self._effOnly:
            files += " --EffOnly"

        dumpTitle(html, title)
        if rerunCommand(fList, outFile, files, html):
            errcode = dumpCommandResult(html, "FTPlot.exe %s" % files, store=cmdLog)
            if errcode == 0:
                shutil.copy ("plots.root", outFile)
            else:
                print >> html, "<b>Plotting failed with error code %s</b>" % errcode
                print >> html, "Command line arguments: %s" % files
        
        else:
            dumpFile(html, cmdLog)
            print >> html, "<p>Inputs have not changed, resuing results from last run</p>"

        print >> html, '<a href="%s">Scale Factor Plots</a>' % outFile
