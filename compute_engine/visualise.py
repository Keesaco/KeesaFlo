###########################################################################
## \file compute_engine/visualise.py
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Depends on AnalysisAPI.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package compute_engine.visualise
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Should be called by the Compute Engine startup sheel script. Depends on AnalysisAPI.
###########################################################################
import sys, os
import API.APIAnalysis as Ana

## Parse command line arguments given by Compute Engine's statup shell script, stripping '.fcs'.
arg_name = sys.argv[1]
name = arg_name[:-4]

## Load raw fcs data from cloud storage.
Ana.load_fcs(name + '.fcs')

## Create visualisation of raw fcs data.
Ana.visualise(name)

## Save visualisation to cloud storage.
Ana.save_vis(name + '.png')

## Clean up.
os.remove(name + '.fcs')
os.remove(name + '.png')