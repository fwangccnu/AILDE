#!/usr/bin/python
import os
def prep4lig(ligand,*charge):
	'''
--------------------------------------------------------
'top4lig' is used to DELETE ALL Hydrogens in the complex
        input : a ligand PDB file & charge type.
        output: ligand prep & crd file.
--------------------------------------------------------
	'''
	if charge == ():	
		charge_type = 'gas'
	else:	
		charge_type = charge[0]
	command = 'antechamber -i ligand.mol2 -fi mol2 -o ligand.prep -fo prepi -c ' + charge_type + r" -nc $(printf '%.0f\n' $(sed -n '/@<TRIPOS>ATOM/,/@<TRIPOS>BOND/p' ./ligand.mol2|awk '/ / {sum += $NF};END {print sum}')) -pf Y"
	print command, charge_type
	os.system(command)
	os.system('parmchk -i ligand.prep -f prepi -o ligand.frcmod')
