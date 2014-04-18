###########################################################################
## \file compute_engine/gate.r
## \brief Performs basic gates of flow cytometry data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
source('rfunctions.r')
imports()

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
gate_name <- args[2]
gate_type <- args[3]
reverse <- as.integer(args[4])
if(gate_type == 'rect')
{
	tlx <- as.integer(args[5])
	tly <- as.integer(args[6])
	brx <- as.integer(args[7])
	bry <- as.integer(args[8])
	x_axis <- args[9]
	y_axis <- args[10]
} else if(gate_type == 'oval')
{
	mx <- as.integer(args[5])
	my <- as.integer(args[6])
	ax <- as.integer(args[7])
	ay <- as.integer(args[8])
	bx <- as.integer(args[9])
	by <- as.integer(args[10])
	x_axis <- args[11]
	y_axis <- args[12]
} else if(gate_type == 'poly')
{
	points <- args[5]
	x_axis <- args[6]
	y_axis <- args[7]
}

## Read fcs data.
if(file.exists(fcs_name) == FALSE)
	quit("no", 1)
x <- read.FCS(fcs_name, transformation = FALSE)

## Find range of relevant observables
r1 <- range(x[,1])
r2 <- range(x[,2])

## Creates a gate object based on the specified parameters
if(gate_type == 'rect')
{
	points <- convertRectCoords(tlx, tly, brx, bry, r1[1,1], r1[2,1], r2[1,1], r2[2,1])
	gate <- createRectGate(points[1], points[2], points[3], points[4], x_axis, y_axis)
} else if(gate_type == 'oval')
{
	points <- convertOvalCoords(mx, my, ax, ay, bx, by, r1[1,1], r1[2,1], r2[1,1], r2[2,1])
	gate <- createEllipsoidGate(points[1], points[2], points[3], points[4], points[5], points[6], x_axis, y_axis)
} else if(gate_type == 'poly')
{
	points <- strsplit(points, " ")
	l <- length(points[[1]])
	newPoints <- convertPolyCoords(points, l, r1[1,1], r1[2,1], r2[1,1], r2[2,1])
	gate <- createPolyGate(newPoints, l/2, x_axis, y_axis)
}

## Creating subset of data.
y <- createSubset(x, gate, reverse)

## Save gate as fcs file
write.FCS(y, gate_name)

## Saves gate info in a txt file
writeInfo(x, gate, reverse)

## Plots the gate
image_name <- paste(gate_name, ".png", sep="")
plotGraph(image_name, y, x_axis, y_axis)
quit("no", 0)
