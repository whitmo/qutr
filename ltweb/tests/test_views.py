from pyramid import testing
import unittest
from mock import Mock


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_index(self):
        from ..views import hp
        request = testing.DummyRequest()
        info = hp(request)
        assert info == {}

    def test_jobs_collection_api(self):
        from ..views import jobs
        post = dict(path='ltweb.tests.dummytasks.numbers_print_out')
        request = testing.DummyRequest(post=post)
        uid = '123'
        request.enqueue = Mock(name='nq', return_value=uid)
        out = jobs(request)
        ## assert out['path'] == post['path']
        ## assert out['uid'] == uid
        ## assert request.enqueue.call_args[0][0] == post['path']

