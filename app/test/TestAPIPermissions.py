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
	APP_ID = '_'
	def setUp(self):
		# First, create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		self.testbed.setup_env(app_id=self.APP_ID)
		# Then activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Next, declare which service stubs you want to use.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		self.conn = ndb.model.make_connection()

	###########################################################################
	## \brief 	Teardown method for testing
	## \note	placeholder
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def tearDown(self):
		self.testbed.deactivate()

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

	def test_user_remove_user(self):
		pass

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
	#@unittest.skip("Manually tested to work")
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
	
	def test_user_get_user_key_by_id(self):
		usr = User('somebody@somewhereguki.com')
		usr.set_nickname('Somebodyguki')
		usr.set_user_id('SomeUserid1234guki')
		key = ps.add_user(usr)

		self.assertEqual(key,ps.get_user_key_by_id("SomeUserid1234guki"))

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
		retrieved = ps.get_permissions_by_key(key)

		self.assertEqual(new_permissions.read, retrieved.read)
		self.assertEqual(new_permissions.write, retrieved.write)
		self.assertEqual(new_permissions.full_control, retrieved.full_control)

	def test_permissions_modify_file_permissions_by_keys(self):
		permission = Permissions(True,True,True)
		key = ps.add_file_permissions(ndb.Key("fk","mfpks"),ndb.Key("uk","mfpks"),permission)

		new_permissions = Permissions(False,False,False)

		ps.modify_file_permissions_by_keys(ndb.Key("fk","mfpks"),ndb.Key("uk","mfpks"), new_permissions)
		retrieved = ps.get_permissions_by_key(key)

		self.assertEqual(new_permissions.read, retrieved.read)
		self.assertEqual(new_permissions.write, retrieved.write)
		self.assertEqual(new_permissions.full_control, retrieved.full_control)

	def test_permissions_revoke_all_by_file_key(self):
		fk = ndb.Key("fk","rafk")
		ps.add_file_permissions(fk,ndb.Key("uk","rafk1"),Permissions(True,True,True))
		ps.add_file_permissions(fk,ndb.Key("uk","rafk2"),Permissions(True,True,True))
		ps.add_file_permissions(fk,ndb.Key("uk","rafk3"),Permissions(True,True,True))

		ps.revoke_all_by_file_key(fk)
		with self.assertRaises(StopIteration):
			ps.get_file_permissions_list(fk).next()


	def test_permissions_revoke_all_by_user_key(self):
		uk = ndb.Key("uk","rauk")
		ps.add_file_permissions(ndb.Key("fk","rauk1"),uk,Permissions(True,True,True))
		ps.add_file_permissions(ndb.Key("fk","rauk1"),uk,Permissions(True,True,True))
		ps.add_file_permissions(ndb.Key("fk","rauk1"),uk,Permissions(True,True,True))

		ps.revoke_all_by_user_key(uk)
		with self.assertRaises(StopIteration):
			ps.get_user_permissions_list(uk).next()

	def test_permissions_revoke_permissions_by_key(self):
		key = ps.add_file_permissions(ndb.Key("fk","rpbk"),ndb.Key("uk","rpbk"),Permissions(True,True,True))
		ps.revoke_permissions_by_key(key)

		self.assertIsNone(ps.get_permissions_by_key(key))

	def test_permissions_revoke_user_file_permissions(self):
		user_key = ndb.Key("uk","rufp")
		file_key = ndb.Key("fk","rufp")
		ps.add_file_permissions(file_key,user_key,Permissions(True,True,True))
		ps.revoke_user_file_permissions(file_key,user_key)
		self.assertIsNone(ps.get_user_file_permissions(file_key,user_key))

	def test_permissions_get_user_file_permissions(self):
		user_key = ndb.Key("uk","gufp")
		file_key = ndb.Key("fk","gufp")
		perms = Permissions(True,True,True)
		ps.add_file_permissions(file_key,user_key,perms)

		obj = ps.get_user_file_permissions(file_key,user_key)

		self.assertEqual(obj.user_key, user_key)
		self.assertEqual(obj.file_key, file_key)
		self.assertEqual(obj.read, perms.read)
		self.assertEqual(obj.write, perms.write)
		self.assertEqual(obj.full_control, perms.full_control)

	def test_permissions_get_permissions_by_key(self):
		user_key = ndb.Key("uk","gpbk")
		file_key = ndb.Key("fk","gpbk")
		perms = Permissions(True,True,True)
		key = ps.add_file_permissions(file_key,user_key,perms)

		obj = ps.get_permissions_by_key(key)
		self.assertEqual(obj.user_key, user_key)
		self.assertEqual(obj.file_key, file_key)
		self.assertEqual(obj.read, perms.read)
		self.assertEqual(obj.write, perms.write)
		self.assertEqual(obj.full_control, perms.full_control)

	def test_permissions_get_user_file_permissions_key(self):
		user_key = ndb.Key("uk","gpbk")
		file_key = ndb.Key("fk","gpbk")
		perms = Permissions(True,True,True)
		key = ps.add_file_permissions(file_key,user_key,perms)
		self.assertEqual(key,ps.get_user_file_permissions_key(file_key,user_key))

	def test_permissions_get_file_permissions_list(self):
		fk = ndb.Key("fk","gfpl")
		ps.add_file_permissions(fk,ndb.Key("uk","gfpl1"),Permissions(True,True,True))
		ps.add_file_permissions(fk,ndb.Key("uk","gfpl2"),Permissions(True,True,True))
		ps.add_file_permissions(fk,ndb.Key("uk","gfpl3"),Permissions(True,True,True))

		permissions = ps.get_file_permissions_list(fk)

		for permission in permissions:
			self.assertEqual(permission.file_key, fk)


	def test_permissions_get_user_permissions_list(self):
		uk = ndb.Key("uk","gupl")
		ps.add_file_permissions(ndb.Key("fk","gupl1"),uk,Permissions(True,True,True))
		ps.add_file_permissions(ndb.Key("fk","gupl2"),uk,Permissions(True,True,True))
		ps.add_file_permissions(ndb.Key("fk","gupl3"),uk,Permissions(True,True,True))

		permissions = ps.get_file_permissions_list(uk)

		for permission in permissions:
			self.assertEqual(permission.user_key, uk)