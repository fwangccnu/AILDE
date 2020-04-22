#!/usr/bin/python
import os
import time
def detect4error(file,size):
        '''
--------------------------------------------------------
'detect4error' is used to detect whether the file is resonable.
        input :  the file
	size: a size standard
        output: 'YES' or 'NO'
--------------------------------------------------------
        '''
	if os.path.isfile(file):
		if os.path.getsize(file) > size:
			result = 'YES'
		else:
			result = 'NO'
	else:
		result = 'NO'

	return result


def error2log(file,errorinfo):
        '''
--------------------------------------------------------
'error2log' is used to write error information to log file.
        input :  file - the error log file you want to write
		errorinfo - the error information you want to write
        output: the log file
--------------------------------------------------------
        '''
	F = open(file,'a')
	F.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + errorinfo + '\n')
	F.close()

######################################################
if __name__ == '__main__':
	A = detect4error('clean_pdb.pyc',1000000)	
	error2log('../../total.error','some problems')
	print A
#####################################################

