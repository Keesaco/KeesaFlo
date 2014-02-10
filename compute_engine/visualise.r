###########################################################################
## \file compute_engine/visualise.r
## \brief Visualises flow cytometry data.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
library("flowCore")
library("flowViz")
library("methods")

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
vis_name <- args[2]

## Read fcs data.
x <- read.FCS(fcs_name, transformation = FALSE)

## Plot data.
png(vis_name)
plot(x)
dev.off()