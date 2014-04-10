###########################################################################
## \file 	app/API/PALDatastore.py
## \brief 	Containts the PALLogging package: Platform Abstraction Layer
##			for application event logging
## \author 	jmccrea@keesaco.com of Keesaco
###########################################################################
## \package app.API.PALLogging
## \brief 	Contains abstraction layer functions for logging application
##			events with varying severity
## \note 	Depends on the Google App Engine logging API
## \note 	Currenty only supports writing to logs - whilst the Google API
##			which this abstracts does support reading logs programatically
##			this is not implemented at this time
###########################################################################

import logging

###########################################################################
## \brief Creates a log at the debug level
## \param String msg - the message to log
## \return None
## \author jmccrea@keesaco.com of Keesaco
###########################################################################
def log_debug(msg):
	logging.debug(msg)

###########################################################################
## \brief Creates a log at the info level
## \param String msg - the message to log
## \return None
## \author jmccrea@keesaco.com of Keesaco
###########################################################################
def log_info(msg):
	logging.info(msg)

###########################################################################
## \brief Creates a log at the warning level
## \param String msg - the message to log
## \return None
## \author jmccrea@keesaco.com of Keesaco
###########################################################################
def log_warning(msg):
	logging.warning(msg)

###########################################################################
## \brief Creates a log at the error level
## \param String msg - the message to log
## \return None
## \author jmccrea@keesaco.com of Keesaco
###########################################################################
def log_error(msg):
	logging.error(msg)

###########################################################################
## \brief Creates a log at the critical level
## \param String msg - the message to log
## \return None
## \author jmccrea@keesaco.com of Keesaco
###########################################################################
def log_critical(msg):
	logging.critical(msg)