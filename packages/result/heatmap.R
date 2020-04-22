library('gplots')
library('RColorBrewer')
#library('xtable')
Mutate <- read.table('./heatmap.input',header=TRUE)   #Whether I can use the './'
rownames(Mutate)  <- Mutate$Hnumber
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
#heatmap.2(MutateM,Rowv=NA, Colv=NA, margins = c(8,8),xlab='Wild Type',ylab='Mutants',cexRow=1.5,cexCol=1.5, main='AIMMS Result',key=TRUE,keysize=1,trace="none",density.info="none",col=brewer.pal(8,"RdBu"),dendrogram = "none",colsep = c(1:50),rowsep=c(1:50),sepwidth=c(0.002,0.002))
heatmap.2(MutateM,Rowv=NA, Colv=NA, margins = c(8,8),xlab='Substituents',ylab='Hydrogen Number',cexRow=1.5,cexCol=1.5, main='Heatmap Result',key=TRUE,keysize=1,trace="none",density.info="none",col=mycolors,dendrogram = "none",colsep = c(1:50),rowsep=c(1:50),sepwidth=c(0.002,0.002))
