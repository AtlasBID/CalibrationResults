#
# Do a bin-by-bin fit, but then also do a fully correlated fit and use the difference as a sys error on the first one.
#

#
# take all input files and transofrm them into a target output analysis.
#
def bbb_fit (f, anaName, saveCHI2Fits = False, includeSources = False, extraFiles = None):
    #
    # First, do both fits
    #
    
    bbb_name = "bbb_%s_temp" % anaName
    comb_name = "comb_%s_temp" % anaName
    fit_comb = f.fit(comb_name, extraFiles = extraFiles)
    fit_bbb = f.fit(bbb_name, binByBin = True, extraFiles = extraFiles)

    #
    # Now, do the sys error difference
    #

    r = (fit_comb + fit_bbb).sys_delta_ana(anaName, bbb_name, comb_name, "Correlated Fit Systematic")

    if saveCHI2Fits:
        r = r + fit_comb

    if includeSources:
        r = r + f
        
    return r
    
