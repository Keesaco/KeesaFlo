###########################################################################
## \file compute_engine/visualise.py
## \brief Supplies functions to visualise flow cytometry data using Bioconductor.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################

imports <- function()	
{
	library("flowCore")
	library("flowViz")
	library("methods")
}

## change magic numbers
imageToGraphCoordx <- function(point, xmin, xmax)
{
	return(((point-73)/360) * (xmax-xmin))
}

imageToGraphCoordy <- function(point, ymin, ymax)
{
	return(ymax - (((point-61)/332) * (ymax-ymin)))
}

createRectGate <- function(topLeftx, topLefty, bottomRightx, bottomRighty, x_axis, y_axis)
{
	mat <- matrix(c(topLeftx, bottomRightx, bottomRighty, topLefty), ncol=2, dimnames=list(c("min", "max"), c(x_axis, y_axis)))
	return(rectangleGate(.gate=mat))
}

createEllipsoidGate <- function(mean_x, mean_y, ax, ay, bx, by, x_axis, y_axis)
{
	l1 <- (ax-mean_x)^2+(ay-mean_y)^2
	l2 <- (bx-mean_x)^2+(by-mean_y)^2
	## Calculate eigenvectors of covariance matrix
	v11 <- ax-mean_x
	v12 <- ay-mean_y
	v21 <- v12 ## This ensures the eigenvectors are perpendicular to each other
	v22 <- -v11
	## Calculate covariance matrix
	V <- matrix(c(v11, v21, v12, v22), ncol = 2, dimnames=list(c(x_axis, y_axis), c(x_axis, y_axis)))
	L <- matrix(c(l1, 0, 0, l2), ncol = 2, dimnames=list(c(x_axis, y_axis), c(x_axis, y_axis)))
	cov <- V %*% L %*% solve(V)
	## Creates the gating parameters
	mean <- c(a=mx, b=my)
	return(ellipsoidGate(.gate = cov, mean = mean))
}

createPolyGate <- function(points, n, x_axis, y_axis)
{
	rownames <- c(1:r)
	mat <- matrix(points, ncol=2, dimnames=list(rownames, c(x_axis, y_axis)))
	return(polygonGate(.gate=mat))
}

createSubset <- function(data, gate, reverse)
{
	if(reverse)
	{
			y <- Subset(data, !gate)
	} else
	{
		y <- Subset(data, gate)
	}
	return(y)
}

writeInfo <- function(data, gate, reverse)
{
	if(reverse)
	{
		result <- filter(data, !gate)
	} else
	{
		result <- filter(data, gate)
	}
	total <- summary(result)$n
	inGate <- summary(result)$true
	proportion <- summary(result)$p
	info <- c(inGate, total, proportion)
	info_name <- paste(gate_name, ".txt", sep="")
	write(info, file = info_name)
}

plotGraph <- function(image_name, data, x_axis, y_axis)
{
	png(image_name)
	plot(data,c(x_axis, y_axis))
	dev.off()
}