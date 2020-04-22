#!/usr/bin/python
import os
class parameter:
	def __init__(self):
		self.step = '01-15'
		self.complex = 'COM.pdb'
		self.ligand_name = 'LIG'
		self.ligand_charge = 'gas'
		self.parallel = 'YES'
		self.MDstart = '3'
		self.MDend = '15'
		self.mm_pbsa = './packages/files/mm_pbsa.in'	
		self.md_request = 'NO'	
		self.entropy = './packages/files/entropy/'
		self.substituent = {'01':'Br', '02':'CF3', '03':'CH3', '04':'Cl', '05':'COOH', '06':'F', '07':'NH2', '08':'NO2', '09':'OCH3', '10':'OH'}
		
		self.hydrogen_list = []
		self.lig_list = []

		path=os.getcwd()
		self.job_id = path.split('/')[-1]

	
	def initial(self,para_file):
		F=open(para_file,'r')
		for line in F:
			if line.startswith('step'):
				self.step = line.split()[1]
			elif line.startswith('complex'):
				self.complex = line.split()[1]
			elif line.startswith('ligand_name'):
				self.ligand_name = line.split()[1]
			elif line.startswith('ligand_charge'):
				self.ligand_charge = line.split()[1]
			elif line.startswith('parallel'):
				self.parallel = line.split()[1]
			elif line.startswith('MDstart'):
				self.MDstart = line.split()[1]
			elif line.startswith('MDend'):
				self.MDend = line.split()[1]
			elif line.startswith('mm_pbsa'):
				self.mm_pbsa = line.split()[1]
			elif line.startswith('md_request'):
				self.md_request = line.split()[1]
			elif line.startswith('entropy'):
				self.entropy = line.split()[1]
			else:
				pass
		F.close()


	def count4ligH(self,ligfile):
	        '''
--------------------------------------------------------
'count4ligH' is used to count ligand HYDROGENS.
        usage: count4ligH(ligfile)
        input : ligfile - ligand PDB file for counting HYDOGEN ATOMS. (usually in ./snapshot_E/point/lig.[1-4])
        output: return the hydrogen_list includes ALL the LIGAND HYDROGEN ATOM NUMBERs 
--------------------------------------------------------
'''
	        hydrogen = []
	        F = open(ligfile,'r')
	        for line in F:
	                if line.startswith('ATOM') or line.startswith('HETATM'):
	                        atom_number = line.split()[1]
	                        element_name = line.split()[-1]
	                        if element_name == 'H':
	                                hydrogen.append(atom_number)            #generating hydrogen_list store all ligand hydrogen atom numbers
	                        else:
	                                pass
	                else:
	                        pass
	        ###########check whether the hydrigen_list is empty#########################
	        if hydrogen == []:
	                F1 = open('./gen4core.log','a')
	                F1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' For ligand pdb file: '+ligfile+' there is no H in the pdb!\n')
	                F1.close()
	        else:
			self.hydrogen_list = hydrogen
	                return hydrogen

	
	def detectlig4list(self,comfile): 
                '''
--------------------------------------------------------
'detectlig4list' is used to detect ligand name.
        usage: detectlig4tuple(comfile)
        input : comfile - the complex pdb file for detecting.
        output: ligand 3 letters name LIST 
--------------------------------------------------------
'''

		amber_res=['HIS','ALA','GLY','SER','THR','LEU','ILE','VAL','ASN','GLN','ARG','HID','HIE','HIP','TRP','PHE','TYR','GLU','ASP','LYS','LYN','PRO','CYS','CYM','CYX','MET','ACE','NME','ASH','GLH','2HO']                    #Constrcut the list that includes residues which can be identify by AMBER
		lig = []
		F = open(comfile,'r')
		for line in F:
			if line.startswith('ATOM') or line.startswith('HETATM'):
				res_name = line[17:20]
				if res_name not in amber_res and res_name not in lig:
					lig.append(res_name)
				else:
					pass
			else:
				pass
		self.lig_list = lig
		return lig


	def update4sublist(self,listfile):
		'''
--------------------------------------------------------
'update4sublist' is used to generate a dictionary for substituent.
        usage: update4sublist(listfile)
        input : lsitfile - the list file record the substituent type, always ../lib/substituent/list.
        output: a dictionary {'01':'Br', '02':'CF3', '03':'CH3', '04':'Cl', '05':'COOH', '06':'F', '07':'NH2', '08':'NO2', '09':'OCH3', '10':'OH'} 
--------------------------------------------------------
'''
		F1 = open(listfile,'r')
		for line in listfile:
			if line.startswith('fragment'):
				num = line.split()[0].split('_')[1]
				type = line.split()[1].split('.')[0][1:]
				self.substituent[num] = type
			else:
				pass
