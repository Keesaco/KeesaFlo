###########################################################################
## \file compute_engine/norm_gate.r
## \brief Applies a filter fitting a bivariate normal distribution to gate
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
source('rfunctions.r')
imports()

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
gate_name <- args[2]
x_axis <- args[3]
y_axis <- args[4]
reverse <- args[5]

## Read fcs data.
if(file.exists(fcs_name) == FALSE)
	quit("no", 1)
x <- read.FCS(fcs_name, transformation = FALSE)

## Find range of relevant observables
r1 <- range(x[,1])
r2 <- range(x[,2])

## Create the filter object
n2f <- norm2Filter(c(x_axis, y_axis))
filter <- filter(x, n2f)

## Creating subset of data.
y <- createSubset(x, filter, reverse)

## Save gate as fcs file
write.FCS(y, gate_name)

## Saves gate info in a txt file
writeInfo(x, filter, reverse)

## Plots the gate
image_name <- paste(gate_name, ".png", sep="")
plotGraph(image_name, y, x_axis, y_axis)
quit("no", 0)