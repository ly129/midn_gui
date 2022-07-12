

source("IMICE/IMICECentral.R")

args = commandArgs(trailingOnly=TRUE)
X=as.matrix(read.table(file=args[1]))
colnames(X) <- NULL

imp = IMICECentral(X,10,c(1, 2),c("Gaussian", "Gaussian"), 10, 20)

#options(max.print=1000000)
#print(imp)

for (i in 1:length(imp)) {
  write.table(imp[i],file= paste('../data/','Result_',i,'.txt', sep=""))
}

            