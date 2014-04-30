###########################################################################
## \file compute_engine/axis.r
## \brief Gates flow cytometry data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
source('rfunctions.r')
imports()

## Parse arguments.
args <- commandArgs(trailingOnly = TRUE)
fcs_name <- args[1]
new_name <- args[2]
xaxis <- args[3]
yaxis <- args[4]

## Read file
if(file.exists(fcs_name) == FALSE)
	quit("no", 1)
x <- read.FCS(fcs_name, transformation = FALSE)

## New fcs file and info file and axes file
write.FCS(x, new_name)
axes_info <- paste(new_name, "info.txt", sep="")
c <- colnames(x)
write(c, file = axes_info)
total <- nrow(x)
proportion <- 1
info <- c(total, total, proportion)
info_name <- paste(new_name, ".txt", sep="")
write(info, file = info_name)

## Plot graph
vis_name <- paste(new_name, ".png", sep="")
png(vis_name)
plot(x,c(xaxis, yaxis))
dev.off()
quit("no", 0)