#!/yp_home/public/soft/system_soft/PYTHON/2.7.9/bin/python
import sys
import os
import fnmatch
import shutil
import time
import linecache
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import random

sys.path.insert(0,'./packages')

from packages.parameter.parameter import parameter
from packages.initialization.detect4cofactor import detect4cofactor
from packages.initialization.delete_H import del_H
from packages.initialization.clean_pdb import clean
from packages.initialization.prep4ligand import prep4lig
from packages.initialization.gen4tleap import *
from packages.initialization.gen4min import *
from packages.application.min_run import sander4minWT
from packages.initialization.gen4md import *
from packages.application.md_run import pmemd4mdWT
from packages.initialization.gen4trajectory import *
from packages.application.refine_run import *
from packages.application.split_run import splitcom2subitems
from packages.initialization.gen4mmpbsa import mmpbsa4energy
from packages.initialization.gen4tleap import tleap4nowat2pbsa
from packages.application.mmpbsa_run import mmpbsa4cal
from packages.initialization.gen4entropy import *
from packages.initialization.gen4newdir import gen4newdir
from packages.application.entropy_run import calculation4entropy
from packages.initialization.gen4replacelist import gen4replacelist
from packages.initialization.gen4replacelist import deal4num
from packages.application.gen4core import gen4core
from packages.application.grow import grow4lead
from packages.application.deal4newlig import deal4newlig
from packages.result.extract4energy import *
from packages.result.gen4molpicture import gen4molpicture
from packages.result.extract4energy import *
from packages.result.cal4activefold import *
from packages.initialization.rm4oldfile import rm4oldfile
from packages.result.extract4Hinfo import extract4Hinfo
from packages.result.extract4Hinfo import extract4Hscore
from packages.initialization.detect4error import *
from packages.result.gen4heatmap import *


########################0.Read parameters and update task status#########################################################

input = parameter()
input.initial(sys.argv[1])                    #read input, catch options
input.update4sublist('./packages/lib/substituent/list')    #read the substituent file

step = input.step                             #start calculation from which step
complex_file = input.complex                  #get complex file
ligand_name = input.ligand_name               #get ligand_name
ligand_charge = input.ligand_charge           #get ligand charge type
parallel = input.parallel                     #whether to use parallel during min and MD
MDSTART = input.MDstart                       #MD job start number 
MDEND = input.MDend                           #MD job end
md_request = input.md_request                 #whether need md on the snapshots
template_pbsa = input.mm_pbsa                 #template pbsa file locations
entropy_file = input.entropy                  #template entropy file locations
substituent = input.substituent
job_id = input.job_id

print 'Read Input File From:', '\t',sys.argv[1]
print 'steps          ','\t',step
print 'complex        ','\t',complex_file
print 'ligand_name    ','\t',ligand_name
print 'ligand_charge  ','\t',ligand_charge
print 'parallel       ','\t',parallel
print 'MDSTART        ','\t',MDSTART
print 'MDEND          ','\t',MDEND
print 'md_request     ','\t',md_request
print 'template_pbsa  ','\t',template_pbsa
print 'entropy_file   ','\t',entropy_file
print 'substituent    ','\t',substituent
print 'job_id         ','\t',job_id     


EXECUTION = deal4num(step)                   #read the steps need to be Executed. 

STEP_LIST = '''###################STEP LIST########################################################################
#####0.Read parameters
#####01.deal with the complex
#####02.generate parameter file for WT min run
#####03.run min step for WT
#####04.generate parameter file for WT MD run
#####05.run MD step for WT
#####06.deal with the trajectory
#####07.generate files snapshots refine
#####08.perform the refine for WT snapshots
#####09.generate crd files and in file for mm_pbsa
#####10.perform the mm_pbsa calculation
#####11.prepare files for WT entropy calculation
#####12.perform WT entropy calculation and get the final delta_g
#####13.get replacelist.prm file for substituent optimization
#####14.Read replace.prm into a dictionary
#####!!!!!!!! 15.Perform the Substituent Optimization !!!!!!!!
#####16.First to generate the wt molecule {LIG}.smi/jpg/pdb in ./result/main/
#####17.Second to generate the first table which display all the compound energy
#####18.@!!generate table2.result and heatmap.result by extracting information from table1.result!!@
#####19.@!!generate heatmap.input and heatmap picture!!@
####################################################################################################
'''

F = open('EXECUTION.txt','w+')	              #got a file EXECUTION.txt for checking step list
F.write(STEP_LIST)
F.write('\n')
F.write('################FOLLOWING STEP(S) WILL BE EXECUTED####################')
F.write('\n')
F.write(step)
F.close()

rm4oldfile('./total.error')                 #remove the old error log file


########################01.deal with the complex######################################################################### 

if '01' in EXECUTION:
	#print del_H.__doc__
	complex_noH = del_H(complex_file)     #delete Hydrogens to get complex_file_noH.pdb

	detect4cofactor(complex_noH,ligand_name,'./cofactor')  #get cofactor pdb and store in ./cofactor
	rm4oldfile('./out.zip')	
	os.system('cp ./packages/initialization/PARA_GEN_all.SH ./')  #generate cofactor prep and frcmod file(s)
	os.system('/bin/bash PARA_GEN_all.SH')                        #and store in out.zip

	clean(complex_noH,ligand_name)        #clean pdb 

else:
	pass

########################02.generate parameter file for WT min run#########################################################

if '02' in EXECUTION:
	prep4lig('ligand.mol2',ligand_charge)                                                #calculate ligand prep and frcmod 

	os.system('cp {entropy_file}/h2o.prep ./'.format(entropy_file = entropy_file))       #cp h2o.prep to ./ for tleap.in to load
	tleap4wat2md('complex.pdb','tleap.in','./')                                          #generate complex top and crd for amber MD
	os.system('tleap -f tleap.in')
	os.system('ambpdb -p complex.top -c complex.crd > complex_start.pdb -aatm')          #get complex_start.pdb

	AA = detect('complex_start.pdb')                                                     #AA is the total residue number, int type
	sander4watmin1()
	sander4watmin2(AA)                                                                   #generate minimazation input file
	sander4watmin3()
	
	#perform a judge step###########################################
	if 'NO' not in [detect4error('./ligand.prep',800),detect4error('./complex.top',8000),detect4error('./complex.crd',5000)]:
		pass
	else:
		error2log('./total.error','error in step 2 --- generate parameter file for WT min run')
		sys.exit(0)
