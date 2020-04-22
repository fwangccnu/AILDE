#!/usr/bin/python
import os
def pmemd4mdWT(top,rst,start,end,option):
	'''
--------------------------------------------------------
'pmemd4mdWT' is used to perform the md step for WT
	usage: pmemd4mdWT(top,rst,start,end,option)
        input : top - top file ; rst - starting rst file ; start - start job of MD ; option - whether to use parallel
        output: finish 3 md steps 
--------------------------------------------------------
'''
	if option == 'YES':               #means use parallel to run MD
		os.environ['CUDA_VISIBLE_DEVICES']='1,2,3,0'
		if start == '3':          #for the convenience to start from stop place
			os.system('mpirun -np 4 pmemd.cuda.MPI -O -i md1.in -o md1.out -p {top_file} -c {rst_file} -r md1.rst -ref {rst_file} -x md1.crd'.format(top_file=top,rst_file=rst))
			os.system('mpirun -np 4 pmemd.cuda.MPI -O -i md2.in -o md2.out -p {top_file} -c md1.rst -r md2.rst -ref md1.rst -x md2.crd'.format(top_file=top))
		else:
			pass
	
		MDSTARTJOB=int(start)
		MDENDJOB=int(end)
		for i in range(MDSTARTJOB,MDENDJOB+1):
			os.system('mpirun -np 4 pmemd.cuda.MPI -O -i md3.in -p {top_file} -c md{MDINPUT}.rst -r md{MDCURRENTJOB}.rst -x md{MDCURRENTJOB}.crd -o md{MDCURRENTJOB}.out -ref md{MDINPUT}.rst'.format(top_file=top,MDINPUT=str(i-1),MDCURRENTJOB=str(i)))

	else:				 #means do not use parallel
		os.environ['CUDA_VISIBLE_DEVICES']='2'
                if start == '3':          #for the convenience to start from stop place
                        os.system('pmemd.cuda -O -i md1.in -o md1.out -p {top_file} -c {rst_file} -r md1.rst -ref {rst_file} -x md1.crd'.format(top_file=top,rst_file=rst))
                        os.system('pmemd.cuda -O -i md2.in -o md2.out -p {top_file} -c md1.rst -r md2.rst -ref md1.rst -x md2.crd'.format(top_file=top))
                else:
                        pass

                MDSTARTJOB=int(start)
                MDENDJOB=int(end)
                for i in range(MDSTARTJOB,MDENDJOB+1):
                        os.system('pmemd.cuda -O -i md3.in -p {top_file} -c md{MDINPUT}.rst -r md{MDCURRENTJOB}.rst -x md{MDCURRENTJOB}.crd -o md{MDCURRENTJOB}.out -ref md{MDINPUT}.rst'.format(top_file=top,MDINPUT=str(i-1),MDCURRENTJOB=str(i)))



if __name__ == '__main__':
	pmemd4mdWT('complex_wat.top','min3.rst','3','15','YES')

