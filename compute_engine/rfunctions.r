###########################################################################
## \file compute_engine/rfunctions.r
## \brief Supplies functions to visualise flow cytometry data using Bioconductor.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################

###########################################################################
## \brief Imports necessary libraries for flow cytometry
###########################################################################
imports <- function()	
{
	library("flowCore")
	library("flowViz")
	library("methods")
}

###########################################################################
## \brief converts an x coordinate from the graph image to an x coordinate in the graph
## \param point -point to be converted
## \param xmin - minimum value x can take on the graph
## \param xmax - maximum value x can take on the graph
## \todo - change magic numbers
## \return returns new coordinate
###########################################################################
imageToGraphCoordx <- function(point, xmin, xmax)
{
	return(((point-73)/360) * (xmax-xmin))
}

###########################################################################
## \brief converts an y coordinate from the graph image to an x coordinate in the graph
## \param point -point to be converted
## \param ymin - minimum value y can take on the graph
## \param ymax - maximum value y can take on the graph
## \return returns new coordinate
###########################################################################
imageToGraphCoordy <- function(point, ymin, ymax)
{
	return(ymax - (((point-61)/332) * (ymax-ymin)))
}

###########################################################################
## \brief converts an all of the coorindates of a rectangle gate to graph coordinates
## \param tlx - top left x coordinate of the rectangle
## \param tly - top left y coordinate of the rectangle
## \param brx - bottom right x coordinate of the rectangle
## \param bry - bottom right y coordinate of the rectangle
## \param xmin - minimum value x can take on the graph
## \param xmax - maximum value x can take on the graph
## \param ymin - minimum value y can take on the graph
## \param ymax - maximum value y can take on the graph
## \return returns new coordinates
###########################################################################
convertRectCoords <- function(tlx, tly, brx, bry, xmin, xmax, ymin, ymax)
{
	tlx <- imageToGraphCoordx(tlx, xmin, xmax)
	brx <- imageToGraphCoordx(brx, xmin, xmax)
	tly <- imageToGraphCoordy(tly, ymin, ymax)
	bry <- imageToGraphCoordy(bry, ymin, ymax)
	return(c(tlx, tly, brx, bry))
}

###########################################################################
## \brief converts an all of the coorindates of a oval gate to graph coordinates
## \param mx - x coordinate of the center of the oval
## \param my - y coordinate of the center of the oval
## \param ax - x coordinate of the first point selected on the circumference of the oval
## \param ay - y coordinate of the first point selected on the circumference of the oval
## \param bx - x coordinate of the second point selected on the circumference of the oval
## \param by - y coordinate of the second point selected on the circumference of the oval
## \param xmin - minimum value x can take on the graph
## \param xmax - maximum value x can take on the graph
## \param ymin - minimum value y can take on the graph
## \param ymax - maximum value y can take on the graph
## \return returns new coordinates
###########################################################################
convertOvalCoords <- function(mx, my, ax, ay, bx, by, xmin, xmax, ymin, ymax)
{
	mx <- imageToGraphCoordx(mx, xmin, xmax)
	ax <- imageToGraphCoordx(ax, xmin, xmax)
	bx <- imageToGraphCoordx(bx, xmin, xmax)
	my <- imageToGraphCoordy(my, ymin, ymax)
	ay <- imageToGraphCoordy(ay, ymin, ymax)
	by <- imageToGraphCoordy(by, ymin, ymax)
	return(c(mx, my, ax, ay, bx, by))
}

###########################################################################
## \brief converts an all of the coorindates of a polygon gate to graph coordinates
## \param points - vector of points for the polygon (all x coordinates first)
## \param len - length of points vector ie. number of points * 2
## \param xmin - minimum value x can take on the graph
## \param xmax - maximum value x can take on the graph
## \param ymin - minimum value y can take on the graph
## \param ymax - maximum value y can take on the graph
## \return returns new coordinates
###########################################################################
convertPolyCoords <- function(points, len, xmin, xmax, ymin, ymax)
{
	point <- 0 ## initialises point
	for(i in 1:len)
	{
		point[i] <- as.numeric(points[[1]][i])
	}
	## Convert pixel coordinates to graph coordinates
	r <- len/2
	for(i in 1:r)
	{
		point[i] <- imageToGraphCoordx(point[i], xmin, xmax)
	}
	s <- r+1
	for(i in s:l)
	{
		point[i] <- imageToGraphCoordy(point[i], ymin, ymax)
	}
	return(point)
}

