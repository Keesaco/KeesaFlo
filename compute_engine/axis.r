###########################################################################
## \file compute_engine/axis.r
## \brief Gates flow cytometry data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
library("flowCore")
library("flowViz")
library("methods")

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
vis_name <- args[2]
xaxis <- args[3]
yaxis <- args[4]

## Read file
x <- read.FCS(fcs_name, transformation = FALSE)

## Plot graph
png(vis_name)
plot(x,c(xaxis, yaxis))
dev.off()