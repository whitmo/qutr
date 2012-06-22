from pyramid import testing
import unittest


class AppTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    dummy_settings = {'ltweb.worker':'false',
                      'ltweb.tasks':'ltweb.tests.dummytasks'}
    def test_appcreation(self):
        from ltweb import app
        wsgiapp = app.main({}, **self.dummy_settings)
        assert hasattr(wsgiapp.registry, 'tasks')
        assert hasattr(wsgiapp.registry, 'qm')
