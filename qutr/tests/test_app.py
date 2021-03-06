from pyramid import testing
import unittest


class AppTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    dummy_settings = {'qutr.worker':'false',
                      'qutr.tasks':'qutr.tests.dummytasks'}
    def test_appcreation(self):
        from qutr import app
        wsgiapp = app.main({}, **self.dummy_settings)
        assert hasattr(wsgiapp.registry, 'tasks')
        assert hasattr(wsgiapp.registry, 'qm')

