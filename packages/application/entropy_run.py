#!/usr/bin/python
import os
def calculation4entropy(workdir):
	'''
--------------------------------------------------------
'calculation4entropy' is used to perform the calculation for entropy
        usage: calculation(workdir)
        input : workdir - the directory you put all the calculation files, including nmode_S, files.in, 
		delta_E_{com|rec|lig}.crd.* , prep and lib files 
        output: ds.out and ts.out
--------------------------------------------------------
'''
	path=os.getcwd()
	os.chdir(workdir)
	os.system('./nmode_S')
#	os.system('./average')
	os.chdir(path)

if __name__ == '__main__':
        calculation4entropy('./snapshot_E/entropy_cal')

 
