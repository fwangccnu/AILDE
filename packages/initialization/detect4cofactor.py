#!/usr/bin/python
import os
import math
import decimal
import os

def distance(A,B):
        '''
--------------------------------------------------------
'distance' is used to calculate the distance between two atoms
        input : a complex PDB file.
        output: the distance number
--------------------------------------------------------
        '''

        POS1=A.split()
        POS2=B.split()
        decimal.getcontext().prec=4
        X1=decimal.Decimal(POS1[0])
        Y1=decimal.Decimal(POS1[1])                          #Define the function to calculate the distance between two atoms
        Z1=decimal.Decimal(POS1[2])
        X2=decimal.Decimal(POS2[0])
        Y2=decimal.Decimal(POS2[1])
        Z2=decimal.Decimal(POS2[2])
        DIS=math.sqrt((X1-X2)**2+(Y1-Y2)**2+(Z1-Z2)**2)
        return DIS

def detect4cofactor(complexpdb,ligname,outputdir):
	'''
--------------------------------------------------------
'detect4cofactor' is used to get cofactor pdb file around 5 anstrom around ligand
	input : a complex PDB file.
	output: complex pdb file under outputdir
--------------------------------------------------------
	'''

	def distance(A,B):

	        POS1=A.split()
	        POS2=B.split()
	        decimal.getcontext().prec=4
	        X1=decimal.Decimal(POS1[0])
	        Y1=decimal.Decimal(POS1[1])                          #Define the function to calculate the distance between two atoms
	        Z1=decimal.Decimal(POS1[2])
	        X2=decimal.Decimal(POS2[0])
	        Y2=decimal.Decimal(POS2[1])
	        Z2=decimal.Decimal(POS2[2])
	        DIS=math.sqrt((X1-X2)**2+(Y1-Y2)**2+(Z1-Z2)**2)
	        return DIS


	F1 = open(complexpdb,'r')
	for line in F1:
	        if line.startswith('ATOM') or line.startswith('HETATM'):
        	        res_name=line[17:20]
                	if res_name==ligname:
                        	LIGAND_CONFIRM=line[17:26]
                        	break
                	else:
                        	continue                #Extract the ligand coordinates of every atom
        	else:
                	continue
	F1.close()
	ligand_coord={}                    #The key is atom serial number(line[6:11]) and the value is atom coordinate(line[30:54])
	F2=open(complexpdb,'r')
	for line in F2:
        	if line.startswith('ATOM') or line.startswith('HETATM'):
                	res_info=line[17:26]
                	if res_info==LIGAND_CONFIRM:
                        	ligand_coord[line[6:11]]=line[30:54]
                	else:
                        	pass
        	else:
                	continue
	F2.close()
	
	############################################################################################################

	amber_res=['HIS','ALA','GLY','SER','THR','LEU','ILE','VAL','ASN','GLN','ARG','HID','HIE','HIP','TRP','PHE','TYR','GLU','ASP','LYS','LYN','PRO','CYS','CYM','CYX','MET','ACE','NME','ASH','GLH','Na+','Cl-','WAT','HOH','MN ']
	cofactor=[]
	for lig_coord in ligand_coord.values():
        	F3=open(complexpdb,'r')
        	for line in F3:
                	if line.startswith('ATOM') or line.startswith('HETATM'):
                        	if line[17:26]!=LIGAND_CONFIRM and line[17:20] not in amber_res:
                                	atom_coord=line[30:54]
                                	D=distance(lig_coord,atom_coord)               #get the information of cofactors
                                	if D<5 and line[17:26] not in cofactor:
                                        	cofactor.append(line[17:26])
                                	else:
                                        	pass
                	else:
                        	continue
        	F3.close()


	############################################################################################################

	if os.path.isdir(outputdir):
	        pass
	else:
        	os.system('mkdir -p ' + outputdir)

	for Y in cofactor:
        	Z=Y[:3]
        	if os.path.isfile('{outputdir}/{old_one}'.format(outputdir=outputdir,old_one=Z+'.pdb')):
                	os.remove('{outputdir}/{old_one}'.format(outputdir=outputdir,old_one=Z+'.pdb'))
        	else:
                	continue
	F4=open(complexpdb,'r')                  #Get cofactor file and save them in the directory  ./cofactor
	for line in F4:
        	if line[17:26] in cofactor:
                	F5=open('{outputdir}/{co_file}'.format(outputdir=outputdir,co_file=line[17:20]+'.pdb'),'a')
                	F5.write(line)
                	F5.close()
        	else:
                	continue

	#############################################################################

	scan_dir = os.listdir(outputdir)
	for ori_pdb in scan_dir:
		if ori_pdb.endswith('.pdb'):
			F6 = open(outputdir+'/'+ori_pdb,'r')
                	d = 0
                	for line in F6:
                		if line[77]!='H':
                        		d+=1
                        	else:
                                	continue
                	if d<6:
                		os.remove(outputdir+'/'+ori_pdb)              #Remove the ligand with the heavy atom<6
                	else:
                        	pass
		else:
			pass

	##############################################################################



if __name__ == '__main__':
	detect4cofactor('./1PWM_noH.pdb','FID','./cofactor')
	
