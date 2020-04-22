#!/usr/bin/python
import os
import sys
import fnmatch

def refine4snapshot(RST,outputdir,comtop,md_request,parallel):
	'''
--------------------------------------------------------
'refine4snapshot' is used to perform the refine step for snapshots
	usage : refine4snapshot(RST,outputdir,comtop,md_request,parallel)
        input : RST - input rst file ; comtop - complex top file  ; 
		md_request - whether to add MD after getting snapshot;
		parallel - whether to use parallel
        output: get com.crd.* in outputdir
--------------------------------------------------------
'''
	NUM=RST.split('.')[2]	 
#########################################################################################################
	if parallel == 'NO':	   #strategy 1: run snapshot one by one 
		os.system('mpirun -np 4 sander.MPI -O -i min_snap_side.in -o {outputdir}/min_snap_side.{NUM}.out -p {comtop} -c {outputdir}/{RST} -r {outputdir}/min_snap_side.{NUM}.rst -ref {outputdir}/{RST}'.format(outputdir=outputdir,RST=RST,NUM=NUM,comtop=comtop))
		os.system('mpirun -np 4 sander.MPI -O -i min_snap.in -o {outputdir}/min_snap.{NUM}.out -p {comtop} -c {outputdir}/min_snap_side.{NUM}.rst -r {outputdir}/min_snap.{NUM}.rst -ref {outputdir}/min_snap_side.{NUM}.rst'.format(outputdir=outputdir,NUM=NUM,comtop=comtop))
		
		if md_request == 'NO':
			os.system("ambpdb -p {comtop} -c {outputdir}/min_snap.{NUM}.rst> {outputdir}/com.crd.{NUM} -aatm".format(NUM=NUM,comtop=comtop,outputdir=outputdir))
		else:
			os.environ['CUDA_VISIBLE_DEVICES']='1,2,3,0'
			os.system('mpirun -np 4 pmemd.cuda.MPI -O -i md_snap.in -o {outputdir}/md_snap.{NUM}.out -p {comtop} -c {outputdir}/min_snap.{NUM}.rst -r {outputdir}/md_snap.{NUM}.rst -ref {outputdir}/min_snap.{NUM}.rst -x {outputdir}/md_snap.{NUM}.crd'.format(NUM=NUM,outputdir=outputdir,comtop=comtop))
			os.system('mpirun -np 4 sander.MPI -O -i min_snap_side.in -o {outputdir}/md_snap_min.{NUM}.out -p {comtop} -c {outputdir}/md_snap.{NUM}.rst -r {outputdir}/md_snap_min.{NUM}.rst -ref {outputdir}/md_snap.{NUM}.rst'.format(NUM=NUM,outputdir=outputdir,comtop=comtop))	
			os.system("ambpdb -p {comtop} -c {outputdir}/md_snap_min.{NUM}.rst > {outputdir}/com.crd.{NUM} -aatm".format(NUM=NUM,comtop=comtop,outputdir=outputdir))

#######################################################################################################
	else:                     #run 4 sereval snapshots together
		os.system('sander -O -i min_snap_side.in -o {outputdir}/min_snap_side.{NUM}.out -p {comtop} -c {outputdir}/{RST} -r {outputdir}/min_snap_side.{NUM}.rst -ref {outputdir}/{RST}'.format(outputdir=outputdir,RST=RST,NUM=NUM,comtop=comtop))
		os.system('sander -O -i min_snap.in -o {outputdir}/min_snap.{NUM}.out -p {comtop} -c {outputdir}/min_snap_side.{NUM}.rst -r {outputdir}/min_snap.{NUM}.rst -ref {outputdir}/min_snap_side.{NUM}.rst'.format(outputdir=outputdir,RST=RST,NUM=NUM,comtop=comtop))
		
		if md_request == 'NO':
			os.system("ambpdb -p {comtop} -c {outputdir}/min_snap.{NUM}.rst> {outputdir}/com.crd.{NUM} -aatm".format(NUM=NUM,comtop=comtop,outputdir=outputdir))
		else:
			GPU=4
			GPU_num=int(NUM)%GPU
			os.environ['CUDA_VISIBLE_DEVICES']=str(GPU_num)
			os.system('pmemd.cuda -O -i md_snap.in -o {outputdir}/md_snap.{NUM}.out -p {comtop} -c {outputdir}/min_snap.{NUM}.rst -r {outputdir}/md_snap.{NUM}.rst -ref {outputdir}/min_snap.{NUM}.rst -x {outputdir}/md_snap.{NUM}.crd'.format(NUM=NUM,outputdir=outputdir,comtop=comtop))
			os.system('sander -O -i min_snap_side.in -o {outputdir}/md_snap_min.{NUM}.out -p {comtop} -c {outputdir}/md_snap.{NUM}.rst -r {outputdir}/md_snap_min.{NUM}.rst -ref {outputdir}/md_snap.{NUM}.rst'.format(NUM=NUM,outputdir=outputdir,comtop=comtop))
			os.system("ambpdb -p {comtop} -c {outputdir}/md_snap_min.{NUM}.rst > {outputdir}/com.crd.{NUM} -aatm".format(NUM=NUM,comtop=comtop,outputdir=outputdir))


#####################################################################################################

def sort4rst(outputdir,matchstr,matchrule):
	'''
--------------------------------------------------------
'sort4rst' is used to get the file list which need to be refined.
        input : outputdir - the location of the rst/crd files which need refine ; 
                matchstr - file name property used to identify;
                matchrule - a str type e.g. '1' or '2' means after split('.'), the number's 
			    offset used to match the number from the file.
        	output: return the rst/crd file list used for map.pool function.
--------------------------------------------------------
'''
	snap_dir = os.listdir(outputdir)
	rst_dic = {}
	rst_file = []
	num = int(matchrule)
	for name in snap_dir:
		if fnmatch.fnmatch(name,matchstr+'*'):
			rst_dic[name.split('.')[num]]=name
		else:
			continue
	for i in range(len(rst_dic)):
		mark = i+1
        	if str(i+1) in rst_dic:
                	rst_file.append(rst_dic[str(i+1)])
        	else:
                	pass

	return rst_file

 
if __name__ == '__main__':
	rstfile = sys.argv[1]          #rstfile name
	filedir = sys.argv[2]	       #where to store the file
	topfile = sys.argv[3]          #top file of complex
	md_request = sys.argv[4]       #whether need md
	parallel = sys.argv[5]         #whether need parallel
	
	refine4snapshot(rstfile,filedir,topfile,md_request,parallel)
