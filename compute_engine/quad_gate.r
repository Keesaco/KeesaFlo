###########################################################################
## \file compute_engine/quad_gate.r
## \brief Applies a filter fitting a bivariate normal distribution to gate
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
source('rfunctions.r')
imports()

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
x_coord <- as.integer(args[2])
y_coord <- as.integer(args[3])
quad1_name <- args[4]
quad2_name <- args[5]
quad3_name <- args[6]
quad4_name <- args[7]
x_axis <- args[8]
y_axis <- args[9]

## Read fcs data.
if(file.exists(fcs_name) == FALSE)
	quit("no", 1)
x <- read.FCS(fcs_name, transformation = FALSE)

## Convert image coordinates to graph coordinates
r1 <- range(x[,x_axis])
r2 <- range(x[,y_axis])
x_coord <- imageToGraphCoordx(x_coord, r1[1,1], r1[2,1])
y_coord <- imageToGraphCoordy(y_coord, r2[1,1], r2[2,1])

## Creates gate
boundaries <- setNames(as.list(c(x_coord, y_coord)), c(x_axis, y_axis))
qg <- quadGate(boundaries)
fres <- filter(x, qg)
quadrants <- split(x, fres)

## Creates new .fcs file and image for each quadrant
quadrant_names <- c(quad1_name, quad2_name, quad3_name, quad4_name)
for(i in 1:4)
{
	## Save gate as fcs file
	write.FCS(quadrants[[i]], quadrant_names[i])
	## Plots the gate
	image_name <- paste(quadrant_names[i], ".png", sep="")
	plotGraph(image_name, quadrants[[i]], x_axis, y_axis, nrow(quadrants[[i]]@exprs))
}
## Saves gate info in .txt file
	info_names <- 0 ## Initialises info names
	for(i in 1:4)
	{
		info_names[i] <- paste(quadrant_names[i], '.txt', sep="")
		axes_info <- paste(quadrant_names[i], "info.txt", sep="")
		c <- colnames(quadrants[[i]])
		write(c, file = axes_info)
	}
	writeInfoMultipleFilters(x, fres, info_names)
quit("no", 0)