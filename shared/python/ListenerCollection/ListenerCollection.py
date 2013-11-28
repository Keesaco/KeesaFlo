## \file shared/python/ListenerCollection/ListenerCollection.py
# \brief A package for creating callback lists
# \author jmccrea@keesaco.com of Keesaco

## \brief Defines a listener type with a callback
class Listener:

	## \brief Constructs a listener instance with a given callback method
	# \param self - instance reference
	# \param callback (= None) [Method] the callback to call when the listener is alerted
	# \return A Listener instance with the given callback
	# \author jmccrea@keesaco.com of Keesaco
	def __init__(self, callback = None):
		## callback for this listener
		self.callback = callback				#set callback to passed callback
		## mute flag to temporarily disable callbacks for this listener
		self.__muted = False					#Start unmuted

	## \brief Calls the callback method so long as the listener is not muted or otherwise prevented from being alerted
	# \param self - instance reference
	# \param *args - argument list to pass to callback
	# \return none
	# \author jmccrea@keesaco.com of Keesaco
	def call(self, *args, **kwargs):
		if ( self.callback != None): 			#check a callback has been set
			if (not self.__muted):				#do not call if this listener has been muted
				self.callback(*args, **kwargs)	#call the listener's callback method

	## \brief Mutes or unmutes the listener
	# \param self - instance reference
	# \param mute - (= True) true mutes the listener, false unmutes the listener
	# \return none
	# \author jmccrea@keesaco.com of Keesaco
	def mute(self, mute = True):
		self.__muted = mute						#set the muted flag with the given argument

	## \brief Unmutes the listener
	# \param self - instance reference
	# \return none
	# \author jmccrea@keesaco.com of Keesaco
	def unmute(self):
		self.mute(False) 						#use the existing mute method in case more logic is added later

	## \brief Gets the current mute status
	# \param self - instance method
	# \return [Bool] true if muted false otherwise
	# \author jmccrea@keesaco.com Keesaco
	def is_muted(self):
		return self.__muted						#return muted flag

## \brief A simple collection of listeners
class ListenerCollection:

	## \brief Constructs a ListenerCollection object
	# \param self - instance reference
	# \return ListenerCollection object
	# \author jmccrea@keesaco.com of Keesaco
	def __init__(self):
		self.listeners = []						#Initialise listeners with empty list

	## \brief Adds a listener to the listener collection
	# \param self - instance reference
	# \param listener - [Listener] the listener to be added
	# \return position at which the new listener was added
	# \author jmccrea@keesaco.com of Keesaco
	def add_listener(self, listener):
		new_position = len(self.listeners)		#get position of next inserted element (current length)
		self.listeners.append(listener)			#add the new listener to the list
		return new_position						#return previously stored position

	## \brief alerts all callbacks (as long as they have not been muted)
	# \param self - instance reference
	# \param *args - argument list to pass to callback
	# \return none
	# \author jmccrea@keesaco.com of Keesaco
	def broadcast(self, *args, **kwargs):
		for l in self.listeners:				#For each listener
			l.call(*args, **kwargs)				#Call with given argument list

# \brief A more versatile listener collection for multiple events and listeners
class SubscriptionCollection:

	def __init__(self):
		self.__events = []
		self.__listeners = []
		self.__subscriptions = []


	def add_listener(self, new_listener):
		new_id = len(self.__listeners)
		self.__listeners.append(new_listener)
		for ev in self.__subscriptions:
			ev.append(False)
		return new_id
			
	def add_event(self, new_event):
		new_id = len(self.__events)
		self.__events.append(new_event)
		self.__subscriptions.append( [False] * len(self.__listeners) )
		return new_id
	
	def dbg_print_table(self):
		for ev in self.__subscriptions:
			for ls in ev:
				print "%s\t"%(ls),
			print ""

	def subscribe(self, listener_id, event_id, enable = True):
		if (listener_id < len(self.__listeners)) and (event_id < len(self.__events)):
			self.__subscriptions[event_id][listener_id] = enable
		else:
			pass							#listener or event doesn't exist

	def unsubscribe(self, listener_id, event_id):
		self.subscribe(listener_id, event_id, False)
