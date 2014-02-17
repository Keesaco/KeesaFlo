###########################################################################
## \file app/Analysis/Manager/startup.sh
## \brief Runs the FCS analysis on new instances.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################

#!/bin/bash
## Obtains the file location from the metadata of the instance request.
FILE_LOCATION=$(curl http://metadata/computeMetadata/v1/instance/attributes/file_location -H "X-Google-Metadata-Request: True")
## Runs the analysis on the file location.
python visualise.py "$FILE_LOCATION"