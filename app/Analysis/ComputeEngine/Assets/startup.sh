###########################################################################
## \file app/Analysis/Manager/startup.sh
## \brief Sets up Compute Engine and runs the FCS analysis on new instances.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################

#!/bin/bash
## Obtains the file location from the metadata of the instance request.
#FILE_LOCATION=$(curl http://metadata/computeMetadata/v1/instance/attributes/file_location -H "X-Google-Metadata-Request: True")
## Obtains the instance name from the metadata of the instance request.
INSTANCE_NAME=$(curl http://metadata/computeMetadata/v1/instance/attributes/instance_name -H "X-Google-Metadata-Request: True")
## Move to the analysis directory.
cd Analysis
## Download analysis scripts from Google Cloud Storage.
gsutil cp -R gs://keesaco_compute_engine/compute_engine/* .
## Runs the visualisation script
python visualise.py
## Shut own instance down.
gcutil deleteinstance "$INSTANCE_NAME" -f --nodelete_boot_pd
#echo "INSTANCE SHOULD BE SHUT DOWN"
