###########################################################################
## \file compute_engine/gating.r
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
tlx <- as.integer(args[3])
tly <- as.integer(args[4])
brx <- as.integer(args[5])
bry <- as.integer(args[6])

## Read fcs data.
x <- read.FCS(fcs_name, transformation = FALSE)

## Finding first two observables.
a <- colnames(x[,1])
b <- colnames(x[,2])

## Working out gate, need to change values.
mat <- matrix(c(tlx, brx, bry, tly), ncol=2, dimnames=list(c("min", "max"), c(a, b)))
rgate <- rectangleGate(.gate=mat)

## Creating subset of data.
y <- Subset(x, rgate)

## Plotting the gate
u <- range(tlx, brx)
v <- range(bry, tly)
png(gate_name)
plot(y,c(a, b), xlim = u, ylim = v)
dev.off()