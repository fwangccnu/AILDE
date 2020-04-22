#!/usr/bin/python
import os
import shutil
def mmpbsa4cal(infile,outputdir):
	'''
--------------------------------------------------------
'mmpbsa4cal' is used to perform the pbsa calculation step.
	usage : mmpbsa4cal(infile,outputdir)
        input : infile - the input of mmpbsa (e.g. mm_pbsa.in )
		outputdir - where to put the delta_E_statistic.out to
        output: the result file delta_E_statistic.out or give out an error.
--------------------------------------------------------
'''
        try:
                os.system('mm_pbsa.pl {infile} > mm_pbsa.log 2>>mm_pbsa.log'.format(infile=infile))
                shutil.move('./delta_E_statistics.out','{dir}'.format(dir=outputdir))
                os.system('mv delta_E_* {dir}'.format(dir=outputdir))
#               os.system('mv pbsa*out ./snapshot_mut/{dir}'.format(dir=outputdir))
#               os.system('mv sander*out ./snapshot_mut/{dir}'.format(dir=outputdir))
        except IOError:
                try:
                        os.system('rm delta_E_*')
#                       os.system('rm pbsa*out')
#                       os.system('rm sander*out')
                        os.system('rm mm_pbsa.log')
                        os.system('mm_pbsa.pl {infile} > mm_pbsa.log 2>>mm_pbsa.log'.format(infile=infile))
                        shutil.move('./delta_E_statistics.out','{dir}'.format(dir=outputdir))
                        os.system('mv delta_E_* {dir}'.format(dir=outputdir))
#                       os.system('mv pbsa*out {dir}'.format(dir=outputdir))
#                       os.system('mv sander*out {dir}'.format(dir=outputdir))
                except IOError:
                        F=open(r'mm_pbsa.err','a')
                        F.write("The mm_pbsa result of {dir} type cann't be calculated\n".format(dir=outputdir))
                        F.close()
                        os.system('mv delta_E_* {dir}'.format(dir=outputdir))
#                       os.system('mv pbsa*out {dir}'.format(dir=outputdir))
#                       os.system('mv sander*out {dir}'.format(dir=outputdir))
	os.system('mv mm_pbsa.log {dir}'.format(dir=outputdir))

if __name__ == '__main__':
	mmpbsa4cal('mm_pbsa.in','./snapshot_E/')
