#!/usr/bin/python
import os
def rm4oldfile(file_path):
	'''
--------------------------------------------------------
'rm4oldfile' is a small tool to remove old file
        usage: rm4oldfile(file_path)
        input : file_path(str type) - give a file for removing
        output: output -  if the file exist, remove
			  if not exist, pass
--------------------------------------------------------
'''
	if os.path.isfile(file_path):
		os.system('rm {file_path}'.format(file_path=file_path))
	else:
		pass
