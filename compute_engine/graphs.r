###########################################################################
## \file compute_engine/graphs.r
## \brief Creates a dot plot of flow cytometry data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
library("flowCore")
library("flowViz")
library("methods")

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
vis_name <- args[2]
x_axis <- args[3]
y_axis <- args[4]
plot_type <- args[5]

## Read fcs data.
if(file.exists(fcs_name) == FALSE)
	quit("no", 1)
x <- read.FCS(fcs_name, transformation = FALSE)

## Plot data.
png(vis_name)
if(plot_type == 'dot')
{
	plot(x, c(x_axis, y_axis), smooth = FALSE)
} else if(plot_type == 'contour')
{
	contour(x, c(x_axis, y_axis))
} else
{
	quit("no", 2)
}
dev.off()
quit("no", 0)