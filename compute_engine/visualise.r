###########################################################################
## \file compute_engine/visualise.r
## \brief Visualises flow cytometry data.
## \author rmurley@keesaco.com of Keesaco
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
library("flowCore")
library("flowViz")
library("methods")

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
vis_name <- args[2]
info_name <- args[3]

## Read fcs data.
if(file.exists(fcs_name) == FALSE)
	quit("no", 1)
x <- read.FCS(fcs_name, transformation = FALSE)

## Finding first two observables.
a <- colnames(x[,1])
b <- colnames(x[,2])

## Finding list of observables
c <- colnames(x)
write(c, file = info_name)

## Plot data.
png(vis_name)
plot(x, c(a, b))
dev.off()
quit("no", 0)