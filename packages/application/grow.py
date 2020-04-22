#!/usr/bin/python
import time
import os
import sys
def grow4lead(core,substituent,classpath,outputdir):
	'''
--------------------------------------------------------
'grow4lead' is used to link core and substituent together
        usage: grow4lead(core,substituent,classpath,outputdir)
        input : core - the core file, it will be check by grow4lead to see whether it just has ONE HYDROGEN or whether 
			it is EMPTY. It will be record in the grow.log file if it has problems
                substituent - it will be checked whether it exists
                classpath - the java class path, default is in the ./packages/lib/autogrow_class/
		outputdir - the outputdir should not exists, otherwise it will stop! 
        output: if any of the core, substituent and outputdir has problems, the GROW PROGRAM WILL NOT be DONE!!!!!!!!!!!
		information WILL BE RECORD in grow.log
                NOTICE: return the 'YES/NO' means whether the grow work be DONE!!!
--------------------------------------------------------
'''
        ####################1.check output dir whether exists######################################################################
	if os.path.isdir(outputdir):
		print 'the',outputdir,'has been exist! please ROMOVE it!'
		sys.exit(0)                                                             #check whether the output directory exists!
	else:
		os.system('mkdir -p {outputdir}'.format(outputdir = outputdir))
        ####################2.check whether the core file exists or empty, if any wrong, record in the grow.log file###############
	core_resonable = 0
	if os.path.isfile(core):
		F1 = open(core,'r')
		for line in F1:
			if line.startswith('ATOM') or line.startswith('HETATM'):
				element_name = line.split()[-1]
				if element_name == 'H':
					core_resonable+=1
				else:
					pass
			else:
				pass
		F1.close()
		if core_resonable == 1:
			pass
		else:
			F2 = open('./grow.log','a')
			F2.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' For core pdb file: '+core+' there is no grow point H!\n')
			F2.close()
	else:
		F2 = open('./grow.log','a')
		F2.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' For core pdb file: ' + core + ' it does not exists!\n')
		F2.close()
	####################3.check whether the substituent exists##################################################################
	sub_resonable = 0
	if os.path.isdir(substituent):
		sub_resonable = 1
	else:
		pass
	####################4.generate parameter file and execute grow program######################################################
	if core_resonable == 1 and sub_resonable == 1:
		F3 = open('./grow.prm','w+')
		F3.write('//DIRECTORIES\n')
		F3.write('working root directory: {outputdir}\n'.format(outputdir = outputdir))
		F3.write('fragments directory: {substituent}\n'.format(substituent = substituent))
		F3.write('scripts directory: /yp_home/user/soft/Autogrow2.0/scripts\n')
		F3.write('\n')
		F3.write('//INPUT FILES\n')
		F3.write('initial ligand: {core}\n'.format(core = core))	
		F3.write('\n')
		F3.write('//EVOLUTION PARAMETERS\n')
		content = '''number of carryovers: 1
number of children: 1
number of mutants: 1
max number atoms: 500
receptor radius: 10
number of generations: 1
'''		
		F3.write(content)
		F3.close()
		os.system('java -cp {classpath} Main -run_mode Execute -parm_file grow.prm >/dev/null 2>&1'.format(classpath = classpath))  #perform the grow program for core and substituent
		DONE = 'YES'
	else:
		DONE = 'NO'
	####################5.return whether the work finished#####################################################################
	return DONE

if __name__ == '__main__':
	A = grow4lead('pfvs_core.pdb','./fragment/fragment_02/','./autogrow_class','./temp')
	print A
