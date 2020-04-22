#!/usr/bin/python
def sander4watmin1():
	content1 = """#First minimazation for waters and ions
&cntrl
imin = 1,
ntmin = 1,
maxcyc = 4000,
ncyc = 2000,
ntpr = 50,
cut = 10.0,
ntb = 1,
ntr = 1,
drms= 0.1,
restraint_wt=500,
restraintmask=':*&!:WAT&!:Cl-&!:Na+&!@H='
/
	"""
	F1 = open('min1.in','w+')
	F1.write(content1)
	F1.close()

def sander4watmin2(total_AA):
	content2 = """#Second minimazation to fix backbone of receptor
&cntrl
imin = 1,
ntmin = 1,
maxcyc = 4000,
ncyc = 2000,
ntpr = 50,
cut = 10.0,
ntb = 1,
ntr = 1,
drms= 0.1,
restraint_wt=500,
"""
	F2 = open('min2.in','w+')
	F2.write(content2)
	F2.write("restraintmask=':1-{AA_number}&@N,CA,C'\n".format(AA_number=str(total_AA)))
	F2.write('/\n')
	F2.close()

def sander4watmin3():
	content3 = """#Third minimazation to minimize all atoms
&cntrl
imin = 1,
ntmin = 1,
maxcyc = 4000,
ncyc = 2000,
ntpr = 50,
cut = 10.0,
ntb = 1,
ntr=0,
drms= 0.1,
/
	"""
	F3 = open('min3.in','w+')
        F3.write(content3)
        F3.close()

def detect(complex):
	F = open(complex,'r')
	res_sum=[]
	for line in F:
		if line.startswith('ATOM'):
			res_num=int(line[22:26])
			if res_num not in res_sum:
				res_sum.append(res_num)
			else:
				pass
		else:
			continue
	F.close()
#	print max(res_sum)
	total_AA = len(res_sum)-1
	return total_AA


def sander4Nowatminside(total_AA):
        content2 = """#minimazation for sidechain of snapshots
&cntrl
imin = 1,
ntmin = 1,
maxcyc = 500,
ncyc = 250,
ntpr = 50,
cut = 10.0,
ntb = 0,
ntr = 1,
drms= 0.2,
restraint_wt=500,
"""
        F2 = open('min_snap_side.in','w+')
        F2.write(content2)
        F2.write("restraintmask=':1-{AA_number}&@N,CA,C'\n".format(AA_number=str(total_AA)))
        F2.write('/\n')
        F2.close()


def sander4Nowatminsnap():
        content3 = """#Third minimazation to minimize all atoms
&cntrl
imin = 1,
ntmin = 1,
maxcyc = 500,
ncyc = 250,
ntpr = 50,
cut = 10.0,
ntb = 0,
ntr=0,
drms= 0.2,
/
        """
        F3 = open('min_snap.in','w+')
        F3.write(content3)
        F3.close()

