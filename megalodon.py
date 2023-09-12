import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import read

au = 1.5e13
pc = 3e18
class SharkData():
	def __init__(self,nout=1,path=".",unit_length='au'):
		print("We're gonna need a bigger boat...")
		filelist = sorted(glob.glob(path+"/output*"))
		if(nout==-1):
			number   = filelist[-1].split("_")[-1]
		else:
			number   = nout
		filename = path+'/'+"output_"+ str(number).zfill(5)+'/'
		print('Reading output number '+ str(number))

		infos=self.read_parameter_file(filename+'info.dat')
		for key in infos:
			print (key,' = ', infos[key])
			setattr(self,key,infos[key])
		self.unit_length=unit_length
		if(self.unit_length=='au'):
			scale_l=au
		if(self.unit_length=='pc'):
			scale_l=pc
		print("Reading x")
		self.x   = self.read_var(filename,'x',self.NX*self.NY)*self.unit_l/scale_l
		print("Reading density")
		self.rho = self.read_var(filename,'rho',self.NX*self.NY)
		print("Reading velocity")
		self.v   = self.read_var(filename,'v',self.NX*self.NY)
		print("Reading gas pressure")
		self.P   = self.read_var(filename,'P',self.NX*self.NY)
		print("Reading dust")
		if(self.ndust>0):
			self.rhod = self.read_var(filename,'rhod',self.NX*self.NY*self.ndust)
			self.sd   = self.read_var(filename,'sd',self.NX*self.NY*self.ndust)
			self.rhod_full = np.reshape(self.rhod,(self.ndust,self.NX),order = "C").T
			self.sd_full   = np.reshape(self.sd,(self.ndust,self.NX),order = "C").T
			
	#Variable reader	
	def read_var(self,filename,varname,size):
		f=open(filename+varname, "rb")
		dat = np.fromfile(f, dtype=np.float, count=size, sep='')
		#dat = np.loadtxt(filename+"/"+varname)#
		return dat

	#Parameter file reader
	def read_parameter_file(self,fname="",dict_name="",evaluate=True,verbose=False,delimiter="="):
		# Read info file and create dictionary
		print('Reading the info file')
		try:
			with open(fname) as f:
				content = f.readlines()
			f.close()
		except IOError:
			# Clean exit if the file was not found
			if verbose:
				print("File not found: "+fname)
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