else:
	pass



########################03.run min step for WT############################################################################

if '03' in EXECUTION:
	sander4minWT('complex_wat.top','complex_wat.crd',parallel)                           #perform the min_run for WT


        #perform a judge step###########################################
        if detect4error('./min3.out',5000) == 'YES':
                pass
        else:
                error2log('./total.error','error in step 3 --- run min step for WT')
		sys.exit(0)

else:
	pass

#######################04.generate parameter file for WT MD run###########################################################

if '05' in EXECUTION:
	AA = detect('complex_start.pdb')                                                     #AA is the total residue number                                                      
										     	     #generate md input file  
	md4watmd1(AA)                                                                        #10ps for md1.in
	md4watmd2()                                                                          #500ps for md2.in
	md4watmd3()                                                                          #200ps for every md3.in

else:
	pass

#######################05.run MD step for WT###############################################################################

if '06' in EXECUTION:
	pmemd4mdWT('complex_wat.top','min3.rst',MDSTART,MDEND,parallel)                      #perform the md_run for WT

else:
	pass

#######################06.deal with the trajectory#########################################################################

if '06' in EXECUTION:
	AA = detect('complex_start.pdb')                                                     #AA is the total residue number

	cpptraj4combine('combine_crd.in',MDEND,AA)                                           #generate combine_crd.in file 
	os.system('cpptraj -p complex_wat.top <combine_crd.in')                              #get md.crd 

	cpptraj4rms('md1.cal_rms',AA)                                                        #generate md1.cal_rms file
	os.system('cpptraj -p complex.top <md1.cal_rms')                                     #get rms-backbone.rms and rms-lig.rms

	total_MDtime = 10 + 500 + (int(MDEND) - 2)*200
	print total_MDtime,'ps' 
	endtime = total_MDtime/1000*1000                                                     #round down  e.g. 3150/1000*1000=3000
	starttime = endtime - 99                                                             #canbe modified to get different number of snapshots
	step = 25
	cpptraj4snapshots('nowat_com.in','snapshot_E',str(starttime),str(endtime),str(step)) #generate nowat_com.in file
	os.system('cpptraj -p complex.top <nowat_com.in')                                    #get com.rst.* & com.pdb.* , stored in ./snapshot_E

        #perform a judge step###########################################
        if detect4error('./md.crd',10000) == 'YES':
                pass
        else:
                error2log('./total.error','error in step 6 --- run MD step for WT')
                sys.exit(0)

else:
	pass

######################07.generate files snapshots refine#####################################################################

if '07' in EXECUTION:
	AA = detect('complex_start.pdb')                                                     #AA is the total residue number

	sander4Nowatminside(AA)                                                              #generate min_snap_side.in, ntb=0
	sander4Nowatminsnap()                                                                #generate min_snap.in, ntb=0

	if md_request == 'NO':
		pass
	else: 
		md4Nowatmdsnap('10000',AA)                                                  #get md_snap.in, time is 10ps, fix backbone

else:
	pass

######################08.perform the refine for WT snapshots##################################################################

if '08' in EXECUTION:
	os.system('cp ./packages/application/refine_run.sh ./')
	os.system('cp ./packages/application/refine_run.py ./')
	os.system('/bin/bash refine_run.sh com.rst ./snapshot_E ./complex.top {md_request} {parallel}'.format(md_request=md_request,parallel=parallel))

        #perform a judge step###########################################
        if detect4error('./snapshot_E/com.crd.1',5000) == 'YES':
                pass
        else:
                error2log('./total.error','error in step 8 --- perform the refine for WT snapshots')
                sys.exit(0)


else:
	pass

######################09.generate crd files and in file for mm_pbsa###########################################################

if '09' in EXECUTION:
	crddir = os.listdir('./snapshot_E')
	destination = './snapshot_E/point'
	for crd in crddir:
		if fnmatch.fnmatch(crd,'com.crd.*'):
			number = crd.split('.')[-1]
			splitcom2subitems('./snapshot_E/'+crd,ligand_name,destination,'com.'+number,'rec.'+number,'lig.'+number)
								                     	     #split com.crd.* into com.*/rec.*/lig.* and store in ./snapshot_E/point
		else:
			pass
	pdbdir = os.listdir(destination)
	for comfile in pdbdir:
		if fnmatch.fnmatch(comfile,'com.*'):
			number = comfile.split('.')[-1]
			tleap4nowat2pbsa('tleap2.in',comfile,'rec.'+number,'lig.'+number,'delta_E_com.crd.'+number,'delta_E_rec.crd.'+number,'delta_E_lig.crd.'+number,destination)
										     	     #generate tleap2.in file
			os.system('tleap -f tleap2.in')                                      #get {complex/recetop/ligand}.top and crd file for delta_E_{com/rec/lig.crd}.* and store in ./snapshot_E/point

	mmpbsa4energy(template_pbsa,'mm_pbsa.in',parallel,destination,destination+'/'+'complex.top',destination+'/'+'receptor.top',destination+'/'+'ligand.top')
							                                     #get mm_pbsa.in file for calculation
else:
	pass

######################10.perform the mm_pbsa calculation########################################################################

if '10' in EXECUTION:
	mmpbsa4cal('mm_pbsa.in','./snapshot_E/')                                             #use mm_pbsa.in as input file, and store the result in ./snapshot_E

        #perform a judge step###########################################
        if detect4error('./snapshot_E/delta_E_statistics.out',500) == 'YES':
                pass
        else:
                error2log('./total.error','error in step 11 --- perform the mm_pbsa calculation')
                sys.exit(0)

else:
	pass

######################11.prepare files for WT entropy calculation##################################################################

