#!/usr/bin/python
import os
def gen4newdir(dir_path):
	'''
--------------------------------------------------------
'gen4new' is a small tool to generate directory
        usage: gen4(dir_path)
        input : dir_path(str type) - give a path for generating new directory
        output: output -  if the path exist, pass
			  if not exist, make a new directory
--------------------------------------------------------
'''
	if os.path.isdir(dir_path):
		pass
	else:
		os.system('mkdir -p {dir_path}'.format(dir_path=dir_path))	

