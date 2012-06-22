from pyramid.config import Configurator
from pyramid.decorator import reify
from pyramid.request import Request as Base
from pyramid_jinja2 import renderer_factory
from retools import queue
import gevent


class Request(Base):
    @reify
    def settings(self):
        return self.registry.settings

    @reify
    def jobns(self):
        return self.settings['ltweb.tasks'].strip()

def launch_worker(settings):
    q, interval, block = (settings['ltweb.q'], 
                          settings['ltweb.q_interval'], 
                          settings['ltweb.q_block'])
    worker = queue.Worker(queues=[q])
    block = False or block.lower() != 'false' 
    worker.work(interval=float(interval), blocking=bool(block))
    print "started worker: %s" %worker.worker_id


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_renderer('.html', renderer_factory)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=360)
    config.add_route('home', '/')
    config.add_route('tasks', '/api/tasks')
    config.add_route('jobs', '/api/jobs')
    config.add_route('job_log', '/api/jobs/{job_id}')
    config.add_route('job_stream', '/{job_id}')
    config.scan()
    config.include('ltweb.io')
    config.set_request_factory(Request)
    if settings['ltweb.worker'] != 'false':
        config.worker = gevent.spawn(launch_worker, settings)
    return config.make_wsgi_app()

