####################################################################################################
#                                                                                                  #
#   Convert dynamical matrix files from Quantum Espresso ph.x to phonon dispersion data files      #
#   suitable for visualization in Grace                                                            #
#                                                                                                  #
####################################################################################################

import os
import re

## ask user for base filename for dynamical matrix files
dmfilename = raw_input("Input base filename for dynamical matrix files (e.g. dyn.G): ")

## store filenames in list and calculate the number of k-points
filestring = os.popen("ls "+dmfilename+"*").read()
filelist = filestring.split()
del filelist[0]
nk = len(filelist)

## human sort of file list (e.g. dyn.G1, dyn.G2, dyn.G3, etc.)
def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]
filelist.sort(key=natural_keys)

## store frequencies
freq = []
for i in range(nk):
    file = open(filelist[i])

    for line in file:
        if 'freq (  ' in line:
            list = line.split()
            freq.append(list[7])

    file.close()
nbands = len(freq)/nk

## write file viewable by xmgrace
outfile = open("output.dat","w")
k = 0
for i in range(nk):
    datstr = str(i)
    for j in range(nbands):
        datstr += " "+freq[k]
        k += 1
    outfile.write(datstr+"\n")
