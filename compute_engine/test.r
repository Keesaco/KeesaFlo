###########################################################################
## \file compute/visualise.r
## \brief Visualises flow cytometry data.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
library("flowCore")
library("flowViz")
library("methods")

# Read fcs data.
x <- read.FCS("test.fcs", transformation = FALSE)

# Plot data.
png("test.png")
plot(x)
#plot(x, "FSC-A", breaks = 256)
dev.off()