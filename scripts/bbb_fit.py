#
# Do a bin-by-bin fit, but then also do a fully correlated fit and use the difference as a sys error on the first one.
#

#
# take all input files and transofrm them into a target output analysis.
#
def bbb_fit (f, anaName):
    #
    # First, do both fits
    #
    
    bbb_name = "bbb_%s_temp" % anaName
    comb_name = "comb_%s_temp" % anaName
    fit_comb = f.fit(comb_name)
    fit_bbb = f.fit(bbb_name, binByBin = True)

    #
    # Now, do the sys error difference
    #

    r = (fit_comb + fit_bbb).sys_delta_ana(anaName, bbb_name, comb_name, "Correlated Fit Systematic")

    return r
    
