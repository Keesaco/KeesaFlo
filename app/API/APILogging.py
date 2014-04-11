###########################################################################
## \file 	app/API/APILogging.py
## \brief 	Defines the logging API for logging application events - built
##			upon PALLogging for platform independence
## \author 	jmccrea@keesaco.com of Keesaco
###########################################################################
## \package app.API.APILogging
## \brief Provides methods for logging application events
## \note Depends on PALLogging
###########################################################################

import API.PALLogging as PAL

###########################################################################
## \brief	Defines numeric log levels
## \note	Written as a class as Python 2.7 does not have enumerate types
###########################################################################
class LogLevels:
	LOG_LEVEL_DEBUG 	= 0
	LOG_LEVEL_INFO		= 1
	LOG_LEVEL_WARNING	= 2
	LOG_LEVEL_ERROR		= 3
	LOG_LEVEL_CRITICAL	= 4
	LOG_LEVEL_DEFAULT	= LOG_LEVEL_INFO



## maps numeric log levels to logging methods
log_level_mapping = {
	LogLevels.LOG_LEVEL_DEBUG 		: PAL.log_debug,
	LogLevels.LOG_LEVEL_INFO		: PAL.log_info,
	LogLevels.LOG_LEVEL_WARNING		: PAL.log_warning,
	LogLevels.LOG_LEVEL_ERROR		: PAL.log_error,
	LogLevels.LOG_LEVEL_CRITICAL	: PAL.log_critical
}

###########################################################################
## \brief 	Creates a log at a given level
##
## \param 	String msg - the message to log
## \param	Int leve - (= LogLevels.LOG_LEVEL_DEFAULT) - the level of log
##			entry to create.
## \return 	None
## \note	Uses log_level_mapping as a lookup for the logging function to
##			use. If no entry is found for the given level, the the default
##			level is used. If the default level is not in the dictionary
##			PALLogging.log_warning is used.
## \author 	jmccrea@keesaco.com of Keesaco
###########################################################################
def log(msg, level = LogLevels.LOG_LEVEL_DEFAULT):
	if level in log_level_mapping:
		log_function = log_level_mapping[level]
		log_function(msg)
	
	elif LogLevels.LOG_LEVEL_DEFAULT in log_level_mapping:
		log_function = log_level_mapping[LogLevels.LOG_LEVEL_DEFAULT]
		log_function("[unknown log level] " + msg)

	## final fallback incase the dictionary doesn't have and entry for the default log level
	else:
		PAL.log_warning("[NO DEFAULT LOG LEVEL] " + msg)


###########################################################################
## \brief 	Creates a log at the debug level
## \param 	String msg - the message to log
## \return 	None
## \author 	jmccrea@keesaco.com of Keesaco
## \note 	This is a wrapper around .log for convenience
###########################################################################
def debug(msg):
	log(msg, LogLevels.LOG_LEVEL_DEBUG)

###########################################################################
## \brief 	Creates a log at the info level
## \param 	String msg - the message to log
## \return 	None
## \author 	jmccrea@keesaco.com of Keesaco
## \note 	This is a wrapper around .log for convenience
###########################################################################
def info(msg):
	log(msg, LogLevels.LOG_LEVEL_INFO)

###########################################################################
## \brief 	Creates a log at the warning level
## \param 	String msg - the message to log
## \return 	None
## \author 	jmccrea@keesaco.com of Keesaco
## \note 	This is a wrapper around .log for convenience
###########################################################################
def warning(msg):
	log(msg, LogLevels.LOG_LEVEL_WARNING)

###########################################################################
## \brief 	Creates a log at the error level
## \param 	String msg - the message to log
## \return 	None
## \author 	jmccrea@keesaco.com of Keesaco
## \note 	This is a wrapper around .log for convenience
###########################################################################
def error(msg):
	log(msg, LogLevels.LOG_LEVEL_ERROR)

###########################################################################
## \brief 	Creates a log at the critical level
## \param 	String msg - the message to log
## \return 	None
## \author 	jmccrea@keesaco.com of Keesaco
## \note 	This is a wrapper around .log for convenience
###########################################################################
def critical(msg):
	log(msg, LogLevels.LOG_LEVEL_CRITICAL)




