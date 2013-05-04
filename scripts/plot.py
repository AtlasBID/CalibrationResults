from comboFitCommands import dumpCommandResult, listToString
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
        files = listToString(self._sf.ResolveToFiles(html))

        errcode = dumpCommandResult(html, "FTPlot.exe %s" % files, "Plots for %s" % self._name)
        if errcode == 0:
            shutil.copy ("plots.root", "%s-plots-%s.root" % (configInfo.name, self._name))
            print >> html, '<a href="%s-plots-%s.root">Scale Factor Plots</a>' % (configInfo.name, self._name)
        else:
            print >> html, "<b>Plotting failed with error code %s</b>" % errcode
            print >> html, "Command line arguments: %s" % files
        