if '11' in EXECUTION:
	entropycal_dir = './snapshot_E/entropy_cal'                                          #specify the dir to perform entropy calculation 

	gen4newdir(entropycal_dir)                                                           #generate directory './snapshot_E/entropy_cal'

	os.system('cp {entropy_file}/* {cal_dir}'.format(entropy_file=entropy_file,cal_dir=entropycal_dir))     #1.copy all lib files from entropy_file to entropycal_dir

	os.system('cp ./ligand.prep {cal_dir}'.format(cal_dir=entropycal_dir))                                  #2.copy ligand prep file to entropycal_dir

	if os.path.isdir('confactors_para'):
		gen4newdir(entropycal_dir+'/confactor_prep')                                 #generate directory './snapshot_E/entropy_cal/confactor_prep'
		os.system('cp ./confactors_para/*prep {cal_dir}/confactor_prep'.format(cal_dir=entropycal_dir)) #3.copy cofactor prep file to entropy_dir/confactor_prep
	else:
		pass

	os.system('cp ./snapshot_E/point/*top {cal_dir}'.format(cal_dir=entropycal_dir))                        #4.copy ./snapshot_E/point/*top to entropy_dir
	os.system('cp ./snapshot_E/point/delta_E_com.crd.* {cal_dir}'.format(cal_dir=entropycal_dir)) 
	os.system('cp ./snapshot_E/point/delta_E_rec.crd.* {cal_dir}'.format(cal_dir=entropycal_dir))           #5.copy ./snapshot_E/point/delta_E_{com/rec/lig}.crd.* to entropy_dir
	os.system('cp ./snapshot_E/point/delta_E_lig.crd.* {cal_dir}'.format(cal_dir=entropycal_dir)) 

	entropy4filesin(entropycal_dir)                                                      #generate files.in file store in entropycal_dir

	lig_list = input.detectlig4list('./complex_start.pdb')                               #get all ligand for use of entropy calculation
	lig_list.remove(ligand_name) 
	entropy4nmodes(entropycal_dir,'complex.top','receptor.top','ligand.top',lig_list)     #generate nmode_S file store in entropycal_dir 
                                  #notice: top and crd file should be in entropycal_dir before generate nmode_S, and delete the co-factor when calculate entropy

else:
	pass

######################12.perform WT entropy calculation and get the final delta_g###################################################
 
if '12' in EXECUTION:
	enthaipy_dir = './snapshot_E/'                                                	     #the delta_E_statistics.out has been put in enthaipy_dir
	entropycal_dir = './snapshot_E/entropy_cal'

	calculation4entropy(entropycal_dir)                                                  #perform the ./nmode_S for WT to get ds.out in entropycal_dir

	os.system('cp {entropycal_dir}/ds.out {enthaipy_dir}'.format(entropycal_dir = entropycal_dir, enthaipy_dir = enthaipy_dir)) #copy ds.out from entropycal_dir to enthaipy_dir
	os.system('cp {entropy_file}/average {enthaipy_dir}'.format(entropy_file = entropy_file,enthaipy_dir = enthaipy_dir))       #copy average from entropy_file dir to enthaipy_dir
	os.system('cp {entropy_file}/ds1.awk {enthaipy_dir}'.format(entropy_file = entropy_file,enthaipy_dir = enthaipy_dir))       #copy ds1.awk from entropy_file dir to enthaipy_dir

	path = os.getcwd()
	os.chdir(enthaipy_dir)
	os.system('./average')                                                               #run average to get delta_g.out
	os.chdir(path)

        #perform a judge step###########################################
	check4wtenergy  = check4energyfile(enthaipy_dir + 'delta_E_statistics.out',enthaipy_dir + 'ds.out')  #check whether the dH_file and dS_file of wt are resonable
	if 'NO' not in check4wtenergy:
		pass
	else:
		error2log('./total.error','error in step 12 --- perform WT entropy calculation and get the final delta_g')
		sys.exit(0)
else:
	pass

######################BEGIN the SUBSTITUENT OPTIMIZATION STEP!!!!!###################################################################
#####################################################################################################################################
######################13.get replacelist.prm file for substituent optimization#######################################################
       # NOTICE here: here can add another way to generate replacelist.prm which H ATOM NUMBER and SUBSTITUENT TYPE can be specified
       # if need to grow AT TWO HYDROGENS AT the SAME TIME, here need to design a new method to write the replacelist.prm

if '13' in EXECUTION:
	hydrogens = input.count4ligH('./snapshot_E/point/lig.1')                             #get ALL ligand hydrogen ATOM NUMBER and store in LIST - hydrogens
	gen4replacelist(hydrogens,'./packages/lib/substituent/list')                         #generate the replacelist.prm file record H ATOM NUMBER and SUBSTITUENT TYPE for substituent optimization  

else:
	pass

######################14.Read replace.prm into a dictionary###########################################################################

if '14' in EXECUTION:
	CALCULATION_LIST = {} 
	F1 = open('./replacelist.prm') 
	for line in F1:
		if line.startswith('TYPE'):
			H_NUM = line.split()[2]                                              #H_NUM is just like '5595'
			SUB_TYPE = line.split()[3]                                           #SUB_TYPE is just like '01-03,04,06,07-10' 
			SUB_TYPE_LIST = deal4num(SUB_TYPE)                                   #use deal4num to deal SUB_TYPE into a list, looks like ['01','02','03','04','06','07','08','09','10']
			CALCULATION_LIST[H_NUM] = SUB_TYPE_LIST	                             #write H_NUM and SUB_TYPE_LIST into the dictionary CALCULATION_LIST
							#the CALCULATION_LIST is just like {'5595':['01','02','03','04','06','07','08','09','10'],'5598':['01','02']}
							#key: means the Hydrogen Number, value: means substituent group number
		else:
			pass

	print CALCULATION_LIST

else:
	pass

##################!!!!!!!! 15.Perform the Substituent Optimization !!!!!!!!###########################################################

