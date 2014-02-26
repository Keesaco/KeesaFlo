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
gatename <- args[2]
tlx <- 50000
tly <- 150000
brx <- 100000
bry <- 50000

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
png(gatename)
plot(y,c(a, b))

## Saves gate as .fcs file

dev.off()