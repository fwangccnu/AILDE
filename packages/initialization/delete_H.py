#!/usr/bin/python
def del_H(input,*output):
	'''
--------------------------------------------------------
'del_H' is used to DELETE ALL Hydrogens in the complex
	input : a complex PDB file.
	output: complex file with NO Hydrogens.
	return: return is the output file name.
--------------------------------------------------------
	'''
	F=open(input,'r')
	if output == ():
		file_out = input.split('.')[0]+'_noH.pdb'
	else:
		file_out = output[0]
	F1=open(file_out,'w+')
	for line in F:
		if line.startswith('ATOM') or line.startswith('HETATM'):
			if line[76:78].strip() == 'H':
				pass
			else:	
				F1.write(line)
                elif line.startswith('TER') or line.startswith('END'):
                        F1.write(line) 
		else:
			pass
	F.close()
	F1.close()
	return file_out
