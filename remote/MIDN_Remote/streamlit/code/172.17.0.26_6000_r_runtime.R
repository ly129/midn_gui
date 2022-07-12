

source("CSLMICE/CSLMICERemote.R")
args = commandArgs(trailingOnly=TRUE)
X=as.matrix(read.table(file=args[1]))
colnames(X) <- NULL

CSLMICERemote(X,"6000","172.17.0.28","6600")

    