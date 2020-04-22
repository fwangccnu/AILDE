#!/usr/bin/python
import os

def gen4heatmapinput(resultfile,inputfile):
	'''
--------------------------------------------------------
'gen4heatmapinput' is used to get a R input file for heatmap
        usage: gen4heatmapinput(resultfile,inputfile)
        input : resultfile - always the heatmap.result including 'NA'
        output: inputfile - a file used by R not include 'NA'
--------------------------------------------------------
	'''
	F = open(inputfile,'w+')
	F.write('%-8s'%'Hnumber' + '%-8s'%'Br' + '%-8s'%'CF3'  + '%-8s'%'CH3'  + '%-8s'%'Cl'  + '%-8s'%'COOH' + '%-8s'%'F' + '%-8s'%'NH2' + '%-8s'%'NO2' + '%-8s'%'OCH3' + '%-8s'%'OH'  + '\n')
	F1 = open(resultfile,'r')
	for line in F1.readlines()[1:]:
		list = line.split()
		for i in range(len(list)):
			if list[i] == 'NA':
				list[i] = '0'
			else:
				pass
		str = ''
		for item in list:
			str = str + '%-8s'%item
		str = str + '\n'
		F.write(str)
	F.close()
	F1.close()
			

def gen4heatmappng(infile):
        '''
--------------------------------------------------------
'gen4heatmappng' is used to get a R png file for heatmap
        usage: gen4heatmappng(resultfile,inputfile)
        input : infile - always the heatmap.input 
        output: outputpng - the heatmap.png
	notice: please give the name of infile, do not add path 
--------------------------------------------------------
        '''
	content1 = '''library('gplots')
library('RColorBrewer')
'''
	content2 = "Mutate <- read.table('"+infile+"',header=TRUE)\n"
	content3 = '''rownames(Mutate)  <- Mutate$Hnumber
B <- dim(Mutate)[2]
Mutate <- Mutate[,2:B]
P <- dim(Mutate)[1]
Q <- dim(Mutate)[2]
C <- max(Mutate)
D <- min(Mutate)
E <- C/4
F <- D/-4
for (i in 1:Q) {
        x=Mutate[,i]
        for (j in 1:P) {
                if (x[j] > 0) {
                        Mutate[j,i] <- x[j]/E
                        }
                else if (x[j] < 0) {
                        Mutate[j,i] <- x[j]/F
                        }
                else    {
                        Mutate[j,i] <- 0
                        }
                }
        }
MutateM <- as.matrix(Mutate)
mycolors <- colorRampPalette(c("#b2182b","#d6604d","#f4a582","#fddbc7","#d1e5f0","#92c5de","#4393c3","#2166ac"))(8)
png(file="heatmap.png",  width = 700, height = 700, units = "px", pointsize = 12,
    bg = "white", res = NA)
heatmap.2(MutateM,Rowv=NA, Colv=NA, margins = c(8,8),xlab='Substituents',ylab='Hydrogen Number',cexRow=1.5,cexCol=1.5, main='Heatmap Result',key=TRUE,keysize=1,trace="none",density.info="none",col=mycolors,dendrogram = "none",colsep = c(1:50),rowsep=c(1:50),sepwidth=c(0.002,0.002))
'''
	F = open('heatmap.R','w+')
	F.write(content1)
	F.write(content2)
	F.write(content3)
	F.close()
	os.system('/yp_home/user/soft/R-3.0.0/bin/R CMD BATCH heatmap.R')

######################################################
if __name__ == '__main__':
#	A = gen4heatmapinput('/yp_home/wufx/CSO/whole_program_test/result/heatmap/heatmap.result','/yp_home/wufx/CSO/whole_program_test/result/heatmap/heatmap.input')
	gen4heatmappng('heatmap.input')
#####################################################


