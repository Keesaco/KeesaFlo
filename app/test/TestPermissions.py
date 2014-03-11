import unittest

from Permissions.Types import *

class TestPermissions(unittest.TestCase):

	def test_group_init_none(self):
		new_group = Group()
		self.assertTrue(new_group.group_name is None)

	def test_group_init_name(self):
		new_group = Group("SomeString")
		self.assertEqual(new_group.group_name, "SomeString")