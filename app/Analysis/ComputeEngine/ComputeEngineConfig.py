###########################################################################
## \file app/Analysis/ComputeEngine/ComputeEngineConfig.py
## \brief Contains constants which change how instantiations are made on compute engine.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.ComputeEngine.ComputeEngineConfig
## \brief Provides constants to modify instantiations on compute engine.
###########################################################################

from Analysis import AdminConfig

## The id of the project as it appears on Google Cloud Developers Console.
PROJECT_ID = 'keesaco-spe'
## The default zone to be used for Google Compute Engine.
DEFAULT_ZONE = 'europe-west1-a'
## The maximum number of instances which can exist simultaneously.
MAX_INSTANCES = AdminConfig.MAX_TOTAL_TASKS

## The Compute Engine version.
API_VERSION = 'v1'

## The name of the authentication json file.
CLIENT_SECRETS = 'client_secrets.json'
## The .dat file in which authentication is stored.
OAUTH2_STORAGE = 'oauth2.dat'
## The scope covered by the authentication request.
GCE_SCOPE = 'https://www.googleapis.com/auth/compute'

## The name of the disk image to use for persistent disks.
DEFAULT_IMAGE = 'debian-bioconductor3'
## The root name of the persistent disks created.
DEFAULT_PD_NAME = 'flowcloud-root-pd-'

## The default machine type to run instances on.
DEFAULT_MACHINE_TYPE = 'f1-micro'
## The default network for instances to communicate over.
DEFAULT_NETWORK = 'default'
## The default service email.
DEFAULT_SERVICE_EMAIL = 'default'
## Tha control scopes of instances.
DEFAULT_SCOPES = [	'https://www.googleapis.com/auth/devstorage.full_control',
					'https://www.googleapis.com/auth/compute']

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
## The file path of the storage container for authentication
STORAGE_URL = 'Analysis/ComputeEngine/Assets/%s' % OAUTH2_STORAGE
## The file path of the client_secrets.json file
SECRETS_URL = 'Analysis/ComputeEngine/Assets/%s' % CLIENT_SECRETS
## The file path of the startup script
STARTUP_URL = 'Analysis/ComputeEngine/Assets/%s' % STARTUP_SCRIPT



