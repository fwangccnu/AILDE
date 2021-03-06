#!/usr/bin/python
def deal4newlig(ligfile,outputlig):
	'''
--------------------------------------------------------
'deal4newlig' is used to deal with the ill-formed ligand pdb file generating by autogrow
        usage: grow4lead(ligfile,outputlig)
        input : ligfile - the ligand pdb file generated by autogrow 
        output: outputlig - the normal form can be identified by AMBER 
--------------------------------------------------------
'''
	F1 = open(ligfile,'r')
	F2 = open(outputlig,'w+')
	e = 1
	for line in F1:
		if line.startswith('ATOM') or line.startswith('HETATM'):
			atom_name = line[12:16]
			CB = atom_name.strip()[:2]    #fetch the ATOM 
			AN = atom_name.strip()[2:]
			resi_name = line[17:20]
			elem_name = line[76:78]
			if CB.lower() == 'cl' and elem_name.lower() == 'cl':        #Regular the 'Cl' and 'Br'
				line = line[:12] + 'Cl' + line[14:]
			elif CB.lower() == 'br' and elem_name.lower() == 'br':
				line = line[:12] + 'Br' + line[14:]
			else:
				pass
			
			if elem_name.strip() == 'A':
				line = line[:76] + ' C ' + line[78:]
			elif elem_name.strip() == 'OA':
				line = line[:76] + ' O ' + line[78:]
			elif elem_name.strip() == 'NA':
				line = line[:76] + ' N ' + line[78:] 
	
			line = line[:14]+'%-2s'%(e)+line[16:]                        #give the atom number to every atom
			line = line[:17] + 'LIG' + line[20:79] + '\n'                #name the small molecule into LIG
			e+=1
			F2.write(line)

		elif line.startswith('TER') or line.startswith('END'):
			F2.write(line)
		
		else:
			pass
	F2.write('END\n')
	F1.close()
	F2.close()

		
