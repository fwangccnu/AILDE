#!/usr/bin/python
def md4watmd1(all_AA):
	content1 = """#hold the solute
&cntrl
imin=0,
irest=0,ntx=1,
ntb=1,ntf=2,ntc=2,cut=10,
nrespa=1,
ntr=1,
tempi=10.0,temp0=300.0,ntt=3,gamma_ln=1.0,tautp=3.0,
nstlim=5000,dt=0.002,
ntpr=500,ntwx=500,ntwr=5000,
/
#Hold the solute fixed
100.0
"""
	F1 = open('md1.in','w+')
	F1.write(content1)
	F1.write('RES 1 {all}\n'.format(all=str(all_AA+1)))
	F1.write('END\n')
	F1.write('END\n')
	F1.write('\n')
	F1.close()



def md4watmd2():
	content2 = """#md2 in wat temperature from 10k to 300k
&cntrl
imin=0,
irest=1,ntx=5,
ntb=1,ntf=2,ntc=2,cut=10,
nrespa=1,
tempi=10.0,temp0=300.0,ntt=3,gamma_ln=1.0,tautp=3.0,
nstlim=250000,dt=0.002,
ntpr=500,ntwx=500,ntwr=5000,
 &end

""" 
	F2 = open('md2.in','w+')
	F2.write(content2)
	F2.close()



def md4watmd3():
	content3 = """#md3 in wat temperature at 300k
&cntrl
imin=0,
irest=1,ntx=5,
ntb=2,ntf=2,ntc=2,cut=10,
ntp=1,pres0=1.0,taup=3,
nrespa=1,
tempi=300.0,temp0=300.0,ntt=3,gamma_ln=1.0,tautp=3,
nstlim=100000,dt=0.002,
ntpr=500,ntwx=500,ntwr=500
/

"""
	F3 = open('md3.in','w+')
	F3.write(content3)
	F3.close()



def md4Nowatmdsnap(time,all_AA):             #time should be str
	content4 = """#md_snap in gas temperature at 300k
&cntrl
imin=0,
irest=0,ntx=1,
ntb=0,cut=9999,
igb=1,
ntr=1,
ntp=0,pres0=1.0,taup=3,
nrespa=1,
tempi=300.0,temp0=300.0,ntt=3,gamma_ln=1.0,tautp=3,
"""
	F4 = open('md_snap.in','w+')
	F4.write(content4)
	time_information = 'nstlim='+ time +',dt=0.001,\n'
	F4.write(time_information)
	F4.write('ntpr=500,ntwx=500,ntwr=500\n')
	F4.write('restraint_wt=20,\n')
	F4.write("restraintmask=':1-{AA_number}&@N,CA,C'\n".format(AA_number=str(all_AA)))
	F4.write('/\n')
	F4.close()

	

