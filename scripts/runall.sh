#/bin/env bash
# This script is sourced in the context of the build runner. Place all the configurations you'd like to run
# here. It is sourced from the base directory of this package.
#
# The "|| true" at the end of the line allows things to progress - the script doesn't just die.
#
#
./scripts/combine.py --zip analyses/2014-Winter-7TeV/2014-Winter-7TeV.py
./scripts/combine.py --zip analyses/2014-Winter/2014-Winter.py
