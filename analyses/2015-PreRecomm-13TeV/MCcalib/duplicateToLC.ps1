# Define this function in powershell:

function writenewfile ($fname) { Get-Content "${fname}.txt" | % {$_ -replace "AntiKt4TopoEMnoJVF","AntiKt4TopoLCnoJVF" } | % {Add-Content "${fname}-LC.txt" "$_"} }

# Then in the directory for all the files do the following to duplicate:

Get-ChildItem . | % {$_.BaseName} | % {writenewfile $_ }