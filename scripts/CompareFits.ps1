# Run fits bin-by-bin and print out the chi2

param (
    [string] $DropSystematicErrors
)

# THe files to use for the inputs
#$cmdFitLine = "..\system8\Combination-MV1_601713.txt ..\ptrel\MV170_toGordon.txt ..\stat_correlation_inputs.txt --ignore .*20-pt-200"
$initialFiles = @("..\system8\Combination-MV1_601713.txt", "..\ptrel\MV170_toGordon.txt")
$cmdFitLine = @("..\stat_correlation_inputs.txt", "--ignore",  ".*20-pt-200")

"Results:" >> results.txt

# Alter the input files as requested.
$allSingleSys = @("")
if ($DropSystematicErrors) {
  "  -> Will drop all comma seperated sys errors: $DropSystematicErrors" >> results.txt

  $allSingleSys = $DropSystematicErrors -split "," | % {$_.Trim()}
}


# Master loop over every possible combination...
foreach ($dropSys in $allSingleSys) {
  $files = $initialFiles

  if ($($dropSys.Length) -gt 0) {
    FTManipSys.exe outputFlavor bottom dropSysError $dropSys $files output dropSysAna.txt $cmdFitLine
    $files = @("dropSysAna.txt")
    "  Drop Sys $dropSys" >> results.txt
  }

  FTCombine.exe $files $cmdFitLine
  "  Correlated fit: " >> results.txt
  get-content combined.txt | ? {$_.Contains("gchi") -or $_.Contains("gndof")} | % { "    $_"}  >> results.txt

  FTCombine.exe $files $cmdFitLine --binbybin
  "  Bin-By-Bin fit: " >> results.txt
  get-content combined.txt | ? {$_.Contains("gchi") -or $_.Contains("gndof")} | % { "    $_"} >> results.txt
  "" >> results.txt
  "" >> results.txt
}
