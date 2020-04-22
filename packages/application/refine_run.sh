#!/bin/bash

###$1- 'com.rst' or 'complex2.crd'
###$2- outputdir
###$3- comtop
###$4- md_request
###$5- parallel

for ((i=1;i<5;i++));do
	{
	python refine_run.py "$1.$i" $2 $3 $4 $5
	}&
	done
	wait

