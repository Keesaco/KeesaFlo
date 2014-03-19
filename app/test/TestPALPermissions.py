###########################################################################
## \file 	app/test/TestPALPermissions.py
## \brief 	Containts test cases for the Permissions PAL
## \author 	cwike@keesaco.com of Keesaco
###########################################################################
## \package app.test.TestPALPermissions
## \brief 	Contains test cases for the Permissions PAL
###########################################################################

import unittest
from google.appengine.ext import testbed, ndb

import API.PALPermissions as ps

from API.User import User

###########################################################################
## \brief 	Testing for Permissions table PAL
## \author 	cwike@Keesaco.com of Keesaco
###########################################################################
class TestPALPerissions(unittest.TestCase):

	###########################################################################
	## \brief 	setup method for testing
	## \note	placeholder 
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def SetUp(self):
		pass

	###########################################################################
	## \brief 	Teardown method for testing
	## \note	placeholder
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def TearDown(self):
		pass

	###########################################################################
	## \brief 	Tests adding user
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_add_user(self):
		usr = User('somebody@somewhereau.com')
		usr.set_nickname('Somebodyau')
		usr.set_user_id('SomeUserid1234au')
		ret = ps.add_user(usr)
		self.assertTrue(isinstance(ret, ndb.Key))

	###########################################################################
	## \brief 	Tests removing non existent user by id
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_remove_user_by_id_fail(self):
		self.assertFalse(ps.remove_user_by_id('userThatDoesntExist'))

	###########################################################################
	## \brief 	Tests removing existing user by id
	## \note	depends on functioning add_user function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_remove_user_by_id_succeed(self):
		usr = User('somebody@somewhereruis.com')
		usr.set_nickname('Somebodyruis')
		usr.set_user_id('SomeUserid1234ruis')
		ps.add_user(usr)
		self.assertTrue(ps.remove_user_by_id('SomeUserid1234'))

	###########################################################################
	## \brief 	Tests removing non existent user by key 
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_remove_user_by_key_fail(self):
		fakeKey = ndb.Key("doesntExist","noReally")
		self.assertFalse(ps.remove_user_by_key(fakeKey))

	###########################################################################
	## \brief 	Tests removing existing user by key
	## \note 	depends on functioning add_user function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_remove_user_by_key_succeed(self):
		usr = User('somebody@somewhereruks.com')
		usr.set_nickname('Somebodyruks')
		usr.set_user_id('SomeUserid1234ruks')
		ukey = ps.add_user(usr)
		self.assertTrue(ps.remove_user_by_key(ukey))

	###########################################################################
	## \brief 	Tests modifying non existant user by id
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_modify_user_by_id_fail(self):
		self.assertNone(ps.modify_user_by_id("AWSEDRFGYHUJUG23151"))

	###########################################################################
	## \brief 	Tests modifying existing user by id
	## \note 	depends on functioning add_user, get_user_by_key function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_modify_user_by_id_succeed(self):
		usr = User('somebody@somewheremids.com')
		usr.set_nickname('Somebodymids')
		usr.set_user_id('SomeUserid1234mids')
		ps.add_user(usr)
		newusr = User('somebodyelse@somewhereelsemids.com')
		newusr.set_nickname('SomebodyElsemids')
		newusr.set_user_id('SomeUotherId3878mids')
		key = ps.modify_user_by_id('SomeUserid1234mids',newusr)

		self.assertEqual(ps.get_user_by_key(key).email_address,newuser.email())

	###########################################################################
	## \brief 	Tests getting non existant user by id
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_get_user_by_id_fail(self):
		self.assertNone(ps.get_user_by_id("AWSEDRFGYHUJUG23151"))

	###########################################################################
	## \brief 	Tests getting existing user by id
	## \note 	depends on functioning add_user function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_get_user_by_id_succeed(self):
		usr = User('somebody@somewhereguis.com')
		usr.set_nickname('Somebodyguis')
		usr.set_user_id('SomeUserid1234guis')
		ps.add_user(usr)

		self.assertEqual(ps.get_user_by_id('SomeUserid1234guis').email_address, usr.email())

	###########################################################################
	## \brief 	Tests getting nonexistant user by key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_get_user_by_key_fail(self):
		fakeKey = ndb.Key("doesntExist","noReally")
		self.assertNone(ps.get_user_by_key(fakeKey))

	###########################################################################
	## \brief 	Tests getting existing user by key
	## \note 	depends on functioning add_user function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_get_user_by_key_succeed(self):
		usr = User('somebody@somewhereguks.com')
		usr.set_nickname('Somebodyguks')
		usr.set_user_id('SomeUserid1234guks')
		key = ps.add_user(usr)

		self.assertEqual(ps.get_user_by_key(key).email_address, usr.email())
	