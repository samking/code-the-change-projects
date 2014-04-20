"""Tests for handlers.py.  

See http://webapp-improved.appspot.com/guide/testing.html for the webapp2
handler testing guide.
"""

import unittest

import webapp2
import webtest

from google.appengine.ext import testbed

import server


class HandlersTest(unittest.TestCase):
    """Test cases for handlers."""

    def setUp(self):
        super(HandlersTest, self).setUp()
        self.testapp = webtest.TestApp(server.APP)
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # It's annoying to have to figure out the right stub while you're
        # writing tests, so initialize ALL the stubs!
        self.testbed.init_all_stubs()
        self.testbed.use_deterministic_high_replication_datastore()

    def tearDown(self):
        super(HandlersTest, self).tearDown()
        self.testbed.deactivate()
    
    def test_get_new_project(self):
        request = webapp2.Request.blank('/project/new')
        response = request.get_response(server.APP)
        self.assertEqual(response.status_int, 200)
        # It should have the POST link.
        self.assertIn('post', response.body)
        # It should have a field for title and description.
        self.assertIn('Title', response.body)
        self.assertIn('Description', response.body)

    def test_post_new_project(self):
        request = webapp2.Request.blank('/project/new', POST={
            'title': 'test_title', 'description': 'test_description'})
        response = request.get_response(server.APP)
        self.assertEqual(response.status_int, 200)
        # It should have the POST link.
        self.assertIn('post', response.body)
        # It should have a field for title and description.
        self.assertIn('Title', response.body)
        self.assertIn('Description', response.body)
        


if __name__ == '__main__':
    unittest.main()
