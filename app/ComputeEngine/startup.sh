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
echo "Instance starts: " &>> "$INSTANCE_NAME".txt
date &>> "$INSTANCE_NAME".txt
## Download analysis scripts from Google Cloud Storage.
gsutil cp -R gs://"$SCRIPT_URL"/* . 2>&1 | tee -a "$INSTANCE_NAME".txt
## Run and log the visualisation script
python visualise.py 2>&1 | tee -a "$INSTANCE_NAME".txt
## Log time instance terminates
echo "Instance terminates: " &>> "$INSTANCE_NAME".txt
date &>> "$INSTANCE_NAME".txt
## Save logs to cloud storage bucket.
gsutil cp "$INSTANCE_NAME".txt gs://"$LOG_URL"/
## Shut own instance down.
gcutil deleteinstance "$INSTANCE_NAME" -f --nodelete_boot_pd