if '15' in EXECUTION:
	subdir = './snapshot_sub' 
	gen4newdir(subdir)                                                          #generate directory './snapshot_sub'
	
		##############outer circulation for every H number############################################################################
	for (key,value) in CALCULATION_LIST.items():
	
		coredir = './snapshot_sub/' + key + '/core'                         #the directory for storing core pdb
		gen4newdir(coredir)                                                 #mkdir a directory under ./snapshot_sub/{H_number}/core to store core pdb(multiple snapshots)
		
		lig_dir = os.listdir('./snapshot_E/point/')
		for file in lig_dir:
			if file.startswith('lig.'):
				NUM = file.split('.')[1]
				gen4core('./snapshot_E/point/'+file,key,coredir+'/core.'+NUM)  #generate core pdb of all snapshots for the key H_number,and store in ./snapshot_sub/{H_number}/core/core.*
			else:
				pass
	
		recdir = './snapshot_sub/' + key + '/rec'                           #the directory for storing receptor pdb will be used later to form new complex
		gen4newdir(recdir)                                                  #mkdir a directory under ./snapshot_sub/{H_number}/rec to store receptor pdb(multiple snapshots)
		os.system('cp ./snapshot_E/point/rec.* {recdir}'.format(recdir = recdir))
		##############inner circulation for every fragment############################################################################
		for frag in value:
	
			workdir = './snapshot_sub/' + key + '/' + frag              #workdir ./snapshot_sub/{H_number}/{frag_number} for every calculation  
			gen4newdir(workdir)                                         #generate directory ./snapshot_sub/{H_number}/{frag_number}
	
			path = os.getcwd()
			os.chdir(path+'/snapshot_sub/'+key+'/'+frag)                #change directory to workdir './snapshot_sub/{H_number}/{frag_number}'
			newligdir = './new_ligand'
			gen4newdir(newligdir)                                       #mkdir a new directory './snapshot_sub/{H_number}/{frag_number}/new_ligand' for sotring growing result



		        if detect4error('./com.crd.1',8000) == 'YES':
				pass                                                #delete <8KB com.crd.1 file
			else:
				os.system('rm com.crd.1')

	
			####begin to do the grow step!!!!######################################################################################	

			if not os.path.isfile('com.crd.1'):
				core_dir = os.listdir('../core')                            #specify the core directory, prepare for grow
				wrong_grow = []                                             #define a list to store wrong grow NUM
				for file in core_dir:
					if file.startswith('core.'):
						NUM = file.split('.')[1]
						DONE = grow4lead('../core/'+file, path+'/packages/lib/substituent/fragment_'+frag, path+'/packages/lib/autogrow_class/', newligdir+'/'+NUM)
											    #this step finish the grow step, grow4lead(core,substituent,classpath,outputdir), core is stored in './snapshot_sub/{H_number}/core', substituent and classpath come from packages/lib, outputdir is './snapshot_sub/{H_number}/{frag_number}/new_ligand/{NUM}' split by different snapshot number, DONE is YES or NO, means whether the grow work be DONE!!!
						if DONE == 'YES':
							pass
						else:
							wrong_grow.append(NUM)              #collect unfinished grow of their dirctory name 
							F2 = open('./grow4lead.log','a')    #creat 'grow4lead.log' file under workdir to record the wrong grow    
							F2.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +' For grow work: ./new_ligand/'+NUM+' is not finished!\n')
							F2.close()				
					else:
						pass                                       
				
				####new ligand needs to deal############################################################################################
				finalligdir = './final_ligand'
				gen4newdir(finalligdir)                                     #mkdir a new directory './snapshot_sub/{H_number}/{frag_number}/final_ligand' for sotring final ligand    
				oldligdir = os.listdir(newligdir)
				for dir in oldligdir:
					try:
						deal4newlig(newligdir + '/' + dir + '/generation_1/ligand2.pdb',finalligdir + '/lig.' + dir)
											    #this step is to deal with the obtained ligand, because there are some problems about the directly growed ligand,the deal4newlig(ligfile,outputlig) define 1. './new_ligand/{NUM}/generation_1/ligand2.pdb'	as the input ligand. 2. './final_ligand/lig.{NUM}' as the output ligand.
					except:
						os.system('cp {fligdir}/lig.1 {fligdir}/lig.{dir}'.format(fligdir=finalligdir,dir=dir))
				####generate ligand prep file###########################################################################################
				os.system('babel -h -ipdb ./{finalligdir}/lig.1 -omol2 ligand.mol2 -p 7 >/dev/null 2>&1'.format(finalligdir = finalligdir)) #here just use './final_ligand/ligand_final_1_.pdb' to get the ligand prep file.
				prep4lig('ligand.mol2',ligand_charge)                       #use prep4lig(ligand,*charge) to calculate ligand.prep and ligand.frcmod
				
				####generate snapshots for new complex##################################################################################
				newpoint = './point_before_refine'
				gen4newdir(newpoint)                                        #mkdir new directory './snapshot_sub/{H_number}/{frag_number}/point' for sotring new com pdb, top, crd
				os.system('cp ../../../h2o.prep ./')                        #cp h2o.prep to './snapshot_sub/{H_number}/{frag_number}/' for tleap3
				if os.path.isdir('../../../confactors_para'):
					os.system('cp -r ../../../confactors_para ./')      #cp confactors_para to './snapshot_sub/{H_number}/{frag_number}/' if needed
				else:
					pass
				os.system('cp {finalligdir}/lig.* {newpoint}'.format(finalligdir = finalligdir,newpoint = newpoint)) #copy final ligand snapshots lig.* to './snapshot_sub/{H_number}/{frag_number}/point_before_refine'
				os.system('cp ../rec/rec.* {newpoint}'.format(newpoint = newpoint)) #copy rec.* pdb snapshot to './snapshot_sub/{H_number}/{frag_number}/point_before_refine'
				pointdir = os.listdir(newpoint)
				for file in pointdir:
					if fnmatch.fnmatch(file,'lig.*'):
						NUM = file.split('.')[1]
						F1 = open(newpoint+'/com.'+NUM,'w+')        #write com.* to './snapshot_sub/{H_number}/{frag_number}/point_before_refine'
						F2 = open(newpoint+'/rec.'+NUM,'r')
						for line2 in F2:
							if line2.startswith('END'):
								pass
							else:
								F1.write(line2)
						F2.close()
						F3 = open(newpoint+'/'+file,'r')
						for line3 in F3:
							if line3.startswith('END'):
								pass
							else:
								F1.write(line3)
						F3.close()
						F1.write('END\n')
						F1.close()
		
						####generate tleap3.in and tleap to get complex.top and complex.crd store in ./point_before_refine###########
						tleap4nowat2pbsa('tleap3.in', 'com.'+NUM, 'rec.'+NUM, 'lig.'+NUM, 'complex2.crd.'+NUM, 'receptor2.crd.'+NUM, 'ligand2.crd.'+NUM, newpoint) #use tleap4nowat2md(com,filename,path) to get complex.top, complex2.crd.* stored in ./point_before_refine, also with the receptor and ligand top and crd file but useless
						os.system('tleap -f tleap3.in')
					else:
						pass
		
				os.system('cp {newpoint}/complex2.crd.* ./'.format(newpoint = newpoint)) #copy './snapshot_sub/{H_number}/{frag_number}/point_before_refine/complex2.crd.*' to './snapshot_sub/{H_number}/{frag_number}/' 		
				os.system('cp {newpoint}/*.top ./'.format(newpoint = newpoint))          #copy './snapshot_sub/{H_number}/{frag_number}/point_before_refine/*.top' to './snapshot_sub/{H_number}/{frag_number}/' 		
		
				####genertate files for sub type snapshots refine#######################################################################
		
				AA = detect(newpoint + '/rec.1') + 1
				sander4Nowatminside(AA)                                      #generate min_snap_side.in, ntb=0
				sander4Nowatminsnap()                                        #generate min_snap.in, ntb=0
		
				if md_request == 'NO':
		        		pass
				else:
		        		md4Nowatmdsnap('10000',AA)                           #get md_snap.in, time is 10ps, fix backbone
		
				####perform the sub type refine step####################################################################################

			        os.system('cp ../../../packages/application/refine_run.sh ./')
			        os.system('cp ../../../packages/application/refine_run.py ./')
	
				os.system('/bin/bash refine_run.sh complex2.crd ./ ./complex.top {md_request} {parallel}'.format(md_request=md_request,parallel=parallel))		

			else:
				pass
		
			####generate crd files and in file of sub type snapshots for mm_pbsa####################################################
	
			crddir = os.listdir('./')
			destination = './point_after_refine'
			for crd in crddir:
			        if fnmatch.fnmatch(crd,'com.crd.*'):
			                number = crd.split('.')[-1]
			                splitcom2subitems('./'+crd,'LIG',destination,'com.'+number,'rec.'+number,'lig.'+number)
			                                                                                     #split com.crd.* into com.*/rec.*/lig.* and store in 'point_after_refine'
			        else:
			                pass
			pdbdir = os.listdir(destination)
			for comfile in pdbdir:
			        if fnmatch.fnmatch(comfile,'com.*'):
			                number = comfile.split('.')[-1]
			                tleap4nowat2pbsa('tleap4.in',comfile,'rec.'+number,'lig.'+number,'delta_E_com.crd.'+number,'delta_E_rec.crd.'+number,'delta_E_lig.crd.'+number,destination)
			                                                                                     #generate tleap2.in file
			                os.system('tleap -f tleap4.in')          #get {complex/recetop/ligand}.top and crd file for delta_E_{com/rec/lig.crd}.* and store in 'point_after_fefine'
			
			mmpbsa4energy('../../../mm_pbsa.in','mm_pbsa2.in',parallel,destination,destination+'/'+'complex.top',destination+'/'+'receptor.top',destination+'/'+'ligand.top')
	                                                                         #get mm_pbsa2.in file for calculation
	
			####perform the mm_pbsa calculation for sub type########################################################################
			
			energydir = './energy_cal'	
	                gen4newdir(energydir)                                    #mkdir new directory './snapshot_sub/{H_number}/{frag_number}/point' for sotring new com pdb, top, crd	
			mmpbsa4cal('mm_pbsa2.in',energydir)                      #use mm_pbsa2.in as input file and store result in './snapshot_sub/{H_number}/{frag_number}/energy_cal' directory
	
			####prepare files for sub type entropy calculation######################################################################
			
			entropycal_dir = './entropy_cal'                         #specify the dir to perform entropy calculation 
			gen4newdir(entropycal_dir)                               #generate directory './snapshot_sub/{H_number}/{frag_number}/entropy_cal'
			
			os.system('cp ../../../packages/files/entropy/* {cal_dir}'.format(cal_dir=entropycal_dir))                    #1.copy all lib files from entropy_file to entropycal_dir
			os.system('cp ./ligand.prep {cal_dir}'.format(cal_dir=entropycal_dir))                                  #2.copy ligand prep file to entropycal_dir
			
			if os.path.isdir('confactors_para'):
			        gen4newdir(entropycal_dir+'/confactor_prep')       #generate directory 'entropy_cal/confactor_prep'
			        os.system('cp ./confactors_para/*prep {cal_dir}/confactor_prep'.format(cal_dir=entropycal_dir)) #3.copy cofactor prep file to entropy_dir/confactor_prep
			else:
			        pass
			
			os.system('cp {destination}/*top {cal_dir}'.format(destination=destination,cal_dir=entropycal_dir))                        #4.copy ./point_after_refine/*top to entropy_dir
			os.system('cp {destination}/delta_E_com.crd.* {cal_dir}'.format(destination=destination,cal_dir=entropycal_dir))
			os.system('cp {destination}/delta_E_rec.crd.* {cal_dir}'.format(destination=destination,cal_dir=entropycal_dir))           #5.copy ./point_after_refine/delta_E_{com/rec/lig}.crd.* to entropy_dir
			os.system('cp {destination}/delta_E_lig.crd.* {cal_dir}'.format(destination=destination,cal_dir=entropycal_dir))
			
			entropy4filesin(entropycal_dir)   #generate files.in file store in entropycal_dir

		        lig_list = input.detectlig4list('../../../complex_start.pdb')                               #get all ligand for use of entropy calculation
        		lig_list.remove(ligand_name)
        		entropy4nmodes(entropycal_dir,'complex.top','receptor.top','ligand.top',lig_list) #generate nmode_S file store in entropycal_dir 
	                                  #notice: top and crd file should be in entropycal_dir before generate nmode_S
	
			####perform sub type entropy calculation and get the final delta_g######################################################
			
			calculation4entropy(entropycal_dir)                                           #perform the ./nmode_S for WT to get ds.out in entropycal_dir
			
			os.system('cp {entropycal_dir}/ds.out {energydir}'.format(entropycal_dir = entropycal_dir, energydir = energydir)) #copy ds.out from 'entropy_cal' to 'energy_cal'
			os.system('cp {entropycal_dir}/average {energydir}'.format(entropycal_dir = entropycal_dir,energydir = energydir)) #copy average from 'entropy_cal' dir to 'energy_cal'
                        os.system('cp {entropycal_dir}/ds1.awk {energydir}'.format(entropycal_dir = entropycal_dir,energydir = energydir)) #copy ds1.awk from 'entropy_cal' dir to 'energy_cal'

			os.chdir(energydir)
			os.system('./average')                                                        #run average to get delta_g.out
			os.chdir(path)

