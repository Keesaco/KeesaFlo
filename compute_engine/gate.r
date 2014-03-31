###########################################################################
## \file compute_engine/gate.r
## \brief Gates flow cytometry data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
source('rfunctions.r')
imports()

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
gate_name <- args[2]
tlx <- as.integer(args[3])
tly <- as.integer(args[4])
brx <- as.integer(args[5])
bry <- as.integer(args[6])
reverse <- as.integer(args[7])

## Read fcs data.
x <- read.FCS(fcs_name, transformation = FALSE)

## Finding first two observables.
a <- colnames(x[,1])
b <- colnames(x[,2])

## Calculate graph coordinates from pixel coordinates
r1 <- range(x[,1])
r2 <- range(x[,2])

tlx <- imageToGraphCoordx(tlx, r1[1,1], r1[2,1])
brx <- imageToGraphCoordx(brx, r1[1,1], r1[2,1])

tly <- imageToGraphCoordy(tly, r2[1,1], r2[2,1])
bry <- imageToGraphCoordy(bry, r2[1,1], r2[2,1])

## Working out gate, need to change values.
gate <- createRectGate(tlx, tly, brx, bry, a, b)

## Creating subset of data.
y <- createSubset(x, gate, reverse)

## Save gate as fcs file
write.FCS(y, gate_name)

## Calculating proportion
writeInfo(x, gate)

## Plotting the gate
image_name <- paste(gate_name, ".png", sep="")
plotGraph(image_name, y, a, b)