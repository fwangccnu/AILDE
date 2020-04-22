#!/usr/bin/python
import os
def gen4molpicture(input_file,file_type,outputdir):
	'''
--------------------------------------------------------
'gen4molpicture' is used to generate ligand molecule picture (jpg format)
        usage: gen4molpicture(input_file,file_type,output_file)
        input : input_file - ligand mol2/pdb format file
                file_type - tell the ligand file type, mol2/pdb
		outputdir - tell where to sotre the smi and jpg file
        output: output - the smile file and jpg picture file
--------------------------------------------------------
'''
	name = input_file.split('/')[-1].split('.')[0]
	os.system('babel -i{file_type} {input_file} -osmi {outputdir}/{name}.smi'.format(file_type=file_type,input_file=input_file,outputdir=outputdir,name=name))
	os.system('unset DISPLAY && molconvert -Y "jpeg:w500,Q95,#ffffff" {outputdir}/{name}.smi -o {outputdir}/{name}.jpg'.format(outputdir=outputdir,name=name))


