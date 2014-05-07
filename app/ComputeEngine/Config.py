###########################################################################
## \file app/Analysis/ComputeEngine/ComputeEngineConfig.py
## \brief Contains constants which change how instantiations are made on compute engine.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.ComputeEngine.ComputeEngineConfig
## \brief Provides constants to administrate instantiations on compute engine.
###########################################################################

## This avoids naming confusion between separate instances running in the same project by tagging them with a unique, lower-case string.
UNIQUE_NAME = 'keesaflo'

## The id of the project as it appears on Google Cloud Developers Console.
PROJECT_ID = 'keesaco-spe'
## The default zone to be used for Google Compute Engine.
DEFAULT_ZONE = 'europe-west1-a'
## The minimum number of instances which can exist simultaneously.
MIN_INSTANCES = 1
## The maximum number of instances which can exist simultaneously.
MAX_INSTANCES = 5
## The desired ratio of tasks to instances.
CE_SCALING = 5
## The slack percentage in the scaling ratio.
CE_SLACK = 0.3

## The Compute Engine version.
API_VERSION = 'v1'

## The email for the service account to be used.
SERVICE_ACCOUNT_EMAIL = '41520595559-5smi2i2nlql32u488dr0ig5epladi0hq@developer.gserviceaccount.com'
## The name of the private key file.
PRIVATE_KEY = 'private_key.pem'
## The scope covered by the authentication request.
GCE_SCOPE = 'https://www.googleapis.com/auth/compute'

## The name of the disk image to use for persistent disks.
DEFAULT_IMAGE = 'debian-bioconductor5'
## The root name of the persistent disks created.
DEFAULT_PD_NAME = '%s-root-pd-' % UNIQUE_NAME
## The root name of the instances created.
DEFAULT_INSTANCE_NAME = '%s-analysis-' % UNIQUE_NAME

## The default machine type to run instances on.
DEFAULT_MACHINE_TYPE = 'n1-standard-1'
## The default network for instances to communicate over.
DEFAULT_NETWORK = 'default'
## The default service email.
DEFAULT_SERVICE_EMAIL = 'default'
## The control scopes of instances.
DEFAULT_SCOPES = [	'https://www.googleapis.com/auth/devstorage.full_control',
					'https://www.googleapis.com/auth/compute',
					'https://www.googleapis.com/auth/taskqueue'	]

## The name of the startup script to run on instantiation.
STARTUP_SCRIPT = 'startup.sh'

## The URL of Google Compute Engine
GCE_URL = 'https://www.googleapis.com/compute/%s/projects/' % (API_VERSION)
## The URL of the project.
PROJECT_URL = '%s%s' % (GCE_URL, PROJECT_ID)
## The URL of the disk image to use.
IMAGE_URL = '%s/global/images/%s' % (PROJECT_URL, DEFAULT_IMAGE)
## The URL of the sone to use.
ZONE_URL = '%s/zones/%s' % (PROJECT_URL, DEFAULT_ZONE)
## The URL of the machine type to use.
MACHINE_TYPE_URL = '%s/machineTypes/%s' % (ZONE_URL, DEFAULT_MACHINE_TYPE)
## The URL of the network to use.
NETWORK_URL = '%s/global/networks/%s' % (PROJECT_URL, DEFAULT_NETWORK)
## The URL of the Assets folder.
ASSETS_URL = 'ComputeEngine'
## The URL of the startup.sh script.
STARTUP_URL = '%s/%s' % (ASSETS_URL, STARTUP_SCRIPT)
## The URL of the private key.
PRIVATE_KEY_URL = '%s/%s' % (ASSETS_URL, PRIVATE_KEY)

## The URL of the instance scripts.
SCRIPT_URL = 'keesaco_gce'
## The URL of the compute engine scripts.
LOG_URL = 'keesaco_log'

## The URL of the instance balancing hook.
BALANCE_HOOK = "http://www.%s.appspot.com/_ah/balance" % PROJECT_ID
