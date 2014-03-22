###########################################################################
## \file compute_engine/polygate.r
## \brief Gates flow cytometry data with a polygon.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
library("flowCore")
library("flowViz")
library("methods")

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
gate_name <- args[2]
points <- args[3]

## Read fcs data
x <- read.FCS(fcs_name, transformation = FALSE)

## Finding first two observables
a <- colnames(x[,1])
b <- colnames(x[,2])

## Parses the points and changes them to numeric
points <- strsplit(points, " ")
l <- length(points[[1]])
point <- 0 ## initialises point
for(i in 1:l)
{
	point[i] <- as.numeric(points[[1]][i])
}

## Convert pixel coordinates to graph coordinates
r1 <- range(x[,1])
r2 <- range(x[,2])
r <- l/2
for(i in 1:r)
{
	point[i] <- ((point[i]-73)/360) * (r1[2,1]-r1[1,1])
}
s <- r+1
for(i in s:l)
{
	point[i] <- r2[2,1] - (((point[i]-61)/332) * (r2[2,1]-r2[1,1]))
}

## Creates polygon gate from points
rownames <- c(1:r)
mat <- matrix(point, ncol=2, dimnames=list(rownames, c(a,b)))
pgate <- polygonGate(.gate=mat)
y <- Subset(x, pgate)

## Save gate as fcs file
write.FCS(y, gate_name)

## Calculating proportion
result <- filter(x, pgate)
total <- summary(result)$n
inGate <- summary(result)$true
proportion <- summary(result)$p
info <- c(inGate, total, proportion)
info_name <- paste(gate_name, ".txt", sep="")
write(info, file = info_name)

## Plotting the gate
image_name <- paste(gate_name, ".png", sep="")
png(image_name)
plot(y,c(a, b))
dev.off()
