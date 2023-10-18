import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np
import matplotlib as mpl
import glob
import lic
import matplotlib
from scipy.io import FortranFile
import struct
import os
def read_var(filename,varname,size):
    f=open(filename+"/"+varname, "rb")
    dat = np.fromfile(f, dtype=np.float, count=size, sep='')
    #dat = np.loadtxt(filename+"/"+varname)#
    return dat

def read_parameter_file(fname="",dict_name="",evaluate=True,verbose=False,delimiter="="):
    # Read info file and create dictionary
    try:
        with open(fname) as f:
            content = f.readlines()
        f.close()
    except IOError:
        # Clean exit if the file was not found
        if verbose:
            print("File not found: "+fname)
        #if raise_error:
        #raise IOError
        #else:
        return 0

    dictionnary={}
    for line in content:
        sp = line.split(delimiter)
        if len(sp) > 1:
            if evaluate:
                try:
                    dictionnary[sp[0].strip()] = eval(sp[1].strip())
                except (NameError,SyntaxError):
                    dictionnary[sp[0].strip()] = sp[1].strip()
            else:
                dictionnary[sp[0].strip()] = sp[1].strip()
    return dictionnary