else:
	pass


	
#########################Begin to extract result######################################################################################

######################16.First to generate the wt molecule {LIG}.smi/jpg/pdb in ./result/main/########################################

if '16' in EXECUTION:
	result_dir = './result/'
	gen4newdir(result_dir)                                   #make new directory './result' for storing all the result file

	result_main = result_dir + '/main/'
	gen4newdir(result_main)                                  #make new directory './result/main' for storing ligand-related result file

	try:
		lig_size = os.path.getsize('./snapshot_E/point/lig.1') 
	except:
		Fmain = open(result_main+'/main.log','w')
		Fmain.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + './snapshot_E/point/lig.1 does not exist, no way to generate picture\n')
		Fmain.close()
		sys.exit(0)                                      #exit program  

	if lig_size > 972:                                       #judge whether the lig.1 size is empty or not suitable
		os.system('cp ./snapshot_E/point/lig.1 '+result_main+ligand_name+'.pdb')
	        path = os.getcwd()
	        os.chdir(path+'/result/main/')                   #change directory to workdir './result/main/'
	        gen4molpicture(ligand_name+'.pdb','pdb','./')    #generate {LIG}.smi and {LIG}.jpg
	        os.chdir(path)
	else:
	        pass

else:
	pass
				
######################17.Second to generate the first table which display all the compound energy#####################################

