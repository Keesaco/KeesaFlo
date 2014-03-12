###########################################################################
## \file compute_engine/gate.py
## \brief Gates flow cytometry data using Google Cloud Storage and Bioconductor. Depends on AnalysisAPI.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
## \package compute_engine.gate
## \brief Gates flow cytometry data using Google Cloud Storage and Bioconductor. Depends on AnalysisAPI.
###########################################################################
import sys, os
import API.APIAnalysis as Ana

## Parse command line arguments given by Compute Engine's startup shell script.
name = sys.argv[1]
gate_type = sys.argv[2]
points = sys.argv[3]

## Load raw fcs data from cloud storage.
Ana.load_fcs(name)

## Create visualisation of raw fcs data.
if gate_type == "R":
	args = points.split()
	Ana.rect_gate(name, args[0], args[1], args[2], args[3])
elif gate_type == "O":
	args = points.split()
	Ana.oval_gate(name, args[0], args[1], args[2], args[3], args[4], args[5])
else:
	Ana.poly_gate(name, points)

## Save visualisation to cloud storage.
Ana.save_vis(name + 'gate.png')

## Clean up.
os.remove(name)
os.remove(name + 'gate.png')