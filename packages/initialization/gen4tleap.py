#!/usr/bin/python
import os
import fnmatch
def tleap4wat2md(com,filename,path):
	f1=open(filename,'w+')
	f1.write('source leaprc.ff14SB.redq\n')
	f1.write('source leaprc.gaff\n')
	f1.write('loadamberparams frcmod.ionsjc_tip3p\n')
	f1.write('loadamberprep h2o.prep\n')
	f1.write('loadamberparams ligand.frcmod\n')
	f1.write('loadamberprep ligand.prep\n')
	if os.path.isdir(r'./confactors_para'):                         #Write tleap.in file and get the complex.top and complex.crd file
	        directory=os.listdir(r'./confactors_para')
	        for file in directory:
	                if fnmatch.fnmatch('./confactors_para/{file}'.format(file=file),'*prep'):
	                        f1.write("loadamberprep ./confactors_para/{confactor_prep}\n".format(confactor_prep=file))
			elif fnmatch.fnmatch('./confactors_para/{file}'.format(file=file),'*.lib'):
				f1.write("loadoff ./confactors_para/{confactor_lib}\n".format(confactor_lib=file))
	                elif fnmatch.fnmatch('./confactors_para/{file}'.format(file=file),'*frcmod'):
	                        f1.write("loadamberparams ./confactors_para/{confactor_frcmod}\n".format(confactor_frcmod=file))
	                else:
	                        continue
	f1.write('complex=loadpdb {path}/{complex}\n'.format(path=path,complex=com))
#	f1.write('receptor=loadpdb {path}/{receptor}\n'.format(path=path,receptor=rec))
#	f1.write('ligand=loadpdb {path}/{ligand}\n'.format(path=path,ligand=lig))
	f1.write('saveamberparm complex {path}/complex.top {path}/complex.crd\n'.format(path=path))
#	f1.write('saveamberparm receptor {path}/receptor.top {path}/receptor.crd\n'.format(path=path))
#	f1.write('saveamberparm ligand {path}/ligand.top {path}/ligand.crd\n'.format(path=path))
	f1.write('model=copy complex\n')
	f1.write('addions complex Cl- 0\n')
	f1.write('addions complex Na+ 0\n')
	f1.write('solvatebox complex TIP3PBOX 10.0\n')
	f1.write('saveamberparm complex {path}/complex_wat.top {path}/complex_wat.crd\n'.format(path=path))
	f1.write('quit')
	f1.close()


def tleap4nowat2md(com,filename,path):
        f1=open(filename,'w+')
        f1.write('source leaprc.ff14SB.redq\n')
        f1.write('source leaprc.gaff\n')
        f1.write('loadamberparams frcmod.ionsjc_tip3p\n')
        f1.write('loadamberprep h2o.prep\n')
        f1.write('loadamberparams ligand.frcmod\n')
        f1.write('loadamberprep ligand.prep\n')
        if os.path.isdir(r'./confactors_para'):                         #Write tleap.in file and get the complex.top and complex.crd file
                directory=os.listdir(r'./confactors_para')
                for file in directory:
                        if fnmatch.fnmatch('./confactors_para/{file}'.format(file=file),'*prep'):
                                f1.write("loadamberprep ./confactors_para/{confactor_prep}\n".format(confactor_prep=file))
			elif fnmatch.fnmatch('./confactors_para/{file}'.format(file=file),'*.lib'):
				f1.write("loadoff ./confactors_para/{confactor_lib}\n".format(confactor_lib=file))
                        elif fnmatch.fnmatch('./confactors_para/{file}'.format(file=file),'*frcmod'):
                                f1.write("loadamberparams ./confactors_para/{confactor_frcmod}\n".format(confactor_frcmod=file))
                        else:
                                continue
        f1.write('complex=loadpdb {path}/{complex}\n'.format(path=path,complex=com))
#       f1.write('receptor=loadpdb {path}/{receptor}\n'.format(path=path,receptor=rec))
#       f1.write('ligand=loadpdb {path}/{ligand}\n'.format(path=path,ligand=lig))
        f1.write('saveamberparm complex {path}/complex.top {path}/complex.crd\n'.format(path=path))
#       f1.write('saveamberparm receptor {path}/receptor.top {path}/receptor.crd\n'.format(path=path))
#       f1.write('saveamberparm ligand {path}/ligand.top {path}/ligand.crd\n'.format(path=path))
        f1.write('quit')
        f1.close()


def tleap4nowat2pbsa(filename,com,rec,lig,comcrd,reccrd,ligcrd,path):
        f1=open(filename,'w+')
        f1.write('source leaprc.ff14SB.redq\n')
        f1.write('source leaprc.gaff\n')
        f1.write('loadamberparams frcmod.ionsjc_tip3p\n')
        f1.write('loadamberprep h2o.prep\n')
        f1.write('loadamberparams ligand.frcmod\n')
        f1.write('loadamberprep ligand.prep\n')
        if os.path.isdir(r'./confactors_para'):                         #Write tleap.in file and get the complex.top and complex.crd file
                directory=os.listdir(r'./confactors_para')
                for file in directory:
                        if fnmatch.fnmatch('./confactors_para/{file}'.format(file=file),'*prep'):
                                f1.write("loadamberprep ./confactors_para/{confactor_prep}\n".format(confactor_prep=file))
			elif fnmatch.fnmatch('./confactors_para/{file}'.format(file=file),'*.lib'):
				f1.write("loadoff ./confactors_para/{confactor_lib}\n".format(confactor_lib=file))
                        elif fnmatch.fnmatch('./confactors_para/{file}'.format(file=file),'*frcmod'):
                                f1.write("loadamberparams ./confactors_para/{confactor_frcmod}\n".format(confactor_frcmod=file))
                        else:
                                continue
        f1.write('complex=loadpdb {path}/{complex}\n'.format(path=path,complex=com))
        f1.write('receptor=loadpdb {path}/{receptor}\n'.format(path=path,receptor=rec))
        f1.write('ligand=loadpdb {path}/{ligand}\n'.format(path=path,ligand=lig))
        f1.write('saveamberparm complex {path}/complex.top {path}/{comcrd}\n'.format(path=path,comcrd=comcrd))
        f1.write('saveamberparm receptor {path}/receptor.top {path}/{reccrd}\n'.format(path=path,reccrd=reccrd))
        f1.write('saveamberparm ligand {path}/ligand.top {path}/{ligcrd}\n'.format(path=path,ligcrd=ligcrd))
        f1.write('quit')
        f1.close()

