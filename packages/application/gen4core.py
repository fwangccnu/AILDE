#!/usr/bin/python
def gen4core(ligfile,Hnumber,output):
	'''
--------------------------------------------------------
'gen4core' is used to generate ligand fragment
        usage: gen4core(ligfile,Hnumber,output)
        input : ligfile - ligand PDB file for generating ligand fragment
		Hnumber(str type) - the ATOM number of the HYDROGEN need to keep as the growth point
	output:	output -  the final ligand fragment PDB file
        	NOTICE: return the 'YES/NO' means whether the ligand fragment PDB is empty 
--------------------------------------------------------
'''
	F1 = open(ligfile,'r')
	F2 = open(output,'w+')
	reasonable = 'NO'
	for line in F1:
		if line.startswith('ATOM') or line.startswith('HETATM'):
			atom_number = line.split()[1]
			element_name = line.split()[-1]
			if element_name == 'H':
				if atom_number == Hnumber:
					reasonable = 'YES' 	
					F2.write(line)
				else:
					pass
			else:
				F2.write(line)
		else:
			F2.write(line)
	F1.close()
	F2.close()
	return reasonable
		
if __name__ == '__main__':
        gen4core('test_ligand.pdb','5625','lig_frag_1.pdb')





def count4ligH(ligfile):
        '''
--------------------------------------------------------
'count4ligH' is used to count ligand HYDROGENS.
        usage: count4ligH(ligfile)
        input : ligfile - ligand PDB file for counting HYDOGEN ATOMS. (usually in ./snapshot_E/point/lig.[1-4])
        output: return the hydrogen_list includes ALL the LIGAND HYDROGEN ATOM NUMBERs 
--------------------------------------------------------
'''
        hydrogen_list = []
        F = open(ligfile,'r')
        for line in F:
                if line.startswith('ATOM') or line.startswith('HETATM'):
                        atom_number = line.split()[1]
                        element_name = line.split()[-1]
                        if element_name == 'H':
                                hydrogen_list.append(atom_number)            #generating hydrogen_list store all ligand hydrogen atom numbers
                        else:
                                pass
                else:
                        pass
        ###########check whether the hydrigen_list is empty#########################
        if hydrogen_list == []:
                F1 = open('./gen4core.log','a')
                F1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' For ligand pdb file: '+ligfile+' there is no H in the pdb!\n')
                F1.close()
        else:
                return hydrogen_list

if __name__ == '__main__':
        A = count4ligH('test_ligand.pdb')
        print A
	
