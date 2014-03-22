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

import API.APIPermissions as ps

from API.User import User
from Permissions.Types import Permissions

###########################################################################
## \brief 	Testing for Permissions table PAL
## \author 	cwike@Keesaco.com of Keesaco
###########################################################################
class TestAPIPermissions(unittest.TestCase):

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

		self.assertTrue(ps.remove_user_by_id('SomeUserid1234ruis'))

	###########################################################################
	## \brief 	Tests removing non existent user by key 
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_remove_user_by_key_fail(self):
		badKey = "asdfasdf"

		self.assertFalse(ps.remove_user_by_key(badKey))

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
		usr = User('somebody@somewheremidf.com')
		usr.set_nickname('Somebodymidf')
		usr.set_user_id('SomeUserid1234midf')

		self.assertFalse(ps.modify_user_by_id("AWSEDRFGYHUJUG23151",usr))

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

		self.assertEqual(ps.get_user_by_key(key).email(), newusr.email())

	###########################################################################
	## \brief 	Tests getting non existant user by id
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_get_user_by_id_fail(self):
		self.assertIsNone(ps.get_user_by_id("AWSEDRFGYHUJUG23151"))

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

		self.assertEqual(ps.get_user_by_id('SomeUserid1234guis').email(), usr.email())

	###########################################################################
	## \brief 	Tests getting nonexistant user by key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_user_get_user_by_key_fail(self):
		fakeKey = ndb.Key("doesntExist","noReally")

		self.assertIsNone(ps.get_user_by_key(fakeKey))

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

		self.assertEqual(ps.get_user_by_key(key).email(), usr.email())
	
	###########################################################################
	## \brief 	Tests adding a new file to table
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_add_file(self):
		ret = ps.add_file("testFileaf",ndb.Key("someKey","af"))

		self.assertTrue(isinstance(ret, ndb.Key))

	###########################################################################
	## \brief 	Tests removing a file by key from table success case
	## \note 	depenends on functioning add_file function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_remove_file_by_key_success(self):
		key = ps.add_file("testFilerfks",ndb.Key("someKey","rfks"))

		self.assertTrue(ps.remove_file_by_key(key))

	###########################################################################
	## \brief 	Tests renaming a file by key success case
	## \note 	depends on functioning add_file,get_file_by_key function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_rename_file_by_key_success(self):
		key = ps.add_file("testFilernfks",ndb.Key("someKey","rnfks"))

		self.assertTrue(ps.rename_file_by_key(key,"testFilernfks2"))

		fileobj = ps.get_file_by_key(key)

		self.assertEqual(fileobj.file_name,"testFilernfks2")

	###########################################################################
	## \brief 	Tests getting existing file by key
	## \note 	depends on functioning add_file function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_get_file_by_key_success(self):
		key = ps.add_file("testFilegfks",ndb.Key("someKey","gfks"))
		fileobj = ps.get_file_by_key(key)

		self.assertEqual(fileobj.file_name,"testFilegfks")

	###########################################################################
	## \brief 	Tests getting non existing file by name
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_get_file_by_name_failure(self):
		self.assertIsNone(ps.get_file_by_name("testFilethatDoesntExist"))

	###########################################################################
	## \brief 	Tests getting existing file by name
	## \note 	depends on functioning add_file function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_get_file_by_name_success(self):
		ps.add_file("testFilegfns",ndb.Key("someKey","gfns"))
		fileobj = ps.get_file_by_name("testFilegfns")

		self.assertEqual(fileobj.owner_key,ndb.Key("someKey","gfns" ))

	###########################################################################
	## \brief 	Tests getting existing files by owner_key
	## \note 	depends on functioning add_file function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_get_files_by_owner_key_sucess(self):
		ps.add_file("testFile1",ndb.Key("someKey","gfuks"))
		ps.add_file("testFile2",ndb.Key("someKey","gfuks"))
		ps.add_file("testFile3",ndb.Key("someKey","gfuks"))
		ps.add_file("testFile4",ndb.Key("someKey","gfuks"))
		
		iterate = ps.get_file_by_owner_key(ndb.Key("someKey","gfuks"))

		for fileobj in iterate:
			self.assertEqual(fileobj.owner_key, ndb.Key("someKey","gfuks"))

	###########################################################################
	## \brief 	
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_add_file_permissions(self):

		permission = Permissions(True,True,False)
		ret = ps.add_file_permissions(ndb.Key("fk","afp"),ndb.Key("uk","afp"),permission)

		self.assertTrue(isinstance(ret, ndb.Key))

	def test_permissions_modify_file_permissions_by_key(self):
		permission = Permissions(True,True,True)
		key = ps.add_file_permissions(ndb.Key("fk","mfpk"),ndb.Key("uk","mfpk"),permission)

		new_permissions = Permissions(False,False,False)
		ps.modify_file_permissions_by_key(key, new_permissions)
		retrieved = get_permissions_by_key(key)

		self.assertEqual(new_permissions.read, retrieved.read)
		self.assertEqual(new_permissions.write, retrieved.write)
		self.assertEqual(new_permissions.full_control, retrieved.full_control)

	def test_permissions_modify_file_permissions_by_keys(self):
		permission = Permissions(True,True,True)
		ret = ps.add_file_permissions(ndb.Key("fk","mfpks"),ndb.Key("uk","mfpks"),permission)

		new_permissions =  Permissions(False,False,False)

		ps.modify_file_permissions_by_keys(ndb.Key("fk","mfpks"),ndb.Key("uk","mfpks"), new_permissions)
		retrieved = get_permissions_by_key(key)

		self.assertEqual(new_permissions.read, retrieved.read)
		self.assertEqual(new_permissions.write, retrieved.write)
		self.assertEqual(new_permissions.full_control, retrieved.full_control)

	def test_permissions_revoke_all_by_file_key(self):
		pass