pointsStringToVector <- function(points)
{
	points <- strsplit(points, " ")
	len <- length(points[[1]])
	newPoints <- 0 ## initialises point
	for(i in 1:len)
	{
		newPoints[i] <- as.numeric(points[[1]][i])
	}
	return(newPoints)
}

###########################################################################
## \brief creates a rectangle gate
## \param topLeftlx - top left x coordinate of the rectangle
## \param topLefty - top left y coordinate of the rectangle
## \param bottomRightx - bottom right x coordinate of the rectangle
## \param bottomRighty - bottom right y coordinate of the rectangle
## \param x_axis - name of x_axis
## \param y_axis - name of y_axis
## \return returns rectangular gate
###########################################################################
createRectGate <- function(topLeftx, topLefty, bottomRightx, bottomRighty, x_axis, y_axis)
{
	mat <- matrix(c(topLeftx, bottomRightx, bottomRighty, topLefty), ncol=2, 
		dimnames=list(c("min", "max"), c(x_axis, y_axis)))
	return(rectangleGate(.gate=mat))
}

###########################################################################
## \brief creates an ellipsoid gate
## \param mean_x - x coordinate of the center of the oval
## \param mean_y - y coordinate of the center of the oval
## \param ax - x coordinate of the first point selected on the circumference of the oval
## \param ay - y coordinate of the first point selected on the circumference of the oval
## \param bx - x coordinate of the second point selected on the circumference of the oval
## \param by - y coordinate of the second point selected on the circumference of the oval
## \param x_axis - name of x_axis
## \param y_axis - name of y_axis
## \return returns ellipsoid gate
###########################################################################
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
	V <- matrix(c(v11, v21, v12, v22), ncol = 2, dimnames=list(c(x_axis, y_axis), 
		c(x_axis, y_axis)))
	L <- matrix(c(l1, 0, 0, l2), ncol = 2, dimnames=list(c(x_axis, y_axis), 
		c(x_axis, y_axis)))
	cov <- V %*% L %*% solve(V)
	## Creates the gating parameters
	mean <- c(a=mean_x, b=mean_y)
	return(ellipsoidGate(.gate = cov, mean = mean))
}

###########################################################################
## \brief creates polygon gate
## \param points - vector of points for the polygon (all x coordinates first)
## \param n - number of points forming polygon gate
## \param x_axis - name of x_axis
## \param y_axis - name of y_axis
## \return returns polygon gate
###########################################################################
createPolyGate <- function(points, n, x_axis, y_axis)
{
	rownames <- c(1:n)
	mat <- matrix(points, ncol=2, dimnames=list(rownames, c(x_axis, y_axis)))
	return(polygonGate(.gate=mat))
}

createBasicGate <- function(gate_type, coords, range_x, range_y, x_axis, y_axis)
{
	if(gate_type == 'rect')
	{
		points <- pointsStringToVector(coords)
		points <- convertRectCoords(points[1], points[2], points[3], points[4], 
			range_x[1,1], range_x[2,1], range_y[1,1], range_y[2,1])
		gate <- createRectGate(points[1], points[2], points[3], points[4], x_axis, y_axis)
	} else if(gate_type == 'oval')
	{
		points <- pointsStringToVector(coords)
		points <- convertOvalCoords(points[1], points[2], points[3], points[4], 
			points[5], points[6], range_x[1,1], range_x[2,1], range_y[1,1], range_y[2,1])
		gate <- createEllipsoidGate(points[1], points[2], points[3], points[4], 
			points[5], points[6], x_axis, y_axis)
	} else if(gate_type == 'poly')
	{
		points <- strsplit(coords, " ")
		l <- length(points[[1]])
		newPoints <- convertPolyCoords(points, l, range_x[1,1], range_x[2,1], 
			range_y[1,1], range_y[2,1])
		gate <- createPolyGate(newPoints, l/2, x_axis, y_axis)
	}
	return(gate)
}

###########################################################################
## \brief creates subset of data based on gate
## \param data - orginal flowFrame being gated
## \param gate - gate to be applied to data
## \param reverse - whether the gate being create is a reverse gate
## \return returns subsetting flowFrame
###########################################################################
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

###########################################################################
## \brief creates file containing gating data
## \param data - orginal flowFrame being gated
## \param gate - gate being applied to data
## \param reverse - whether the gate being create is a reverse gate
###########################################################################
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

###########################################################################
## \brief creates png of graph of data
## \param image_name - name of image file to be created
## \param data - data to be graphed
## \param x_axis - name of x_axis in graph
## \param y_axis - name of y_axis in graph
###########################################################################
plotGraph <- function(image_name, data, x_axis, y_axis)
{
	png(image_name)
	plot(data,c(x_axis, y_axis))
	dev.off()
}