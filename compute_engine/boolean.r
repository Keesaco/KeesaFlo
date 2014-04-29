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
gate2_x_axis <- args[12]
gate2_y_axis <- args[13]

## Read fcs data.
if(file.exists(fcs_name) == FALSE)
	quit("no", 1)
x <- read.FCS(fcs_name, transformation = FALSE)

## Find range of relevant observables
r1 <- range(x[,x_axis])
r2 <- range(x[,y_axis])

## Creates a gate object based on the specified parameters
gate1 <- createBasicGate(gate1_type, points1, r1, r2, x_axis, y_axis)

## Creates a second gate object based on the specified parameters
gate2 <- createBasicGate(gate2_type, points2, r1, r2, gate2_x_axis, gate2_y_axis)

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
plotGraph(image_name, y, x_axis, y_axis, nrow(y@exprs))
quit("no", 0)
