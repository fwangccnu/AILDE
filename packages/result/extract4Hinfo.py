#!/usr/bin/python
import decimal

def extract4Hinfo(Hno,infile,subdictionary):
	'''
--------------------------------------------------------
'extract4Hinfo' is used to get a dictionary which is about Hydrogen number
        usage: extract4Hinfo(Hno,infile)
        input : Hno - the Hydrogen number you want to extract infomation
	infile: the file used to read, always table1.result
        output: output - a dictionary, include mysql table2 infomation
        notice: the dictionary include:
               	1. hydrogen; 2. Br; 3. Br_ddG; 4. CF3; 5. CF3_ddG; 6. CH3; 7. CH3_ddG; 8. Cl; 9. Cl_ddG; 
	10. COOH; 11. COOH_ddG; 12. F; 13. F_ddG; 14. NH2; 15. NH2_ddG; 16. NO2; 17. NO2_ddG; 
	18. OCH3; 19. OCH3_ddG; 20. OH; 21. OH_ddG   and other added substituent
--------------------------------------------------------
	'''
	F = open(infile,'r')
	H_information = {}
	for line in F.readlines()[1:]:
		hydrogen = line.split()[2]
		fragment = line.split()[1]
		ddG = line.split()[5]
		level = line.split()[7]
		if hydrogen == Hno:
			H_information['hydrogen'] = hydrogen
			H_information[fragment] = level
			H_information[fragment+'_ddG'] = ddG
		else:
			continue
	F.close()

	if H_information == {}:
		pass
	else:
		sublist = []
		for key in subdictionary:
			if subdictionary[key] not in sublist:
				sublist.append(subdictionary[key])
			else:
				pass

		for subtype in sublist:
			if subtype not in H_information:
				H_information[subtype] = 'CA'        #calculating
				H_information[subtype+'_ddG'] = 'NA' #calculating
			else:
				pass
			
	return H_information



def extract4Hscore(Hno,infile):
        '''
--------------------------------------------------------
'extract4Hscore' is used to get a score
        usage: extract4Hscore(Hno,infile)
        input : Hno - the Hydrogen number you want to calculate score
        infile: the file used to read, always table1.result
        output: output - a score number
--------------------------------------------------------
        '''

        F = open(infile,'r')
	score_H = 0
	score_all = 0
        for line in F.readlines()[1:]:
                hydrogen = line.split()[2]
                level = line.split()[7]
		if hydrogen == Hno:
			if level == 'Low' or level == 'NA':
				score_H = score_H + 1
				score_all = score_all + 3
			elif level == 'Middle':
				score_H = score_H + 2
				score_all = score_all + 3
			elif level == 'High':
				score_H = score_H + 3
				score_all = score_all +3
			else:
				pass
		else:
			continue

	if score_all == 0:
		score = 'NA'
	else:
		decimal.getcontext().prec=5
		score = decimal.Decimal(score_H)/decimal.Decimal(score_all)*100

	return score		

######################################################
if __name__ == '__main__':
	A = extract4Hinfo('6234','/yp_home/wufx/CSO/whole_program_test/result/table1/table1.result',{'01':'Br', '02':'CF3', '03':'CH3', '04':'Cl', '05':'COOH', '06':'F', '07':'NH2', '08':'NO2', '09':'OCH3', '10':'OH'})
	print A
	B = extract4Hscore('6234','/yp_home/wufx/CSO/whole_program_test/result/table1/table1.result')
	print B
#####################################################


