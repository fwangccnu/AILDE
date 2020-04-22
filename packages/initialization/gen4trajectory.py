#!/usr/bin/python
import os
def cpptraj4combine(filename,end,AA): 
	F = open(filename,'w+')
	MDENDJOB = int(end)         #end represents the last number of crd file
	for x in range(1,MDENDJOB+1):
		F.write('trajin md{x}.crd\n'.format(x=str(x)))
	F.write('\n')
	F.write('center :1-{all_AA}\n'.format(all_AA=str(AA+1)))
	F.write('image center familiar\n')
	F.write('strip :WAT\n')
	F.write('strip :Cl-\n')
	F.write('strip :Na+\n')
	F.write('trajout md.crd nobox\n')
	F.close()

def cpptraj4rms(filename,AA):
	F1 = open(filename,'w+')
	F1.write('trajin complex.crd\n')
	F1.write('trajin md.crd\n')
	F1.write('rms mass first out rms-backbone.rms :1-{AA_number}&!@N,CA,C= time 1\n'.format(AA_number=str(AA)))
	F1.write('rms mass first out rms-lig.rms :{all_AA}&!@H= time 1'.format(all_AA=str(AA+1)))
	F1.close()

def cpptraj4snapshots(filename,outputdir,starttime,endtime,step): 
	if os.path.isdir(outputdir):
	        pass
	else:
        	os.system('mkdir -p {dir}'.format(dir=outputdir))
	F2=open(filename,'w+')
	F2.write('trajin md.crd {start} {end} {step}\n'.format(start=starttime,end=endtime,step=step))
	F2.write('strip :Na+\n')
	F2.write('strip :WAT\n')
	F2.write('trajout ./snapshot_E/com.rst multi restart\n')          #get snapshot into restart format
	F2.write('trajout ./snapshot_E/com.pdb multi pdb\n')              #get snapshot into pdb format
	F2.close()


