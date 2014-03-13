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

class TestPALPerissions(unittest.TestCase):

	def SetUp(self):
		pass

	def TearDown(self):
		pass

	def test_user_add_user(self):
		usr = User('somebody@somewhere.com')
		usr.set_nickname('Somebody')
		usr.set_user_id('SomeUserid1234')
		ret = ps.add_user(usr)
		self.assertTrue(isinstance(ret, ndb.Key))

	def test_user_remove_user_by_id_1(self):
		self.assertFalse(ps.remove_user_by_id('userThatDoesntExist'))

	def test_user_remove_user_by_id_2(self):
		usr = User('somebody@somewhere.com')
		usr.set_nickname('Somebody')
		usr.set_user_id('SomeUserid1234')
		ps.add_user(usr)
		self.assertTrue(ps.remove_user_by_id('SomeUserid1234'))




