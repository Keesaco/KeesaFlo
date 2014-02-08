###########################################################################
## \file compute/visualise.py
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Depends on AnalysisAPI.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package compute.visualise
## \brief Visualises flow cytometry data using Google Cloud Storage and Bioconductor. Should be called by the Compute Engine startup sheel script. Depends on AnalysisAPI.
###########################################################################
import sys, AnalysisAPI

# Parse command line arguments from shell script.
arg_name = sys.argv[1]
name = arg_name[:-4]

# Analyse data.
AnalysisAPI.load_fcs(name + '.fcs')
AnalysisAPI.visualise(name + '.fcs', name + '.png')
AnalysisAPI.save_vis(name + '.png')
