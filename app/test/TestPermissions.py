import unittest

from Permissions.Types import *

class TestPermissions(unittest.TestCase):

	def test_group_init_none(self):
		new_group = Group()
		self.assertTrue(new_group.group_name is None)

	def test_group_init_name(self):
		new_group = Group("SomeString")
		self.assertEqual(new_group.group_name, "SomeString")


class TestUser(unittest.TestCase):
	
	def test_user_init_none(self):
		new_user = User()
		self.assertTrue(new_user.username is None)
	
	def test_user_init_name(self):
		new_user = User("SomeString")
		self.assertEqual(new_user.username, "SomeString")


class TestPermissions(unittest.TestCase):
	def test_permissions_init_none(self):
		new_permissions = Permissions()
		
		self.assertFalse(new_permissions.read)
		self.assertFalse(new_permissions.write)
		self.assertFalse(new_permissions.full_control)

	def test_permissions_init_args(self):
		new_permissions = Permissions(write = True)

		self.assertTrue(new_permissions.write)
		self.assertFalse(new_permissions.read)
		self.assertFalse(new_permissions.full_control)

	def test_permissions_init_fc_force(self):
		new_permissions = Permissions(False, True, True)

		self.assertTrue(new_permissions.read)
		self.assertTrue(new_permissions.write)
		self.assertTrue(new_permissions.full_control)

	def test_permissions_set_args(self):
		new_permissions = Permissions()
		new_permissions.set_permissions(True, True)
	
		self.assertTrue(new_permissions.write)
		self.assertTrue(new_permissions.read)
		self.assertFalse(new_permissions.full_control)

	def test_permissions_set_fc_force(self):
		new_permissions = Permissions(True, False, False)
		new_permissions.set_permissions(False, True, True)
	
		self.assertTrue(new_permissions.read)
		self.assertTrue(new_permissions.write)
		self.assertTrue(new_permissions.full_control)

	def test_permissions_set_missing_args(self):
		new_permissions = Permissions(True, True, False)
		new_permissions.set_permissions(write = True)

		self.assertTrue(new_permissions.read)


class TestGroupAccess(unittest.TestCase):
	def test_groupaccess_init_args(self):
		test_group = Group("TestGroup")
		test_permissions = Permissions(True, False, False)
		new_ga = GroupAccess(test_group, test_permissions)

		self.assertEqual(new_ga.group, test_group)
		self.assertEqual(new_ga.permissions, test_permissions)


class TestUserAccess(unittest.TestCase):
	def test_useraccess_init_args(self):
		test_user = User("TestUser")
		test_permissions = Permissions(True, False, False)
		new_ua = UserAccess(test_user, test_permissions)
		
		self.assertEqual(new_ua.user, test_user)
		self.assertEqual(new_ua.permissions, test_permissions)

class TestPermissionSet(unittest.TestCase):
	def test_permissionset_init(self):
		test_user = User("someUser")
		test_ps = PermissionSet(test_user)

		self.assertEqual(test_ps.authed_user, test_user)

	def test_permissionset_adduser(self):
		test_ps = PermissionSet(User("test"))
		test_ps.add_user(User("newUser"))

		self.assertEqual(len(test_ps.users), 1)

	def test_permissionset_addgroup(self):
		test_ps = PermissionSet(User("test"))
		test_ps.add_group(Group("newGroup"))
		
		self.assertEqual(len(test_ps.groups), 1)
