###########################################################################
## \file app/Notification/ListenerCollection.py
## \brief A package for creating callback lists
## \author jmccrea@keesaco.com of Keesaco
###########################################################################
## \package app.Notification.ListenerCollection
## \brief Provides classes for listeners and listener/subscription collections and alerting
###########################################################################

## \brief Defines a listener type with a callback
class Listener:

	###########################################################################
	## \brief Constructs a listener instance with a given callback method
	## \param self - instance reference
	## \param callback (= None) [Method] the callback to call when the listener is alerted
	## \return A Listener instance with the given callback
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, callback = None):
		## callback for this listener
		self.callback = callback				#set callback to passed callback
		## mute flag to temporarily disable callbacks for this listener
		self.__muted = False					#Start unmuted

	###########################################################################
	## \brief Calls the callback method so long as the listener is not muted or otherwise prevented from being alerted
	## \param self - instance reference
	## \param *args - arguments to call the callback with
	## \param **kwargs - named arguments to call the callback with
	## \return none
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def call(self, *args, **kwargs):
		if ( self.callback != None): 				#check a callback has been set
			if (not self.__muted):				#do not call if this listener has been muted
				self.callback(*args, **kwargs)		#call the listener's callback method

	###########################################################################
	## \brief Mutes or unmutes the listener
	## \param self - instance reference
	## \param mute - (= True) true mutes the listener, false unmutes the listener
	## \return none
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def mute(self, mute = True):
		self.__muted = mute					#set the muted flag with the given argument

	###########################################################################
	## \brief Unmutes the listener
	## \param self - instance reference
	## \return none
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def unmute(self):
		self.mute(False) 					#use the existing mute method in case more logic is added later

	###########################################################################
	## \brief Gets the current mute status
	## \param self - instance method
	## \return [Bool] true if muted false otherwise
	## \author jmccrea@keesaco.com Keesaco
	###########################################################################
	def is_muted(self):
		return self.__muted					#return muted flag

## \brief A simple collection of listeners
class ListenerCollection:

	###########################################################################
	## \brief Constructs a ListenerCollection object
	## \param self - instance reference
	## \return ListenerCollection object
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def __init__(self):
		## List of listeners
		self.listeners = []					#Initialise listeners with empty list

	###########################################################################
	## \brief Adds a listener to the listener collection
	## \param self - instance reference
	## \param listener - [Listener] the listener to be added
	## \return position at which the new listener was added
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def add_listener(self, listener):
		new_position = len(self.listeners)			#get position of next inserted element (current length)
		self.listeners.append(listener)				#add the new listener to the list
		return new_position					#return previously stored position

	###########################################################################
	## \brief alerts all callbacks (as long as they have not been muted)
	## \param self - instance reference
	## \param *args - arguments to pass to callbacks
	## \param **kwargs - named arguments to pass to callbacks
	## \return none
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def broadcast(self, *args, **kwargs):
		for l in self.listeners:				#For each listener
			l.call(*args, **kwargs)				#Call with given arguments

## \brief A more versatile listener collection for multiple events and listeners
class SubscriptionCollection:

	###########################################################################
	## \brief Constructs a SubscriptionCollection instance
	## \param self - instance reference
	## \return SubscriptionCollection instance
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def __init__(self):
		## List of events in the subscription table
		self.__events = []					#Initialise empty event list				
		## List of listeners which can be subscribed to events
		self.__listeners = []					#Initialise empty listener list
		## Subscription table of Boolean values such that __subscriptions[event_id][listener_id] is True if the Listener with ID listener_id is subscribed to the Event with ID event_id
		self.__subscriptions = []				#Initialise empty subscription table

	###########################################################################
	## \brief Adds a listener to the subscription collection with no subscriptions
	## \param self - instance reference
	## \param new_listener - [Listener] the listener to be added
	## \return [Int] ID which the listener was assigned, used for modifying subscriptions
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def add_listener(self, new_listener):
		new_id = len(self.__listeners)				#capture next listener ID
		self.__listeners.append(new_listener)			#add the new listener to the listener list
		for ev in self.__subscriptions:				#for all rows in the subscription table
			ev.append(False)				#append false so that new listener is subscribed to no events by default
		return new_id						#return the previously stored ID
	
	###########################################################################
	## \brief Adds a new event to the subscription collection, by default no listeners are subscribed
	## \param self - instance reference
	## \param new_event - [Event] the event to be added to the collection
	## \return [Int] the ID which the event was added with (used for modifying subscriptions and firing the event)
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def add_event(self, new_event):					
		new_id = len(self.__events)				#capture next event ID
		self.__events.append(new_event)				#add new event to event list
		self.__subscriptions.append( [False] * len(self.__listeners) ) #Add a row of all False to a new row in the subscription table so that no listeners are subscribed to the event
		return new_id						#return the ID of the new event

	###########################################################################
	## \brief Prints the subscription table as booleans such that 1 row is the listeners which are subscribed to an event in order of listener ID, rows in order of event ID
	## \param self - instance reference
	## \return none
	## \todo Remove or hide this method ("__dbg_print_table(...)")
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def dbg_print_table(self):
		for ev in self.__subscriptions:				#for each event row
			for ls in ev:					# for each listener
				print "%s\t"%(ls),			#  print whether the listener is subscribed to the event followed by a tab, inhibit the line break
			print ""					# line break

	###########################################################################
	## \brief Subscribes a given listener to a given event
	## \param self - instance reference
	## \param listener_id - [Int] The ID of the listener to subscribe
	## \param event_id - [Int] The ID of the event for the listener to be subscribed to
	## \param enable - (= True) [Boolean] True enables the subscription, False disables the subscription
	## \return none
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def subscribe(self, listener_id, event_id, enable = True):
		if (listener_id < len(self.__listeners)) and (event_id < len(self.__events)): #if the event and the listener exist
			self.__subscriptions[event_id][listener_id] = enable #set the subscription for the given event and subscription IDs to the passed enable value
		else:
			pass 						#listener or event doesn't exist

	###########################################################################
	## \brief alerts all callbacks (as long as they have not been muted)
	## \param self - instance reference
	## \param listener_id - [Int] The ID of the listener to unsubscribe
	## \param event_id - [Int] The ID of the event for the listener to be unsubscribed from
	## \return none
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def unsubscribe(self, listener_id, event_id):
		self.subscribe(listener_id, event_id, False) #Use existing subscribe method to avoid repeating code

	###########################################################################
	## \brief alerts all callbacks that are subscribed to the given event
	## \param self - instance reference
	## \param event_id - [Int] ID of the event to inform
	## \param *args - arguments to pass to callbacks
	## \param **kwargs - named arguments to pass to callbacks
	## \return none
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def broadcast_event(self, event_id, *args, **kwargs):
		if event_id < len(self.__events):			#if the event ID exists
			for x in range(len(self.__listeners)):	#For each listener
				if (self.__subscriptions[event_id][x]):	#if it is subscribed to the given event
					self.__listeners[x].call(*args, **kwargs) #call its callback with th given arguments
		else:
			pass 						#event doesn't exist
