###########################################################################
## \file app/Analysis/Manager/startup.sh
## \brief Sets up Compute Engine and runs the FCS analysis on new instances.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################

#!/bin/bash
## Get metadata.
INSTANCE_NAME=$(curl http://metadata/computeMetadata/v1/instance/attributes/instance_name -H "X-Google-Metadata-Request: True")
SCRIPT_URL=$(curl http://metadata/computeMetadata/v1/instance/attributes/script_url -H "X-Google-Metadata-Request: True")
LOG_URL=$(curl http://metadata/computeMetadata/v1/instance/attributes/log_url -H "X-Google-Metadata-Request: True")
## Move to the analysis directory.
cd Analysis
## Log time instance starts.
echo "Instance starts: " &>> "$INSTANCE_NAME".log
date &>> "$INSTANCE_NAME".log
## Download analysis scripts from Google Cloud Storage.
gsutil cp -R gs://"$SCRIPT_URL"/* . &>> "$INSTANCE_NAME".log
## Run and log the visualisation script
python visualise.py &>> "$INSTANCE_NAME".log
## Log time instance terminates
echo "Instance terminates: " &>> "$INSTANCE_NAME".log
date &>> "$INSTANCE_NAME".log
## Save logs to cloud storage bucket.
gsutil cp "$INSTANCE_NAME".log gs://"$LOG_URL"/
## Shut own instance down.
gcutil deleteinstance "$INSTANCE_NAME" -f
