from mock import Mock
from mock import call
from mock import patch
from pyramid import testing
import unittest


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
        post = dict(path='qutr.tests.dummytasks.numbers_print_out')
        request = testing.DummyRequest(post=post)
        uid = '123'
        request.enqueue = Mock(name='nq', return_value=uid)
        with patch("retools.global_connection.redis.publish") as rpub:
            out = jobs(request)
            assert rpub.call_args == call('jobs:123', '{"state": "queued"}')
            assert out['uid'] == uid
        assert request.enqueue.call_args == call(post['path'])




