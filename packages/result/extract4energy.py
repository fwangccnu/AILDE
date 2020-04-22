#!/usr/bin/python

import decimal
import os

def extract4energy(dH_wt,dS_wt,dH_sub,dS_sub):
	'''
--------------------------------------------------------
'extract4energy' is used to calculate ddH,-TddS and ddG value
        usage: extract4energy(dH_wt,dS_wt,dH_sub,dS_sub)
        input : dH_wt/dH_sub - specify the entropy result file path (always named {path}/delta_E_statistic.out) for wt/sub 
		dS_wt/dS_sub - specify the entropy result file path (always named {path}/delta_g.out or {path}/x) for wt/sub
        output: output - the energy of ddH(PB),ddH(GB),-TddS, ddG(PB) and ddG(GB) stored in result_directory, value is number 
	Notice: Please ensure the four files exist
--------------------------------------------------------
'''
	if dH_wt != 'NA':
		F1 = open(dH_wt,'r')
		for line in F1:
			if line.startswith('PBTOT'):
				dH4wtPB = line.split()[1]    #get wild type dH(PB)
			elif line.startswith('GBTOT'):
				dH4wtGB = line.split()[1]    #get wild type dH(GB)
			else:
				pass
		F1.close()
	else:
		dH4wtPB = 'NA'
		dH4wtGB = 'NA'
	#####################################################################

	if dS_wt != 'NA':		
		F2 = open(dS_wt,'r')                         #here both of 'x' and 'delta_g.out' can be used as dS_file
		for line in F2:
			if line.startswith('-TS'):
				nTS4wt = line.split()[1]     #get wild type -TS
			else:
				pass
		F2.close()
	else:
		nTS4wt = 'NA'
	#####################################################################
 
	
	if dH_sub != 'NA':	
		F3 = open(dH_sub,'r')
		for line in F3:
			if line.startswith('PBTOT'):
				dH4subPB = line.split()[1]   #get substituent type dH(PB)
	        	elif line.startswith('GBTOT'):
	                	dH4subGB = line.split()[1]   #get substituent type dH(GB)
			else:
				pass
		F3.close()
	else:
		dH4subPB = 'NA'
		dH4subGB = 'NA'
	#####################################################################
	
	if dS_sub != 'NA':
		F4 = open(dS_sub,'r')
		for line in F4:
			if line.startswith('-TS'):
				nTS4sub = line.split()[1]    #get substituent type -TS
			else:
				pass
		F4.close()
	else:
		nTS4sub = 'NA'

	##########change the value into decimal##########################################

	if dH4wtPB == 'NA':
		dH4wtPB_value = 'NA'
	else:
		decimal.getcontext().prec=5
		dH4wtPB_value = decimal.Decimal(dH4wtPB)

	if dH4wtGB == 'NA':
		dH4wtGB_value = 'NA'
	else:
		decimal.getcontext().prec=5
		dH4wtGB_value = decimal.Decimal(dH4wtGB)

	if nTS4wt == 'NA':
		nTS4wt_value = 'NA'
	else:
		decimal.getcontext().prec=5 
		nTS4wt_value  = decimal.Decimal(nTS4wt)

	if dH4subPB == 'NA':
		dH4subPB_value = 'NA'
	else:
		decimal.getcontext().prec=5
		dH4subPB_value = decimal.Decimal(dH4subPB)	

	if dH4subGB == 'NA':
		dH4subGB_value = 'NA'
	else:
		decimal.getcontext().prec=5
		dH4subGB_value = decimal.Decimal(dH4subGB)

	if nTS4sub == 'NA':
		nTS4sub_value = 'NA'
	else:
		decimal.getcontext().prec=5
		nTS4sub_value = decimal.Decimal(nTS4sub)

	##########get the final 5 result################################################# 
	
	try: 
		ddH4PB = dH4subPB_value - dH4wtPB_value      #enthalpy change of PB
	except:
		ddH4PB = 'NA'

	try:
		ddH4GB = dH4subGB_value - dH4wtGB_value      #enthalpy change of GB
	except:
		ddH4GB = 'NA'
	
	try:
		nTddS = nTS4sub_value - nTS4wt_value	     #entropy change 
	except:
		nTddS = 'NA'
	
	if 'NA' in [ddH4PB,nTddS]:
		ddG4PB = 'NA'
	else:
		ddG4PB = ddH4PB + nTddS                      #binding free energy change of PB

#	try:
#		ddG4PB = ddH4PB + nTddS                      #binding free energy change of PB
#	except:
#		ddG4PB = 'NA'
	
	if 'NA' in [ddH4GB,nTddS]:
		ddG4GB = 'NA'
	else:
		ddG4GB = ddH4GB + nTddS                      #binding free energy change of GB

#	try:
#		ddG4GB = ddH4GB + nTddS                      #binding free energy change of GB
#	except:
#		ddG4GB = 'NA'

	result_directory = {'ddH4PB':ddH4PB, 'ddH4GB':ddH4GB, 'nTddS':nTddS, 'ddG4PB':ddG4PB, 'ddG4GB':ddG4GB}
							     #store them in the result directory
	return result_directory


if __name__ == '__main__':
	directory = '/yp_home/wufx/CSO_case_study/bc1_complex/MD_wild/'
	result = extract4energy(directory+'/snapshot_E/delta_E_statistics.out',directory+'/snapshot_E/delta_g.out',directory+'/snapshot_sub/6257/04/energy_cal/delta_E_statistics.out',directory+'/snapshot_sub/6257/04/energy_cal/delta_g.out')	
	print result




def check4energyfile(dH_file,dS_file):
        '''
--------------------------------------------------------
'check4energyfile' is used to judge whether enthalpy file and entropy file is calculated correctly for using
        usage: check4energyfile(dH_file,dS_file)
        input : dH_file/dS_file - specify the dH file and dS file
        output: whether the two files exist and whether can be used for energy calculation.
		a list [A1,A2], ['YES','YES'] mean both of the two file can be used.
--------------------------------------------------------
'''
	if os.path.isfile(dH_file):                  #judge the enthalpy file
		A1 = 'YES'
	else:
		A1 = 'NO'


	#############################################################################

	if os.path.isfile(dS_file):                  #judge the entropy filr
		A2 = 'YES'
		F1 = open(dS_file,'r')
		content = F1.readlines()
		if len(content) > 2:
			for result in content:
				if A2 == 'YES':
					for value in result.split():
						if value == '0' or value == 'nan' or value == '0.000':
							A2 = 'NO'        #once there is insuitable value, break
							break
						else:
							continue
				else:
					break
		else:
			A2 = 'NO'                                        #once file is enmpty, break
		F1.close()
	else:
		A2 = 'NO'                                                #once no file, break

	#############################################################################

	return [A1,A2]


if __name__ == '__main__':
        directory = '/yp_home/wufx/CSO_case_study/bc1_complex/MD_wild/'
        result = check4energyfile(directory+'/snapshot_sub/6257/04/energy_cal/delta_E_statistics.out',directory+'/snapshot_sub/6257/04/energy_cal/ds.out')
        print result




