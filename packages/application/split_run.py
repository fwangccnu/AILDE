#!/usr/bin/python
import os
def splitcom2subitems(filename,ligname,outputdir,comout,recout,ligout):
	'''
--------------------------------------------------------
'splitcom2subitems' is used to split complex into com,rec,lig by using ligand name
	usage : splitcom2subitems(filename,ligname,outputdir,comout,recout,ligout)
        input : filename - file need to be deal; ligname - ligand name (3 letters);
		outputdir - destinations to put the result file
		comout/rceout/ligout - out name of comout/recout/ligout 
        output: pdb file for com/rec/lig
--------------------------------------------------------
'''
        if os.path.isdir(outputdir):
                pass
        else:
                os.system('mkdir -p {dir}'.format(dir=outputdir))
	
	F1 = open(filename,'r')
	F2 = open(outputdir+'/'+recout,'w+')
	F3 = open(outputdir+'/'+ligout,'w+')
	F4 = open(outputdir+'/'+comout,'w+')
	for line in F1:
		F4.write(line)
		if line.startswith('ATOM') or line.startswith('HETATM'):
			if line[17:20] == ligname:
				F3.write(line)
			else:
				F2.write(line)
		elif line.startswith('TER'):
				F2.write(line)
		else:
			pass
	F2.write('END')
	F3.write('END')
	F2.close()
	F3.close()
	F4.close()
