#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UneedTest: Google App Engine Unit Test Framework
Based on GAEUnit by George Lei and Steven R. Farley.

Requirements:
  UneedTest runs only on Python 2.7 Google App Engine and uses standard libraries only.

Usage:
  1. Put uneedtest.py into your application directory.  Modify 'app.yaml' by
    adding the following mapping below the 'handlers:' section:

   - url: /_ah/unittest/.*
     script: uneedtest.app

  2. Write your own test cases by extending unittest.TestCase.

  3. Configure directories with unit tests.
    Framework can be configured for looking for tests in directory, so as
    looking for tests inside packages.

  4. Launch the development web server. To run all tests, point your browser to:
    http://localhost:8080/_ah/unittest/     (Modify the port if necessary.)

  5. The results are displayed as the tests are run.

Notes:
  1. By default all tests are running on isolated amd emulated datastore.
    This means datastore is clean when test are starting.
    If you want see how it works on real datastore, or check values written during tests,
    you should add GET parameter 'datastore' (e.g. 'http://localhost:8080/_ah/unittest/?datastore')

  2. Tests are running synchronously. I made it so because on Google servers valid
    asyncronous tests may fail. Because of infrastructure architecture not recommended
    to use setUp and tearDown functions - initialization and finalization should be
    in test function.
    If you want to run tests asynchronously add GET parameter 'async'
    (e.g. 'http://localhost:8080/_ah/unittest/?async')

------------------------------------------------------------------------------
Copyright (c) 2012, Alexey Navolotsky.  All rights reserved.
Copyright (c) 2008-2009, George Lei and Steven R. Farley.  All rights reserved.

