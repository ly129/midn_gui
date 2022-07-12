Samples for testing
Here is the sample R code the genereate the random data

X = matrix(rnorm(1000),100,10)
X[1:10,1] = NA
X[,2] = rbinom(100,1,0.5)
X[11:20,2] = NA

library(MASS)

write.matrix(X,'test.txt')
