###########################################################################
## \file 	app/test/TestAPIDatastore.py
## \brief 	Containts test cases for the Datastore API
## \author 	jmccrea@keesaco.com of Keesaco
###########################################################################
## \package app.test.TestAPIDatastore
## \brief 	Contains test cases for the Datastore API
###########################################################################

import unittest
from google.appengine.ext import testbed

import API.APIDatastore as ds

###########################################################################
## \brief 	Test class for Datastore API. Sets up testbed and deactivates
##			it when done. Contains test cases for writing, reading, listing
##			and checking the existance of files as well as some permissions
##			oriented functions.
## \author 	jmccrea@Keesaco.com of Keesaco
###########################################################################
class TestAPIDatastore(unittest.TestCase):
	
	###########################################################################
	## \brief 	Sets up the testbed for running tests on code which uses
	##			Google Cloud Platform. Sets up app identity for GCS.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def setUp(self):
		self.testbed = testbed.Testbed()
		self.testbed.activate()
		self.testbed.init_app_identity_stub()
		
	###########################################################################
	## \brief 	Deactivates the test bed to prevent interferance with
	##			subsequent tests.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def tearDown(self):
		self.testbed.deactivate()
	
	###########################################################################
	## \brief	Tests that get_container correctly returns the parent directory
	##			of a file.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def test_getcontainer_filename(self):
		self.assertEqual(ds.get_container("/dir/subdir/file.ext"), "/dir/subdir/")
	
	###########################################################################
	## \brief	Tests that get_container returns the parent directory when
	##			passed a path to its sub-directory.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def test_getcontainer_dirname(self):
		self.assertEqual(ds.get_container("/dir/subdir"), "/dir/")
	
	###########################################################################
	## \brief	Tests that the path returned by get_container is unchanged if
	##			passed the path to the root of a bucket.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def test_getcontainer_bucketroot(self):
		self.assertEqual(ds.get_container("/dir/"), "/dir/")
	
	###########################################################################
	## \brief	Tests that an empty path is returned by get_container if passed
	##			a blank path.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def test_getcontainer_empty(self):
		self.assertEqual(ds.get_container(""), "/")
	
	###########################################################################
	## \brief	Tests that an empty path is returned by get_contaier if passed
	##			an empty path.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def test_getcontainer_slash(self):
		self.assertEqual(ds.get_container("/"), "/")
	

	
	###########################################################################
	## \brief	Tests that check_exists returns false for a file known not to
	##			exist.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def test_checkexists_notExist(self):
		self.assertFalse(ds.check_exists("/some_bucket/no_file/here/file.notafile", None))
	
	###########################################################################
	## \brief	Tests that check_exists returns false when passed the path to
	##			a directory known not to exist.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def test_checkexists_notExistDir(self):
		self.assertFalse(ds.check_exists("/some_bucket/not_a_real_dir/", None))
	
	###########################################################################
	## \brief	Adds a file then checks that that file exists.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def test_addfile_checkExists(self):
		ds.add_file("/test_bucket/test_dir/test_file.ext")
		self.assertTrue(ds.check_exists("/test_bucket/test_dir/test_file.ext", None))
	
	###########################################################################
	## \brief	Tries to add the same file twice, the second attempt should
	##			fail and return false.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def test_addfile_alreadyExists(self):
		ds.add_file("/test_bucket/test_dir/test_file_2.ext");
		self.assertFalse(ds.add_file("/test_bucket/test_dir/test_file)2.ext"))
	
	###########################################################################
	## \brief	Adds a file with a known string as contents then reads the file
	##			contents to check it is the same as the original string.
	## \author 	jmccrea@Keesaco.com of Keesaco
	###########################################################################
	def test_addfile_checkCont(self):
		ds.add_file("/test_bucket/test_dir/test_file_3.ext", "testing-testing-testing", None)
		fh = ds.open("/test_bucket/test_dir/test_file_3.ext", 'r')
		self.assertEqual(fh.read(), "testing-testing-testing")