######################File name: table1.result########################################################################################
######################Include Following Fields:
######################1. smile   : molecule smile information#########################################################################
######################2. fragment: which fragment is used to link to the original ligand##############################################
######################3. hydrogen: which hydrogen is used to link the fragment########################################################
######################4. ddH     : the enthalpy change between ligand and linked-ligand###############################################
######################5. nTddS   : the entropy change between ligand and linked-ligand################################################
######################6. ddG     : the free energy change between ligand and linked-ligand############################################
######################7. AF      : activity fold######################################################################################
######################8. level   : activity change level (Low,Middle,High)############################################################
######################9. picture : the path of the new linked-compound picture########################################################
#####################10. complex : the path of the new complex pdb file###############################################################

if '17' in EXECUTION:
	result_dir = './result'
        gen4newdir(result_dir)                                    #make new directory './result' for storing all the result file

	result_table1 = result_dir + '/table1/'	 
        gen4newdir(result_table1)                                 #make new directory './result/table1' for storing result file

	rm4oldfile(result_table1 + '/table1.log')                 #remove the old log and result file of table1
	rm4oldfile(result_table1 + '/table1.result')
	Fresult = open(result_table1 + '/table1.result','a')      #write a title for table1.result
	Fresult.write('%-100s'%'smile' + '\t' + '%-10s'%'fragment' + '%-8s'%'H_NO.' + '%-20s'%'ddH' + '%-20s'%'-TddS' + '%-20s'%'ddG' + '%-20s'%'AF' + '%-8s'%'level' + '%-20s'%'picture' + '%-20s'%'complex' + '\n')
	Fresult.close()
	

	wt_dir  = './snapshot_E'
	sub_dir = './snapshot_sub'

	search_dir_out = os.listdir(sub_dir)
	for hydrogen in search_dir_out:                           #3.hydrogen  is here -- hydrogen
		search_dir_in = os.listdir(sub_dir + '/' + hydrogen)
		for fragment in search_dir_in:                    #2.fragment  is here -- substituent[fragment]
			if fragment == 'core' or fragment == 'rec':
				pass
			else:
				destination = sub_dir + '/' + hydrogen + '/' + fragment   #get the directory stored the calculated file and result

				########!!get complex file to ./result/table1/com_{hydrogen}_{fragment}.pdb!!#########################

			        try:
			                com_size = os.path.getsize(destination + '/point_after_refine/com.1')   #check whether the file exist
					if com_size > 972:
						os.system('cp ' + destination + '/point_after_refine/com.1 ./result/table1/com_' + hydrogen + '_' + substituent[fragment] + '.pdb') #copy complex file into ./result/table1/com_{hydrogen}_{fragment}.pdb 	
