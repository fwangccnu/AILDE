#!/usr/bin/python
def mmpbsa4energy(filein,fileout,parallel,path,comtop,rectop,ligtop):
        '''
--------------------------------------------------------
'mmpbsa4energy' is used to generate pbsa input file.
        input :
filein - template in file.   fileout - final pbsa file for calculation
parallel - whether to use mutiple processes(default 4 processes)
path - the destination of the snapshots
comtop,rectop,ligtop - the destination of top file for com/rec/lig.
        output: a file named fileout, for mmpbsa calculation.
--------------------------------------------------------
        '''
	F1 = open(filein,'r')
	F2 = open(fileout,'w+')
	for line in F1:
		if line.startswith('PARALLEL') and parallel == 'YES':
			line='PARALLEL'+'              '+'4'+'\n'
			F2.write(line)
	        elif line.startswith('PATH'):
        	        line='PATH'+'                  '+path+'\n'
                	F2.write(line)
        	elif line.startswith('COMPT'):
                	line='COMPT'+'                 '+comtop+'\n'
                	F2.write(line)
        	elif line.startswith('RECPT'):
                	line='RECPT'+'                 '+rectop+'\n'
                	F2.write(line)
        	elif line.startswith('LIGPT'):
                	line='LIGPT'+'                 '+ligtop+'\n'
                	F2.write(line)
        	else:
                	F2.write(line)
	F1.close()
	F2.close()
	
