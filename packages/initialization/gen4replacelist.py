#!/usr/bin/python
def gen4replacelist(hydrogen_list,fragment_file):
	'''
--------------------------------------------------------
'gen4replacelist' is used to generate the file 'replacelist.prm' for SPECIFYING the REPLACE SITES and SUBSTITUENTS TYPE!
        usage: gen4replacelist(hydrogen_list,fragment_file)
        input : hydrogen_list(list type) - the list RECORD the HYDROGEN ATOM NUMBER. 
                fragment_file(file) - fragment list, default is ./packages/lib/substituent/list
        output: output - 'file replacelist.prm'
--------------------------------------------------------
'''

	F1 = open('replacelist.prm','w+')
	F1.write('#####This File is used for SPECIFY the REPLACE SITES and SUBSTITUENTS TYPE!####\n\n')
	F1.write("#####SUBSTITUENT TYPE SPECIFIED BY FRAGMENT_NUMBER, split by ',' reprensent NON-CONTINUOUS type, use '-' represent CONTINUOUS fragment####\n\n")
	F1.write('#####The OPTINAL SUBSTITUENTS TYPES are shown below:\n\n')
	F1.write('##\tFRAGMENT NUMBER\t\tFRAGMENT TYPE\n')
	F2 = open(fragment_file,'r')
	for line in F2:
		if line.startswith('fragment'):
			fragment_number = line.split()[0].split('_')[1]
			F1.write('##\t'+fragment_number+'\t'+line)
		else:
			pass
	F2.close()
	F1.write('#############################################################################\n\n')
	F1.write('#####The REPLACE SITES and SUBSTITUENTS TYPE is shown below:\n\n')
	F1.write('##\t\tID\tH.NO.\t\tSUB-TYPES\n')
	ID = 0
	for num in hydrogen_list:
		ID+=1
		F1.write('TYPE      \t'+str(ID)+'\t'+num+'\t\t'+'01-'+fragment_number+'\n')
	F1.close()


def deal4num(num_sequence):
        '''
--------------------------------------------------------
'deal4num' is used to DEAL WITH A NUMBER SEQUENCE INTO a LIST
	e.g. '01-02,03,05,07-10' ---- ['01','02','03','05','07','08','09','10'] 
        usage: deal4num(num_sequence)
        input : a number sequece like e.g. 
        output: return a list 
--------------------------------------------------------
'''
	
	list1 = num_sequence.split(',')
	list2 = []
	for item in list1:
		if '-' in item:
			list3 = item.split('-')
			start = int(list3[0])
			end   =	int(list3[1])
			for i in range(start,end+1):
				list2.append(str(i))
		else:
			list2.append(str(int(item)))
	list4 = []
	for j in list2:
		if len(j) == 1:
			list4.append('0'+j)
		else:
			list4.append(j)
	list5 = list(set(list4))
	list5.sort()	
	return list5
				
