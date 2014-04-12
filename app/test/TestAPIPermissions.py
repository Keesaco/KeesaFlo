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
from Permissions.Types import Permissions, FileInfo

###########################################################################
## \brief 	Testing for Permissions table PAL
## \author 	cwike@Keesaco.com of Keesaco
###########################################################################
class TestAPIPermissions(unittest.TestCase):

	###########################################################################
	## \brief 	setup method for testing
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
	## \brief 	Tests getting user key by id
	## \note 	depends on functioning add_user function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
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
		ret = ps.add_file( FileInfo("testFileaf",ndb.Key("someKey","af") ) )

		self.assertTrue(isinstance(ret, ndb.Key))

	###########################################################################
	## \brief 	Tests removing a file by key from table success case
	## \note 	depenends on functioning add_file function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_remove_file_by_key_success(self):
		key = ps.add_file( FileInfo("testFilerfks",ndb.Key("someKey","rfks") ) )

		self.assertTrue(ps.remove_file_by_key(key))

	###########################################################################
	## \brief 	Tests renaming a file by key success case
	## \note 	depends on functioning add_file,get_file_by_key function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_rename_file_by_key_success(self):
		key = ps.add_file( FileInfo("testFilernfks",ndb.Key("someKey","rnfks") ) )

		self.assertTrue(ps.rename_file_by_key(key,"testFilernfks2"))

		fileobj = ps.get_file_by_key(key)

		self.assertEqual(fileobj.file_name,"testFilernfks2")

	###########################################################################
	## \brief 	Tests getting existing file by key
	## \note 	depends on functioning add_file function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_get_file_by_key_success(self):
		key = ps.add_file( FileInfo( "testFilegfks",ndb.Key("someKey","gfks") ) )
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
		ps.add_file( FileInfo("testFilegfns",ndb.Key("someKey","gfns") ) )
		fileobj = ps.get_file_by_name("testFilegfns")

		self.assertEqual(fileobj.owner_key,ndb.Key("someKey","gfns" ))

	###########################################################################
	## \brief 	Tests getting existing files by owner_key
	## \note 	depends on functioning add_file function
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_file_get_files_by_owner_key_sucess(self):
		ps.add_file( FileInfo("testFile1",ndb.Key("someKey","gfuks") ) )
		ps.add_file( FileInfo("testFile2",ndb.Key("someKey","gfuks") ) )
		ps.add_file( FileInfo("testFile3",ndb.Key("someKey","gfuks") ) )
		ps.add_file( FileInfo("testFile4",ndb.Key("someKey","gfuks") ) )
		
		iterate = ps.get_file_by_owner_key(ndb.Key("someKey","gfuks"))

		for fileobj in iterate:
			self.assertEqual(fileobj.owner_key, ndb.Key("someKey","gfuks"))

	###########################################################################
	## \brief 	Tests adding a file permission
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_add_file_permissions(self):

		permission = Permissions(True,True,False)
		ret = ps.add_file_permissions(ndb.Key("fk","afp"),ndb.Key("uk","afp"),permission)

		self.assertTrue(isinstance(ret, ndb.Key))

	###########################################################################
	## \brief 	Tests modifying a file permission using key
	## \note 	depends on add_file_permissions, get_permissions_by_key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_modify_file_permissions_by_key(self):
		permission = Permissions(True,True,True)
		key = ps.add_file_permissions(ndb.Key("fk","mfpk"),ndb.Key("uk","mfpk"),permission)

		new_permissions = Permissions(False,False,False)
		ps.modify_file_permissions_by_key(key, new_permissions)
		retrieved = ps.get_permissions_by_key(key)

		self.assertEqual(new_permissions.read, retrieved.read)
		self.assertEqual(new_permissions.write, retrieved.write)
		self.assertEqual(new_permissions.full_control, retrieved.full_control)

	###########################################################################
	## \brief 	Tests modifying a file permission by file key and user key
	## \note 	depends add_file_permissions, get_permissions_by_key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_modify_file_permissions_by_keys(self):
		permission = Permissions(True,True,True)
		key = ps.add_file_permissions(ndb.Key("fk","mfpks"),ndb.Key("uk","mfpks"),permission)

		new_permissions = Permissions(False,False,False)

		ps.modify_file_permissions_by_keys(ndb.Key("fk","mfpks"),ndb.Key("uk","mfpks"), new_permissions)
		retrieved = ps.get_permissions_by_key(key)

		self.assertEqual(new_permissions.read, retrieved.read)
		self.assertEqual(new_permissions.write, retrieved.write)
		self.assertEqual(new_permissions.full_control, retrieved.full_control)

	###########################################################################
	## \brief 	Tests revoking all permissions attached to a file
	## \note 	depends add_file_permissions, get_permissions_by_key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_revoke_all_by_file_key(self):
		fk = ndb.Key("fk","rafk")
		ps.add_file_permissions(fk,ndb.Key("uk","rafk1"),Permissions(True,True,True))
		ps.add_file_permissions(fk,ndb.Key("uk","rafk2"),Permissions(True,True,True))
		ps.add_file_permissions(fk,ndb.Key("uk","rafk3"),Permissions(True,True,True))

		ps.revoke_all_by_file_key(fk)
		with self.assertRaises(StopIteration):
			ps.get_file_permissions_list(fk).next()

	###########################################################################
	## \brief 	Tests revoking all permissions attached to a user
	## \note 	depends add_file_permissions, get_user_permissions_list
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_revoke_all_by_user_key(self):
		uk = ndb.Key("uk","rauk")
		ps.add_file_permissions(ndb.Key("fk","rauk1"),uk,Permissions(True,True,True))
		ps.add_file_permissions(ndb.Key("fk","rauk1"),uk,Permissions(True,True,True))
		ps.add_file_permissions(ndb.Key("fk","rauk1"),uk,Permissions(True,True,True))

		ps.revoke_all_by_user_key(uk)
		with self.assertRaises(StopIteration):
			ps.get_user_permissions_list(uk).next()

	###########################################################################
	## \brief 	Tests revoking a permission by key
	## \note 	depends add_file_permissions, get_permissions_by_key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_revoke_permissions_by_key(self):
		key = ps.add_file_permissions(ndb.Key("fk","rpbk"),ndb.Key("uk","rpbk"),Permissions(True,True,True))
		ps.revoke_permissions_by_key(key)

		self.assertIsNone(ps.get_permissions_by_key(key))

	###########################################################################
	## \brief 	Tests revoking permission based on user and file
	## \note 	depends add_file_permissions, get_user_file_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_revoke_user_file_permissions(self):
		user_key = ndb.Key("uk","rufp")
		file_key = ndb.Key("fk","rufp")
		ps.add_file_permissions(file_key,user_key,Permissions(True,True,True))
		ps.revoke_user_file_permissions(file_key,user_key)
		self.assertIsNone(ps.get_user_file_permissions(file_key,user_key))


	###########################################################################
	## \brief 	Tests getting a permission by user and file
	## \note 	depends add_file_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
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

	###########################################################################
	## \brief 	Tests getting permissions by key
	## \note 	depends add_file_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
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


	###########################################################################
	## \brief 	Tests getting permissions key by user file
	## \note 	depends add_file_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_get_user_file_permissions_key(self):
		user_key = ndb.Key("uk","gpbk")
		file_key = ndb.Key("fk","gpbk")
		perms = Permissions(True,True,True)
		key = ps.add_file_permissions(file_key,user_key,perms)
		self.assertEqual(key,ps.get_user_file_permissions_key(file_key,user_key))

	###########################################################################
	## \brief 	Tests getting all permissions attached to a file
	## \note 	depends add_file_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_get_file_permissions_list(self):
		fk = ndb.Key("fk","gfpl")
		ps.add_file_permissions(fk,ndb.Key("uk","gfpl1"),Permissions(True,True,True))
		ps.add_file_permissions(fk,ndb.Key("uk","gfpl2"),Permissions(True,True,True))
		ps.add_file_permissions(fk,ndb.Key("uk","gfpl3"),Permissions(True,True,True))

		permissions = ps.get_file_permissions_list(fk)

		for permission in permissions:
			self.assertEqual(permission.file_key, fk)

	###########################################################################
	## \brief 	Tests getting all permissions attached to a user
	## \note 	depends add_file_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_permissions_get_user_permissions_list(self):
		uk = ndb.Key("uk","gupl")
		ps.add_file_permissions(ndb.Key("fk","gupl1"),uk,Permissions(True,True,True))
		ps.add_file_permissions(ndb.Key("fk","gupl2"),uk,Permissions(True,True,True))
		ps.add_file_permissions(ndb.Key("fk","gupl3"),uk,Permissions(True,True,True))

		permissions = ps.get_file_permissions_list(uk)

		for permission in permissions:
			self.assertEqual(permission.user_key, uk)

	###########################################################################
	## \brief 	Tests adding a named element
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_element_add_element(self):
		ret = ps.add_element( "someRefae" )

		self.assertTrue(isinstance(ret, ndb.Key))

	###########################################################################
	## \brief 	Tests removing an element by reference
	## \note 	depends add_element
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_element_remove_element_by_ref(self):
		ps.add_element("someRefRebr")

		self.assertTrue(ps.remove_element_by_ref("someRefRebr"))

	###########################################################################
	## \brief 	Tests removing an element by key
	## \note 	depends add_element
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_element_remove_element_by_key(self):
		key = ps.add_element("someRefRebk")

		self.assertTrue(ps.remove_element_by_key(key))

	###########################################################################
	## \brief 	Tests renaming element
	## \note 	depends add_element, get_element_by_key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_element_rename_element(self):
		key = ps.add_element("someRefRe")
		ps.rename_element("someRefRe","someNewRefRe")

		self.assertEqual(ps.get_element_by_key(key).element_ref, "someNewRefRe")

	###########################################################################
	## \brief 	Tests getting an element by key
	## \note 	depends add_element
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_element_get_element_by_key(self):
		key = ps.add_element("someRefGebk")

		self.assertEqual(ps.get_element_by_key(key).element_ref,"someRefGebk" )

	###########################################################################
	## \brief 	Tests getting an element by reference
	## \note 	depends add_element
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_element_get_element_key_by_ref(self):
		key = ps.add_element("someRefGekbr")

		self.assertEqual(ps.get_element_key_by_ref("someRefGekbr"),key )

	###########################################################################
	## \brief 	Tests adding element permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_add_element_permissions(self):
		ret = ps.add_element_permissions(ndb.Key("uk","aep"),ndb.Key("ek","aep"),True)

		self.assertTrue(isinstance(ret, ndb.Key))

	###########################################################################
	## \brief 	Tests modifying element permissions by key
	## \note 	depends add_element_permissions, get_element_permissions_by_key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_modify_element_permissions_by_key(self):
		key = ps.add_element_permissions(ndb.Key("uk","mepk"),ndb.Key("ek","mepk"),True)

		ps.modify_element_permissions_by_key(key, False)
		retrieved = ps.get_element_permissions_by_key(key)

		self.assertFalse(retrieved.access)

	###########################################################################
	## \brief 	Tests modifying element permissions by both element and user keys
	## \note 	depends add_elelemt_permissions, get_element_permissions_by_key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_modify_user_element_permissions(self):
		key = ps.add_element_permissions(ndb.Key("uk","muep"),ndb.Key("ek","muep"),True)

		ps.modify_user_element_permissions(ndb.Key("uk","muep"),ndb.Key("ek","muep"), False)
		retrieved = ps.get_element_permissions_by_key(key)

		self.assertFalse(retrieved.access)

	###########################################################################
	## \brief 	Tests revokeing all element permissions by element key
	## \note 	depends add_element_permissions, get_element_permissions_by_element_key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_revoke_element_permissions_element_key(self):
		ek = ndb.Key("ek","repek")
		ps.add_element_permissions(ndb.Key("uk","repek1"),ek,True)
		ps.add_element_permissions(ndb.Key("uk","repek2"),ek,True)
		ps.add_element_permissions(ndb.Key("uk","repek3"),ek,True)

		ps.revoke_element_permissions_element_key(ek)
		with self.assertRaises(StopIteration):
			ps.get_element_permissions_by_element_key(ek).next()

	###########################################################################
	## \brief 	Tests revokeing element permissions by user key
	## \note 	depends add_element_permissions, get_element_permissions_by_user_key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_revoke_element_permissions_user_key(self):
		uk = ndb.Key("uk","repuk")
		ps.add_element_permissions(uk,ndb.Key("ek","repuk1"),True)
		ps.add_element_permissions(uk,ndb.Key("ek","repuk1"),True)
		ps.add_element_permissions(uk,ndb.Key("ek","repuk1"),True)

		ps.revoke_element_permissions_user_key(uk)
		with self.assertRaises(StopIteration):
			ps.get_element_permissions_by_user_key(uk).next()

	###########################################################################
	## \brief 	Tests revoking an element permissions by user and element keys
	## \note 	depends add_element_permissions, get_user_element_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_revoke_user_element_permissions(self):
		user_key = ndb.Key("uk","ruep")
		element_key = ndb.Key("ek","ruep")
		ps.add_element_permissions(user_key,element_key,True)
		ps.revoke_user_element_permissions(user_key,element_key)
		self.assertIsNone(ps.get_user_element_permissions(user_key,element_key))

	###########################################################################
	## \brief 	Tests revoking an element permission by its key
	## \note 	depends add_element_permissions, get_element_permissions_by_key
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_revoke_element_permissions_by_key(self):
		key = ps.add_element_permissions(ndb.Key("uk","repk"),ndb.Key("ek","repk"),True)
		ps.revoke_element_permissions_by_key(key)
		self.assertIsNone(ps.get_element_permissions_by_key(key))

	###########################################################################
	## \brief 	Tests getting an element permissions list by element key
	## \note 	depends add_element_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_get_element_permissions_by_element_key(self):
		ek = ndb.Key("ek","gepek")
		ps.add_element_permissions(ndb.Key("uk","gepek1"),ek,True)
		ps.add_element_permissions(ndb.Key("uk","gepek2"),ek,True)
		ps.add_element_permissions(ndb.Key("uk","gepek3"),ek,True)

		elements = ps.get_element_permissions_by_element_key(ek)

		for element in elements:
			self.assertEqual(element.element_key, ek)

	###########################################################################
	## \brief 	Tests getting an elements permissions list by user key
	## \note 	depends add_element_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_get_element_permissions_by_user_key(self):
		uk = ndb.Key("uk","gepuk")
		ps.add_element_permissions(uk,ndb.Key("ek","gepuk1"),True)
		ps.add_element_permissions(uk,ndb.Key("ek","gepuk2"),True)
		ps.add_element_permissions(uk,ndb.Key("ek","gepuk3"),True)

		elements = ps.get_element_permissions_by_user_key(uk)

		for element in elements:
			self.assertEqual(element.user_key, uk)

	###########################################################################
	## \brief 	Tests getting an entry by user and element keys
	## \note 	depends add_element_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_get_user_element_permissions(self):
		user_key = ndb.Key("uk","guep")
		element_key = ndb.Key("ek","guep")
		ps.add_element_permissions(user_key,element_key,True)

		obj = ps.get_user_element_permissions(user_key,element_key)

		self.assertEqual(obj.user_key, user_key)
		self.assertEqual(obj.element_key, element_key)
		self.assertEqual(obj.access, True)

	###########################################################################
	## \brief 	Tests getting element permissions entry by key
	## \note 	depends add_element_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_get_element_permissions_by_key(self):
		user_key = ndb.Key("uk","gepk")
		element_key = ndb.Key("ek","gepk")
		key = ps.add_element_permissions(user_key,element_key,True)

		obj = ps.get_element_permissions_by_key(key)

		self.assertEqual(obj.user_key, user_key)
		self.assertEqual(obj.element_key, element_key)
		self.assertEqual(obj.access, True)

	###########################################################################
	## \brief 	Tests getting key to element permissions entry by user and element keys
	## \note 	depends add_element_permissions
	## \author 	cwike@Keesaco.com of Keesaco
	###########################################################################
	def test_e_permissions_get_user_element_permissions_key(self):
		user_key = ndb.Key("uk","guepk")
		element_key = ndb.Key("ek","guepk")
		key = ps.add_element_permissions(user_key,element_key,True)
		self.assertEqual(key,ps.get_user_element_permissions_key(user_key,element_key))
