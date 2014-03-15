###########################################################################
## \file compute_engine/ivalgate.r
## \brief Gates flow cytometry data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
library("flowCore")
library("flowViz")
library("methods")

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
gate_name <- args[2]
mx <- as.integer(args[3])
my <- as.integer(args[4])
ax <- as.integer(args[5])
ay <- as.integer(args[6])
bx <- as.integer(args[7])
by <- as.integer(args[8])

## Read fcs data.
x <- read.FCS(fcs_name, transformation = FALSE)

## Finding first two observables.
a <- colnames(x[,1])
b <- colnames(x[,2])

## Calculate graph coordinates from pixel coordinates
r1 <- range(x[,1])
r2 <- range(x[,2])

mx <- ((mx-73)/360) * (r1[2,1]-r1[1,1])
ax <- ((ax-73)/360) * (r1[2,1]-r1[1,1])
bx <- ((bx-73)/360) * (r1[2,1]-r1[1,1])

my <- r2[2,1] - (((my-61)/332) * (r2[2,1]-r2[1,1]))
ay <- r2[2,1] - (((ay-61)/332) * (r2[2,1]-r2[1,1]))
by <- r2[2,1] - (((by-61)/332) * (r2[2,1]-r2[1,1]))

## Calculate eigenvalues of covariance matrix

l1 <- (ax-mx)^2+(ay-my)^2
l2 <- (bx-mx)^2+(by-my)^2

## Calculate eigenvectors of covariance matrix

v11 <- ax-mx
v12 <- ay-my
v21 <- v12 ## This ensures the eigenvectors are perpendicular to each other
v22 <- -v11

## Calculate covariance matrix

V <- matrix(c(v11, v21, v12, v22), ncol = 2, dimnames=list(c(a, b), c(a, b)))
L <- matrix(c(l1, 0, 0, l2), ncol = 2, dimnames=list(c(a, b), c(a, b)))
cov <- V %*% L %*% solve(V)

## Creates the gating parameters

mean <- c(a=mx, b=my)
egate <- ellipsoidGate(.gate = cov, mean = mean)

## Creating subset of data.
y <- Subset(x, egate)

## Calculating proportion

result <- filter(x, egate)
total <- summary(result)$n
inGate <- summary(result)$true
proportion <- summary(result)$p
info <- c(inGate, total, proportion)
info_name <- paste(gate_name, ".txt", sep="")
write(info, file = info_name)

## Plotting the gate
image_name <- paste(gate_name, ".png", sep="")
png(image_name)
plot(y,c(a, b))
dev.off()