#						path = os.getcwd()
						complex = hydrogen + '_' + substituent[fragment] + '.pdb' 	#10. complex path is here -- complex
					
					else:
						complex = 'NA'                                                                                  #if file is not suitable, use 'NA'
			        except:
					complex = 'NA'                                                                                          #if file is not suitable, use 'NA'
		                	Ftable1 = open(result_table1+'/table1.log','a')
	        	        	Ftable1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + destination + '/point_after_refine/com.1 does not exist, can not copy!\n')
	                		Ftable1.close()


				########!!calculate the energy value!!################################################################
				
				check4wt  = check4energyfile('./snapshot_E/delta_E_statistics.out','./snapshot_E/ds.out')  #check whether the dH_file and dS_file of wt are resonable
				check4sub = check4energyfile(destination + '/energy_cal/delta_E_statistics.out', destination + '/energy_cal/ds.out') #check whether the dH_file and dS_file of sub are resonable 
				if check4wt[0] == 'YES':                                                        #specify value for dH_wt, using by function extract4energy below
					dH_wt = './snapshot_E/delta_E_statistics.out'
				else:
					dH_wt = 'NA'
					Ftable1 = open(result_table1+'/table1.log','a')
					Ftable1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + './snapshot_E/delta_E_statistics.out has problems!\n')
					Ftable1.close()

				if check4wt[1] == 'YES':                                                        #specify value for dS_wt, using by function extract4energy below
					dS_wt = './snapshot_E/delta_g.out'
				else:
					dS_wt = 'NA'
                                        Ftable1 = open(result_table1+'/table1.log','a')
                                        Ftable1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + './snapshot_E/ds.out has problems!\n')
                                        Ftable1.close()

				if check4sub[0] == 'YES':
					dH_sub = destination + '/energy_cal/delta_E_statistics.out'             #specify value for dH_sub, using by function extract4energy below
				else:
					dH_sub = 'NA'
                                        Ftable1 = open(result_table1+'/table1.log','a')
                                        Ftable1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + destination + '/energy_cal/delta_E_statistics.out has problems!\n')
                                        Ftable1.close()

				if check4sub[1] == 'YES':
					dS_sub = destination + '/energy_cal/delta_g.out'                        #specify value for dS_sub, using by function extract4energy below
				else:
					dS_sub = 'NA'
                                        Ftable1 = open(result_table1+'/table1.log','a')
                                        Ftable1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + destination + '/energy_cal/delta_g.out has problems!\n')    
					Ftable1.close()


				energy_result = extract4energy(dH_wt,dS_wt,dH_sub,dS_sub)                       #4.ddH -- energy_result['ddH4PB'], 5.-TddS -- energy_result['nTddS'], 6.ddG -- energy_result['ddG4PB'] energy_result is dictionary {'ddH4PB':value, 'ddH4GB':value, 'nTddS':value, 'ddG4PB':value, 'ddG4GB':value}, value is decimal and can be 'NA'

					
				########!!evaluate the AF and level value!!###########################################################

				print energy_result['ddG4PB']
				AF = ddG2activefold(energy_result['ddG4PB'])                                    #7. AF -- AF here, activity improvement fold, a float number
				level = evaluate4level(AF)                                                      #8. level -- level here, 'Low', 'Middle', 'High' or 'NA'
														# 0<AF<=1, Low; 1<AF<=100, Middle; AF>100, High    

 
				########!!calculate to get smile and picture!!########################################################

                                try:
                                        lig_size = os.path.getsize(destination + '/final_ligand/lig.1')         #check whether the file exist
                                        if lig_size > 972:
                                                os.system('cp ' + destination + '/final_ligand/lig.1 ./result/table1/lig_' + hydrogen + '_' + substituent[fragment] + '.pdb') #copy ligand file into ./result/table1/lig_{hydrogen}_{fragment}.pdb       
						gen4molpicture(result_table1 + '/lig_' + hydrogen + '_' + substituent[fragment] + '.pdb','pdb',result_table1)           #generate ligand smi/jpg file
						smile = linecache.getline(result_table1 + '/lig_' + hydrogen + '_' + substituent[fragment] + '.smi',1).split()[0] #1. smile -- smile here, new ligand smile
                                                picture = hydrogen + '_' + substituent[fragment] + '.jpg'                                       #9. picture -- picture here, new ligand picture path is here

                                        else:
                                                smile  = 'NA'                                                                                   #if file is not suitable, use 'NA'
                                                picture = 'NA'                                                                                  #if file is not suitable, use 'NA'
						Ftable1 = open(result_table1+'/table1.log','a')
						Ftable1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + destination + '/final_ligand/lig.1 has problem!\n')
						Ftable1.close()
                                except:
                                        smile = 'NA'                                                                                            #if file is not suitable, use 'NA'
                                        picture = 'NA'                                                                                          #if file is not suitable, use 'NA'
                                        Ftable1 = open(result_table1+'/table1.log','a')
                                        Ftable1.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + destination + '/final_ligand/lig.1 does not exist, can not copy!\n')
                                        Ftable1.close()

				########!!get the list of database format!!###########################################################

				if energy_result['ddH4PB'] == 'NA':                                                                                #change the 4 value subitems into str, energy_result[ddH4PB], energy_result[nTddS], energy_result[ddG4PB], AF 
					output_ddH4PB = '%-20s'%'NA'
				else:
					output_ddH4PB = '%-20.2f'%energy_result['ddH4PB']  

				if energy_result['nTddS'] == 'NA':
					output_nTddS = '%-20s'%'NA'
				else:
					output_nTddS = '%-20.2f'%energy_result['nTddS']

                                if energy_result['ddG4PB'] == 'NA':
                                        output_ddG4PB = '%-20s'%'NA'
                                else:
                                        output_ddG4PB = '%-20.2f'%energy_result['ddG4PB']

                                if AF == 'NA':
                                        output_AF = '%-20s'%'NA'
                                else:
                                        output_AF = '%-20.2f'%AF

				table1 = [smile, substituent[fragment], hydrogen, energy_result['ddH4PB'], energy_result['nTddS'], energy_result['ddG4PB'], AF, level, picture, complex]   #get the list storing the every sub item
				
				Fresult = open(result_table1 + './table1.result','a')
				Fresult.write('%-100s'%table1[0] + '\t' + '%-10s'%table1[1] + '%-8s'%table1[2] + output_ddH4PB + output_nTddS + output_ddG4PB + output_AF + '%-8s'%table1[7] + '%-20s'%table1[8] + '%-20s'%table1[9] + '\n')
				Fresult.close()
					
 

######################18.@!!generate table2.result and heatmap.result by extracting information from table1.result!!@#################
#####################################line.split()[1] ----- fragment###################################################################
#####################################line.split()[2] ----- hydrogen###################################################################
#####################################line.split()[5] ----- ddG########################################################################
#####################################line.split()[7] ----- level######################################################################

