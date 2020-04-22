#!/usr/bin/python
import os
import fnmatch

def entropy4filesin(workdir):
	'''
--------------------------------------------------------
'entropy4filesin' is used to generate files.in file.
        input : workdir - the destination directory to put files.in file
        output: the files.in file for nmode_S
--------------------------------------------------------
	'''
	if os.path.isdir(workdir):
		pass
	else:
		os.system('mkdir -p {workdir}'.format(workdir=workdir))
	content1 = """  AMBER FILES  FOR CONFORMATIONAL ENTROPY
ProteinNT     all_aminont94.in
Proteinct     all_aminoct94.in
Protein       all_amino94.in
DNA           all_nuc02.in
Ligand        ./ligand.prep
Nonstandard   ./ASH.prep
Nonstandard   ./GLH.prep
Nonstandard   ./h2o.prep
"""
	F = open(workdir+'/files.in','w+')
	F.write(content1)
	if os.path.isdir(workdir+'/confactor_prep'):
		list1 = os.listdir(workdir+'/confactor_prep')
		for prep_file in list1:
			if fnmatch.fnmatch(prep_file,'*.prep'):
				F.write('Nonstandard ./confactor_prep/'+prep_file+'\n')
			else:
				pass
	else:
		pass
	F.write('Bondindex     bondindex.h\n')	
	F.close()


def entropy4nmodes(workdir,comtopname,rectopname,ligtopname,liglist):
	'''
--------------------------------------------------------
'entropy4nmodes' is used to generate nmode_S file.
        input : workdir - the destination directory to put nmode_S file
		com/rec/lig + topname - complex/receptor/ligand top file name, the 3 files 
					should be put in the workfir before calculation
		 dellig - means ligand need to be deleted from entropy calculation
	notice : the top files, crd files should be put in the workdir before calculation
        output: the nmode_S file
--------------------------------------------------------
'''
	content1 = """#!/bin/csh


set i=1
echo   Receptor              Ligand         Complex        Conf>ds.out
echo surf polar_ratio  surf polar_ratio  surf polar_ratio  Dnrb>>ds.out
"""

	content2 = """./molsurf  rec.pdb 1.4 | grep "surface area =" | awk ' { printf " %10.3f ", $4 }'>>ds.out
./surf rec.pdb 50 | grep ratio | awk '{ printf "%10.7f ", $6 }'>>ds.out

./molsurf lig.pdb 1.4 | grep "surface area =" | awk ' { printf " %10.3f ", $4 }'>>ds.out
./surf lig.pdb 50 | grep ratio | awk '{ printf "%10.7f ", $6 }'>>ds.out

./molsurf  com.pdb 1.4 | grep "surface area =" | awk ' { printf " %10.3f ", $4 }'>>ds.out
./surf com.pdb 50 | grep ratio | awk '{ printf "%10.7f ", $6 }'>>ds.out

"""
        ############get how many snapshots we have#########################
	list1 = os.listdir(workdir)
	x = 0
	for delta in list1:
		if fnmatch.fnmatch(delta,'delta_E_com.crd.*'):
			x+=1
		else:
			pass
	###################################################################

	F = open(workdir+'/nmode_S','w+')
	F.write(content1)
	F.write('while ( $i < {number} )\n'.format(number=str(x+1)))
	F.write('if ( -e com.pdb ) rm  com.pdb\n')
	F.write('if ( -e rec.pdb ) rm  rec.pdb\n')
	F.write('if ( -e lig.pdb ) rm  lig.pdb\n')
	F.write('ambpdb -p {comtopfile} -pqr <./delta_E_com.crd.$i >com.pdb\n'.format(comtopfile=comtopname))
	F.write('ambpdb -p {rectopfile} -pqr <./delta_E_rec.crd.$i >rec.pdb\n'.format(rectopfile=rectopname))
	F.write('ambpdb -p {ligtopfile} -pqr <./delta_E_lig.crd.$i >lig.pdb\n'.format(ligtopfile=ligtopname))
	F.write(content2)

	if liglist == []:
		pass
	else:
		for dellig in liglist:
			F.write("sed -i '/{dellig}/d' com.pdb\n".format(dellig = dellig))  #ignore cofactor when calculate entropy

	content3 = "./conf -f files.in  -pdb com.pdb -top " + comtopname + " -d 5 |tail -1 |awk '{ print $6-$5-$4}'>>ds.out\n"
	F.write(content3)
	content4 = """@ i += 1
end
cp ds.out ds.out.bak
"""
	F.write(content4)
	F.close()
	os.system('chmod +x {workdir}/nmode_S'.format(workdir=workdir))
