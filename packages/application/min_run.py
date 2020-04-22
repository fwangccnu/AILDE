#!/usr/bin/python
import os
def sander4minWT(top,crd,option):
	'''
--------------------------------------------------------
'sander4minWT' is used to perform the min step for WT
	usage : sander4minWT(top,crd,option)
        input : top - top file ; crd - starting crd file ; option - whether to use parallel
        output: finish 3 min steps 
--------------------------------------------------------
'''
	if option == 'YES':
		os.system('mpirun -np 4 sander.MPI -O -i min1.in -o min1.out -p {top_file} -c {crd_file} -r min1.rst -ref {crd_file}'.format(top_file=top,crd_file=crd)) #Movements was allowed only for the water molecules, ions and Hydrogens
        	os.system('mpirun -np 4 sander.MPI -O -i min2.in -o min2.out -p {top_file} -c min1.rst -r min2.rst -ref min1.rst'.format(top_file=top)) #The backbone atoms were fixed, and other atoms were allowed to move
        	os.system('mpirun -np 4 sander.MPI -O -i min3.in -o min3.out -p {top_file} -c min2.rst -r min3.rst -ref min2.rst'.format(top_file=top)) #Minimaze all atoms
	else:	
                os.system('sander -O -i min1.in -o min1.out -p {top_file} -c {crd_file} -r min1.rst -ref {crd_file}'.format(top_file=top,crd_file=crd)) #Movements was allowed only for the water molecules, ions and Hydrogens
                os.system('sander -O -i min2.in -o min2.out -p {top_file} -c min1.rst -r min2.rst -ref min1.rst'.format(top_file=top)) #The backbone atoms were fixed, and other atoms were allowed to move
                os.system('sander -O -i min3.in -o min3.out -p {top_file} -c min2.rst -r min3.rst -ref min2.rst'.format(top_file=top)) #Minimaze all atoms

if __name__ == '__main__':
	sander4minWT('complex_wat.top','complex_wat.crd','YES')
