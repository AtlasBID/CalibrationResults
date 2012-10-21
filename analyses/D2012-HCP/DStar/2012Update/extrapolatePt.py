
import os
import glob

for oldfile in glob.glob( os.path.join('./', '*.txt') ):

    infile = open(oldfile,"r")
    line = infile.readline()
    if line.find(",charm,")!=-1:
        print "copying file " + oldfile
        newfile = "./mod/"+oldfile
#        newfile = newfile.replace(".txt","_expt.txt")
        print "          to " + newfile
 
#open files
        outfile = open(newfile, "w")
        infile.seek(0);

#inquire numebr of lines
        count_lines = len(infile.readlines())

#put back pointer at the top
        infile.seek(0)

# stop when we found two consecutive }
        found = -1
        stop  = -1
        for i in range(count_lines):
            line = infile.readline()
            if found == 1:
                if line.find("}") != -1:
                    stop = i
            if line.find("}") != -1:
                found = 1 
            else:
                found = 0

#put back pointer at the top
        infile.seek(0)

#finally create new files

        for i in range(stop):
            line = infile.readline()
            outfile.write(line)
        infile.seek(0)
        copy = 0
        for i in range(stop):
            line = infile.readline()
            if line.find("140<pt<200") != -1:
                copy = 1
                line = line.replace("140<pt<200","200<pt<300")
            if copy==1:
                if line.find("}") != -1:
                    outfile.write('     sys(Dstar: pT extrap,16%)\n')
                    outfile.write('  } \n')
                else:
                    outfile.write(line);
        outfile.write('}\n')    
        