Distributed under the following BSD license:

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
------------------------------------------------------------------------------
"""
__author__ = 'Alexey Navolotsky'
__email__ = 'alexey@navolotsky.com'
__version__ = '1.0.0'
__copyright__ = '(c) 2012, Alexey Navolotsky'
__license__ = 'New BSD License'
__url__ = "http://code.google.com/p/uneedtest/"

config = {
  'test_directories': [
      {'dir_name': 'test'}, # Run tests from all files in 'test' dir
      {'dir_name': 'smth/ext', 'submodule': 'test'}
                            # Run tests from all packages in smth.ext, containing submodule called 'test'.
  ],
  'web_dir': '/_ah/unittest'
}

from google.appengine.api import apiproxy_stub_map, datastore_file_stub, namespace_manager, users
from google.appengine.ext import webapp
import json, logging, os, sys, unittest

def app_admin(handler):
  """ Request handler wrapper.
  Forbids access for all except application administrators.
  Doesn't checks for admin rights on development server.
  """

  def wrapper(self, *args, **kwargs):
    dev_server = self.request.environ.get(
      'SERVER_SOFTWARE') and self.request.environ.get('SERVER_SOFTWARE').lower().startswith('development') or False
    demo_app = self.request.environ.get('APPLICATION_ID').lower() == 's~uneedtestdemo' or False
    if users.is_current_user_admin() or dev_server or demo_app: handler(self, *args, **kwargs)
    elif users.get_current_user(): self.error(403)
    else: self.redirect(users.create_login_url(self.request.uri))

  return wrapper


class UnitTestHandler(webapp.RequestHandler):
  """ Base class for request hanlders.
  Includes useful functions
  """

  def reload_module(self, module_name):
    """ Imports module by name.
    Module name must be absolute.
    """
    module = sys.modules.get(module_name) or __import__(module_name, globals(), locals(), ['unittest'], 0)
    if os.environ.get('SERVER_SOFTWARE').lower().startswith('development'): module = reload(module)
    return module

  def _load_modules_from_dir(self, dir_name, submodule=''):
    """ Loads test modules from specified directory.
    Also loads tests for precompiled modules (when only .pyc file is available).
    """
    modules_names = []
    if os.path.isdir(dir_name):
      prefix = dir_name.replace('/', '.')
      if submodule:
        for package_dir in os.listdir(dir_name):
          if os.path.isdir(os.path.join(dir_name, package_dir)):
            if os.path.isfile(os.path.join(dir_name, package_dir, '%s.py' % submodule)) or os.path.isfile(
              os.path.join(dir_name, package_dir, '%s.pyc' % submodule)):
              modules_names.append('%s.%s.%s' % (prefix, package_dir, submodule))
      else:
        for module_file in os.listdir(dir_name):
          if os.path.isfile(os.path.join(dir_name, module_file)):
            module_name = ''
            if module_file.endswith('.py'): module_name = '%s.%s' % (prefix, module_file[:-3])
            if module_file.endswith('.pyc'): module_name = '%s.%s' % (prefix, module_file[:-4])
            if module_name.endswith('__init__'): module_name = module_name[:-9]
            if module_name: modules_names.append(module_name)
    return [self.reload_module(name) for name in list(set(modules_names))]

  def load_default_test_modules(self):
    """ Loads test modules from config directories.
    Don't forget to put __init__.py in these directories.
    """
    modules_names = []
    for dir in config.get('test_directories'):
      modules_names.extend(self._load_modules_from_dir(dir.get('dir_name'), dir.get('submodule', '')))
    return modules_names

  def create_suite(self):
    """ Creates new test suite for all test or specified package or test """
    error = None
    package_name = self.request.get('package', '')
    test_name = self.request.get('name', '')
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    try:
      if test_name:
        self.load_default_test_modules()
        suite.addTest(loader.loadTestsFromName(test_name))
      elif package_name:
        package = self.reload_module(package_name)
        suite.addTest(loader.loadTestsFromModule(package))
      else:
        modules = self.load_default_test_modules()
        for module in modules: suite.addTest(loader.loadTestsFromModule(module))
    except Exception, e:
      error = str(e)
      logging.error(error)
    return suite, error

  def _get_tests_from_suite(self, suite):
    """ Recursively get list of all tests """
    tests = []
    for test in suite:
      if isinstance(test, unittest.TestSuite): tests.extend(self._get_tests_from_suite(test))
      else: tests.append(test)
    return tests

  def _test_suite_to_json(self, suite):
    """ Converting suite to JSON """
    #noinspection PyUnresolvedReferences
    test_tuples = [(type(test).__module__, type(test).__name__,
                    test._testMethodName) for test in self._get_tests_from_suite(suite)]
    test_dict = {}
    for test_tuple in test_tuples:
      module_name, class_name, method_name = test_tuple
      if module_name not in test_dict: test_dict[module_name] = {class_name: [method_name]}
      else:
        mod_dict = test_dict[module_name]
        if class_name not in mod_dict: mod_dict[class_name] = [method_name]
        else:
          method_list = mod_dict[class_name]
          method_list.append(method_name)
    return json.dumps(test_dict)

  def run_test_suite(self, runner, suite, real_datastore=False):
    """ Run the test suite.
    Datastore is isolated by namespace or api proxy. All other API's used as-is.
    """
    if real_datastore: # Run tests on real datastore
      namespace_manager.set_namespace('unittest')
      return runner.run(suite)
    original_apiproxy = apiproxy_stub_map.apiproxy
    try: # Run tests on isolated datastore
      apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
      temp_stub = datastore_file_stub.DatastoreFileStub('GAEUnitDataStore', None, trusted=True)
      apiproxy_stub_map.apiproxy.RegisterStub('datastore', temp_stub)
      # Allow the other services to be used as-is for tests.
      for name in ['user', 'urlfetch', 'mail', 'memcache', 'images', 'taskqueue']:
        apiproxy_stub_map.apiproxy.RegisterStub(name, original_apiproxy.GetStub(name))
      return runner.run(suite)
    finally: apiproxy_stub_map.apiproxy = original_apiproxy

  def render_main_page(self, suite, error):
    """ Render HTML for main test page. """
    rds = self.request.GET.has_key('datastore') and ' + "&amp;datastore"' or ''
    script = not error and HTML_SCRIPT % {'suite': self._test_suite_to_json(suite), 'web_dir': config.get('web_dir'),
                                          'datastore': rds} or ''
    error = error and '<div class="warning">Can\'t create test suite:<br/><br/>%s</div>' % error or ''
    self.response.write(HTML_MAINPAGE % {'style': HTML_STYLE, 'script': script, 'error': error,
                                         'web_dir': config.get('web_dir')})


class JsonTestResult(unittest.TestResult):
  """ Test result with JSON renderer. """

  def __init__(self):
    super(JsonTestResult, self).__init__()
    self.testNumber = 0

  def _list(self, list): return [{'desc': test.shortDescription() or str(test), 'detail': err} for test, err in list]

  def render(self): return json.dumps({'total': self.testNumber, 'errors': self._list(self.errors),
                                       'runs': self.testsRun, 'failures': self._list(self.failures)})


class JsonTestRunner:
  def run(self, test):
    self.result = JsonTestResult()
    self.result.testNumber = test.countTestCases()
    test(self.result)
    return self.result


class JsonTestRunHandler(UnitTestHandler):
  """ Handler for test running. """

  @app_admin
  def get(self):
    self.load_default_test_modules()
    suite = unittest.defaultTestLoader.loadTestsFromName(self.request.get('name'))
    runner = JsonTestRunner()
    self.run_test_suite(runner, suite, self.request.GET.has_key('datastore'))
    self.response.headers['Content-Type'] = 'text/javascript'
    self.response.write(runner.result.render())


class MainPageHandler(UnitTestHandler):
  """ Handler for 'browsered' test main page.
  Tests will run on real datastore (in namespace 'unittest') if GET parameter 'datastore' is defined.
  """

  @app_admin
  def get(self):
    suite, error = self.create_suite()
    self.render_main_page(suite, error)


app = webapp.WSGIApplication([
  ('%s/' % config.get('web_dir'), MainPageHandler),
  ('%s/run' % config.get('web_dir'), JsonTestRunHandler)
], debug=True)

HTML_MAINPAGE = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <style type="text/css">%(style)s</style>
    <script language="javascript" type="text/javascript">%(script)s</script>
    <title>UneedTest</title>
    <link rel="shortcut icon" href="http://appengine.google.com/favicon.ico" type="image/x-icon"/>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <!--[if IE]><meta http-equiv="X-UA-Compatible" content="IE=edge"/><![endif]-->
  </head>
  <body onload="renderPage()">
    <div id="wrapper">
      <div id="toppanel">
        <div id="links">
          <ul>
            <li><a href="%(web_dir)s/">run all tests</a></li>
            <li><a href="javascript:location.reload(true)">restart current</a></li>
            <li><a href="/_ah/admin/datastore" target="_blank">development console</a></li>
          </ul>
        </div>
        <div id="title"><h1>UneedTest</h1></div>
        <div style="clear:both"></div>
      </div>
      <div id="middle">
        <div id="container">
          <div id="results">
            <div id="testprogressbar"><div id="testindtext"></div><div id="testindicator"></div></div>
            <table border="0" cellspacing="0" cellpadding="0" id="results_table"><tr>
              <td>Runs: <span id="testran">0</span>/<span id="testtotal">0</span></td>
              <td>Errors: <span id="testerror">0</span></td>
              <td>Failures: <span id="testfailure">0</span></td>
            </tr></table>
            <div id="errorarea">%(error)s</div>
          </div>
        </div>
        <div id="sidebar">
          <h2>Tests</h2>
          <div id="testlist"></div>
        </div>
      </div>
    </div>
    <div id="footer">
      <div id="footer_right">&copy; 2012 Alexey Navolotsky</div>
      <div id="footer_left">
        <a href="http://code.google.com/p/uneedtest/" target="_blank">UneedTest</a> is based on
        <a href="http://code.google.com/p/gaeunit" target="_blank">GAEUnit</a>
        unittest framework made by George Lei and Steven R. Farley
      </div>
      <div style="clear:both"></div>
    </div>
  </body>
</html>'''

HTML_STYLE = '''
* {margin:0; padding:0}
html {height:100%}
body {height:100%; font-family:arial,sans-serif; font-size:14px; text-align:center; background-color:#eee}
h2 {font-family:Georgia,serif; font-weight:bold; font-size:16px; color:#333}
pre {white-space: pre-wrap}
#container {width:100%; float:left; overflow:hidden; text-align:center}
#errorarea {padding-top:25px; margin:0 auto}
#footer{height:38px; margin:-38px auto 0; color:#555; position: relative}
#footer_right{float:right; padding:10px}
#footer_left{float:left; padding:10px}
#links {float:right}
#links li {padding:0 10px; list-style-type:none; display:inline}
#links a {color: #fff08c; text-decoration:underline}
#links a:hover {text-decoration:none}
#middle {width:100%; padding:0 0 40px; height:1%; position:relative;}
#middle:after {content:'.'; display:block; clear:both; visibility:hidden; height:0;}
#results {margin:0 auto; padding:15px 0 0 210px; text-align:center; font-weight:bold}
#results_table {margin:0 auto; text-align:center; width:800px}
#results_table span {font-weight:bold}
#sidebar {float:left; width:200px; padding-top:15px; margin-left:-100%; position:relative;}
#title {float:left}
#title h1 {font-family:Georgia,serif; font-weight:bold; font-size:18px}
#testlist {padding:10px; text-align:left}
#testlist a {text-decoration:none}
#testlist ul {padding:0 0 0 15px;}
#testlist li {padding:1px 0}
#testindicator{height:30px; width:5px; background-color:#888}
#testindtext{position:absolute;height:27px;width:800px;margin-top:3px;font-family:Georgia,serif; font-size:18px}
#testprogressbar {width:800px; height:30px; background-color:#ddd; margin:10px auto; border:1px solid #999}
#toppanel {background-color:#777; height:20px; color:#eee; padding:10px}
#wrapper{min-height:100%;height:auto!important;height:100%;min-width:1000px;margin:0 auto}
.error {border-color: #c3d9ff; border-style: solid; border-width: 2px 1px 2px 1px; width:800px;
          padding:1px; margin:0 auto 10px; text-align:left}
.errtitle {background-color:#c3d9ff; font-weight:bold;border:1px solid #c3d9ff;font-family:Georgia,serif}
.errtitle a{font-style:italic;text-decoration:none;color:#300}
.warning{background-color:#fcc;border:1px solid red;font-weight:700;color:#300;
          text-align:center;margin:10px;padding:10px;border-radius:5px;}
'''

HTML_SCRIPT = '''
var testsToRun = %(suite)s;
var testsToRunList = new Array();
var totalRuns = 0;
var totalErrors = 0;
var totalFailures = 0;
var start = new Date();

function newXmlHttp() {
  try { return new XMLHttpRequest(); } catch(e) {}
  try { return new ActiveXObject("Msxml2.XMLHTTP"); } catch (e) {}
  try { return new ActiveXObject("Microsoft.XMLHTTP"); } catch (e) {}
  alert("XMLHttpRequest not supported");
  return null;
}

function requestTestRun(moduleName, className, methodName) {
  var methodSuffix = "";
  if (methodName) {
    methodSuffix = "." + methodName;
  }
  var xmlHttp = newXmlHttp();
  xmlHttp.open("GET", "%(web_dir)s/run?name=" + moduleName + "." + className + methodSuffix%(datastore)s, true);
  xmlHttp.onreadystatechange = function() {
    if (xmlHttp.readyState != 4) {
      return;
    }
    if (xmlHttp.status == 200) {
      var result = eval("(" + xmlHttp.responseText + ")");
      totalRuns += parseInt(result.runs);
      totalErrors += result.errors.length;
      totalFailures += result.failures.length;
      document.getElementById("testran").innerHTML = totalRuns;
      document.getElementById("testerror").innerHTML = totalErrors;
      document.getElementById("testfailure").innerHTML = totalFailures;
      if (totalErrors == 0 && totalFailures == 0) {
        testSucceed();
      } else {
        testFailed();
      }
      var errors = result.errors;
      var failures = result.failures;
      var details = "";
      for(var i=0; i<errors.length; i++) {
        details += '<p><div class="error"><div class="errtitle">ERROR <a href="%(web_dir)s/?name=' +
                   moduleName + "." + className + methodSuffix + '">' +
                   errors[i].desc +
                   '</a></div><div class="errdetail"><pre>'+errors[i].detail +
                   '</pre></div></div></p>';
      }
      for(var i=0; i<failures.length; i++) {
        details += '<p><div class="error"><div class="errtitle"> FAILURE <a href="%(web_dir)s/?name=' +
                   moduleName + "." + className + methodSuffix + '">' +
                   failures[i].desc +
                   '</a></div><div class="errdetail"><pre>' +
                   failures[i].detail +
                   '</pre></div></div></p>';
      }
      var errorArea = document.getElementById("errorarea");
      errorArea.innerHTML += details;
    } else {
      document.getElementById("errorarea").innerHTML = xmlHttp.responseText;
      testFailed();
    }
    if (window.location.search.indexOf("async") == -1) {
      var runParams = testsToRunList[totalRuns]
	  requestTestRun(runParams[0], runParams[1], runParams[2])
    }
  };
  xmlHttp.send(null);
}

function updInfoTime() {
  var end = new Date().getTime();
  var hr = start.getHours();
  var mn = start.getMinutes();
  var sc = start.getSeconds();
  if (hr < 10) {hr = '0' + hr;}
  if (mn < 10) {mn = '0' + mn;}
  if (sc < 10) {sc = '0' + sc;}
  document.getElementById("testindtext").innerHTML = hr + ':' + mn +':' + sc +
                                                       ' (' + (end - start.getTime())/1000 + 's)';
  document.getElementById("testindicator").style.width = Math.round((800* totalRuns /
                          document.getElementById("testtotal").innerHTML)) + 'px';
}

function testFailed() {
  document.getElementById("testindicator").style.backgroundColor="#fcc";
  updInfoTime();
}

function testSucceed() {
  document.getElementById("testindicator").style.backgroundColor="#aea";
  updInfoTime();
}

function runTests() {
  for (var moduleName in testsToRun) {
    var classes = testsToRun[moduleName];
    for (var className in classes) {
      methods = classes[className];
      for (var i = 0; i < methods.length; i++) {
        var methodName = methods[i];
        var runParams = new Array();
        runParams = [moduleName, className, methodName]
        testsToRunList.push(runParams)
      }
    }
  }
  document.getElementById("testtotal").innerHTML = testsToRunList.length;
  if (window.location.search.indexOf("async") > 0) {
    for (i=0;i<testsToRunList.length;i++) {
      var runParams = testsToRunList[i]
      requestTestRun(runParams[0], runParams[1], runParams[2])
    }
  } else {
     var runParams = testsToRunList[0]
	 requestTestRun(runParams[0], runParams[1], runParams[2])
  }
}

function renderPage() {
  html = '<ul>';
  for (var key in testsToRun) {
    if (testsToRun.hasOwnProperty(key)) {
      html += '<li>';
      html += '<a href="?package=' + key + '">' + key + '</a>';
      html += '<ul>'
      for (var subkey in testsToRun[key]) {
        if (testsToRun[key].hasOwnProperty(subkey)) {
          html += '<li>';
          html += '<a href="?name=' + key + '.' + subkey + '">' + subkey + '</a>';
          html += '<ul>'
          for (var test in testsToRun[key][subkey]) {
            html += '<li><a href="?name=' + key + '.' + subkey + '.' + testsToRun[key][subkey][test] + '">' +
                     testsToRun[key][subkey][test] + '</a></li>';
          }
          html += '</ul>';
          html += '</li>';
        }
      }
      html += '</ul>';
      html += '</li>';
    }
  }
  html += '</ul>';
  document.getElementById("testlist").innerHTML = html;
  runTests();
}
'''