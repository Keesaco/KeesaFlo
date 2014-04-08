###########################################################################
## \file compute_engine/boolean.r
## \brief Performs boolean gates of flow cytometry data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
source('rfunctions.r')
imports()

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
gate_name <- args[2]
boolean_op <- args[3]
gate1_type <- args[4]
points1 <- args[5]
reverse1 <- as.integer(args[6])
gate2_type <- args[7]
points2 <- args[8]
reverse2 <- as.integer(args[9])
x_axis <- args[10]
y_axis <- args[11]

## Read fcs data.
if(file.exists(fcs_name) == FALSE)
	quit("no", 1)
x <- read.FCS(fcs_name, transformation = FALSE)

## Find range of relevant observables
r1 <- range(x[,1])
r2 <- range(x[,2])

## Creates a gate object based on the specified parameters
if(gate1_type == 'rect')
{
	points <- pointsStringToVector(points1)
	points <- convertRectCoords(points[1], points[2], points[3], points[4], r1[1,1], r1[2,1], r2[1,1], r2[2,1])
	gate1 <- createRectGate(points[1], points[2], points[3], points[4], a, b)
} else if(gate1_type == 'oval')
{
	points <- pointsStringToVector(points1)
	points <- convertOvalCoords(points[1], points[2], points[3], points[4], points[5], points[6], r1[1,1], r1[2,1], r2[1,1], r2[2,1])
	gate1 <- createEllipsoidGate(points[1], points[2], points[3], points[4], points[5], points[6], a, b)
} else if(gate1_type == 'poly')
{
	points <- strsplit(points1, " ")
	l <- length(points[[1]])
	newPoints <- convertPolyCoords(points, l, r1[1,1], r1[2,1], r2[1,1], r2[2,1])
	gate1 <- createPolyGate(newPoints, l/2, x_axis, y_axis)
}

## Creates a second gate object based on the specified parameters
if(gate2_type == 'rect')
{
	points <- pointsStringToVector(points2)
	points <- convertRectCoords(points[1], points[2], points[3], points[4], r1[1,1], r1[2,1], r2[1,1], r2[2,1])
	gate2 <- createRectGate(points[1], points[2], points[3], points[4], a, b)
} else if(gate2_type == 'oval')
{
	points <- pointsStringToVector(points2)
	points <- convertOvalCoords(points[1], points[2], points[3], points[4], points[5], points[6], r1[1,1], r1[2,1], r2[1,1], r2[2,1])
	gate2 <- createEllipsoidGate(points[1], points[2], points[3], points[4], points[5], points[6], a, b)
} else if(gate2_type == 'poly')
{
	points <- strsplit(points2, " ")
	l <- length(points[[1]])
	newPoints <- convertPolyCoords(points, l, r1[1,1], r1[2,1], r2[1,1], r2[2,1])
	gate2 <- createPolyGate(newPoints, l/2, x_axis, y_axis)
}

## Creates subset of data based on gates and boolean operator
if(reverse1)
{
	gate1 <- !gate1
}
if(reverse2)
{
	gate2 <- !gate2
}

if(boolean_op == 'or')
{
	gate <-  gate1 | gate2
} else if(boolean_op == 'and')
{
	gate <- gate1 & gate2
}

## Creating subset of data.
y <- createSubset(x, gate, 0)

## Save gate as fcs file
write.FCS(y, gate_name)

## Saves gate info in a txt file
writeInfo(x, gate, 0)

## Plots the gate
image_name <- paste(gate_name, ".png", sep="")
plotGraph(image_name, y, x_axis, y_axis)
quit("no", 0)
