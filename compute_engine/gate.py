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
tlx = sys.argv[2]
tly = sys.argv[3]
brx = sys.argv[4]
bry = sys.argv[5]

## Load raw fcs data from cloud storage.
Ana.load_fcs(name)

## Create visualisation of raw fcs data.
Ana.rect_gate(name, tlx, tly, brx, bry)

## Save visualisation to cloud storage.
Ana.save_vis(name + 'gate.png')

## Clean up.
os.remove(name)
os.remove(name + 'gate.png')