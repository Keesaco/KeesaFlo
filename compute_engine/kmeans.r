###########################################################################
## \file compute_engine/kmeans.r
## \brief Applies a filter fitting a bivariate normal distribution to gate
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
source('rfunctions.r')
imports()

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
cluster_names <- args[2]
no_clusters <- as.integer(args[3])
x_axis <- args[4]
y_axis <- args[5]

## Read fcs data.
if(file.exists(fcs_name) == FALSE)
	quit("no", 1)
x <- read.FCS(fcs_name, transformation = FALSE)

## Creates gate
c <- list(1:no_clusters)
names(c) <- x_axis
kf <- kmeansFilter(c)
fres <- filter(x, kf)
clusters <- split(x, fres)

## Creates new .fcs file and image for each quadrant
cluster_names <- strsplit(cluster_names, " ")
l <- length(cluster_names[[1]])
if(l < no_clusters)
	quit("no", 2)

for(i in 1:no_clusters)
{
	## Save gate as fcs file
	write.FCS(clusters[[i]], cluster_names[[1]][i])
	## Plots the gate
	image_name <- paste(cluster_names[[1]][i], ".png", sep="")
	plotGraph(image_name, clusters[[i]], x_axis, y_axis, nrow(clusters[[i]]@exprs))
}
## Saves gate info in .txt file
	info_names <- 0 ## Initialises info names
	for(i in 1:4)
	{
		info_names[i] <- paste(cluster_names[[1]][i], '.txt', sep="")
	}
	writeInfoMultipleFilters(x, fres, info_names)
quit("no", 0)