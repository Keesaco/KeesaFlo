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
reverse <- as.integer(args[3])
x_axis <- args[4]
y_axis <- args[5]
sf <- as.integer(args[6])

## Read fcs data.
if(file.exists(fcs_name) == FALSE)
	quit("no", 1)
x <- read.FCS(fcs_name, transformation = FALSE)

## Create the filter object
n2f <- norm2Filter(c(x_axis, y_axis), scale.factor = sf)
normfilter <- filter(x, n2f)

## Creating a subset of data.
y <- createSubset(x, normfilter, reverse)

## Save gate as fcs file
write.FCS(y, gate_name)

## Saves gate info in a txt file
writeInfo(x, n2f, reverse)

## Plots the gate
image_name <- paste(gate_name, ".png", sep="")
plotGraph(image_name, y, x_axis, y_axis, nrow(y@exprs))
quit("no", 0)