if '18' in EXECUTION:
        result_dir = './result'
        gen4newdir(result_dir)                                    #make new directory './result' for storing all the result file

        result_table2 = result_dir + '/table2/'
        result_heatmap = result_dir + '/heatmap/'
        gen4newdir(result_table2)                                 #make new directory './result/table2' for storing result file
        gen4newdir(result_heatmap)                                #make new directory './result/heatmap' for storing result file

        rm4oldfile(result_table2 + '/table2.log')                 #remove the old log and result file of table2
        rm4oldfile(result_heatmap + '/heatmap.log')                 #remove the old log and result file of table2
        rm4oldfile(result_table2 + '/table2.result')
        rm4oldfile(result_heatmap + '/heatmap.result')

        Fresult2 = open(result_table2 + '/table2.result','a')      #write a title for table2.result
        Fresult2.write('%-20s'%'hydrogen' + '%-15s'%'Br' + '%-15s'%'Br_ddG' + '%-15s'%'CF3' + '%-15s'%'CF3_ddG' + '%-15s'%'CH3' + '%-15s'%'CH3_ddG' + '%-15s'%'Cl' + '%-15s'%'Cl_ddG' + '%-15s'%'COOH' +  '%-15s'%'COOH_ddG' + '%-15s'%'F' + '%-15s'%'F_ddG' + '%-15s'%'NH2' + '%-15s'%'NH2_ddG' + '%-15s'%'NO2' + '%-15s'%'NO2_ddG' + '%-15s'%'OCH3' + '%-15s'%'OCH3_ddG' + '%-15s'%'OH'  + '%-15s'%'OH_ddG' + '%-20s'%'score' + '\n')
        Fresult2.close()

        Fresult3 = open(result_heatmap + '/heatmap.result','a')      #write a title for heatmap.result
        Fresult3.write('%-20s'%'hydrogen' + '%-15s'%'Br' + '%-15s'%'CF3'  + '%-15s'%'CH3'  + '%-15s'%'Cl'  + '%-15s'%'COOH' + '%-15s'%'F' + '%-15s'%'NH2' + '%-15s'%'NO2' + '%-15s'%'OCH3' + '%-15s'%'OH'  + '\n')                                              #here title is substituent, but ddG value should be write
        Fresult3.close()

 
	table1_file = './result/table1/table1.result'	
	hydrogens = input.count4ligH('./snapshot_E/point/lig.1')                                #get ALL ligand hydrogen ATOM NUMBER and store in LIST - hydrogens

	if os.path.isfile(table1_file):
		
		for H in hydrogens:
			H_info = extract4Hinfo(H,table1_file,substituent)	    #get all this H information in a dictionary H_info e.g.{'F': 'High', 'Cl': 'High', 'F_ddG': '-4.77', 'CH3_ddG': '-2.54', 'OH': 'High', 'Br_ddG': '-4.96', 'COOH_ddG': '46.33', 'NH2_ddG': '-4.01', 'OCH3_ddG': 'NA', 'NH2': 'High', 'CF3_ddG': '2.14', 'NO2_ddG': '-1.06', 'OCH3': 'NA', 'CH3': 'Middle', 'Cl_ddG': '-3.44', 'Br': 'High', 'OH_ddG': '-3.65', 'COOH': 'Low', 'hydrogen': '6226', 'CF3': 'Low', 'NO2': 'Middle'} but do not include score
			if H_info == {}:
				pass
			else:
				H_score = extract4Hscore(H,table1_file)  #get score value, decimal type
				H_info['score']	= H_score                #add the score to H_info
				
				Fresult2 = open(result_table2 + '/table2.result','a')
				Fresult2.write('%-20s'%H_info['hydrogen'] + '%-15s'%H_info['Br'] + '%-15s'%H_info['Br_ddG'] + '%-15s'%H_info['CF3'] + '%-15s'%H_info['CF3_ddG'] + '%-15s'%H_info['CH3'] + '%-15s'%H_info['CH3_ddG'] + '%-15s'%H_info['Cl'] + '%-15s'%H_info['Cl_ddG'] + '%-15s'%H_info['COOH'] +  '%-15s'%H_info['COOH_ddG'] + '%-15s'%H_info['F'] + '%-15s'%H_info['F_ddG'] + '%-15s'%H_info['NH2'] + '%-15s'%H_info['NH2_ddG'] + '%-15s'%H_info['NO2'] + '%-15s'%H_info['NO2_ddG'] + '%-15s'%H_info['OCH3'] + '%-15s'%H_info['OCH3_ddG'] + '%-15s'%H_info['OH']  + '%-15s'%H_info['OH_ddG'] + '%-20.2f'%float(H_info['score']) + '\n')
				Fresult2.close()

				Fresult3 = open(result_heatmap + '/heatmap.result','a')
				Fresult3.write('%-20s'%H_info['hydrogen'] + '%-15s'%H_info['Br_ddG'] + '%-15s'%H_info['CF3_ddG']  + '%-15s'%H_info['CH3_ddG']  + '%-15s'%H_info['Cl_ddG']  + '%-15s'%H_info['COOH_ddG'] + '%-15s'%H_info['F_ddG'] + '%-15s'%H_info['NH2_ddG'] + '%-15s'%H_info['NO2_ddG'] + '%-15s'%H_info['OCH3_ddG'] + '%-15s'%H_info['OH_ddG']  + '\n')
				Fresult3.close()
	
	else:
		error2log('./total.error','error in step 17 --- generate the first table which display all the compound energy, table1.result has problems!')
		error2log(result_table2+'/table2.log','table1.result does not exist!')
		error2log(result_heatmap+'/heatmap.log','table1.result does not exist!')
		sys.exit(0)

else:
	pass


######################19.@!!generate heatmap.input and heatmap picture!!@#############################################################

if '19' in EXECUTION:
	workdir = './result/heatmap/'
	heatmap_result = './result/heatmap/heatmap.result'
	heatmap_input = './result/heatmap/heatmap.input'
	gen4heatmapinput(heatmap_result,heatmap_input)  #generate heatmap.input under './result/heatmap/'
	path = os.getcwd()
	os.chdir(workdir)
        gen4heatmappng('heatmap.input')                   #run heatmap.R to get heatmap.png under './result/heatmap/'
        os.chdir(path)

        #perform a judge step###########################################
        if detect4error('./result/heatmap/heatmap.png',3000) == 'YES':
                pass
        else:
                error2log('./total.error','error in step 22 --- generate heatmap.input and heatmap picture, problems with the heatmap.input or heatmap.png')
                sys.exit(0)

else:
	pass

