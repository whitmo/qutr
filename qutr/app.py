from . import utils
from . import qutils
from pyramid.config import Configurator
from pyramid.decorator import reify
from pyramid.request import Request as Base
from pyramid_jinja2 import renderer_factory
import gevent
import inspect


class Request(Base):
    @reify
    def settings(self):
        return self.registry.settings

    @reify
    def tasks(self):
        return self.registry.tasks

    @reify
    def qm(self):
        return self.registry.qm
        
    def enqueue(self, job, **kw):
        func = self.qm.resolve(job)
        taskmeta = qutils.Task.is_task(func)
        if 'events' in taskmeta:
            [self.qm.subscriber(event,
                               job=job,
                               handler=spec) \
             for event, spec in taskmeta['events'].items()]
                
        return self.qm.enqueue(job, **kw)


def load_tasks_list(spec):
    taskns = utils.resolve(spec)
    assert inspect.ismodule(taskns)
    path = "%s.{0}" %taskns.__name__
    is_task = qutils.Task.is_task
    return sorted(dict(path=path.format(x), 
                       **is_task(y)) for x, y in vars(taskns).items() \
                  if not x.startswith('_') and is_task(y))
    

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_renderer('.html', renderer_factory)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static')
    config.add_route('home', '/')
    config.add_route('tasks', '/api/tasks')
    config.add_route('jobs', '/api/jobs')
    config.add_route('job', '/api/jobs/{job_id}')
    config.add_route('job_stream', '/{job_id}')
    config.scan()
    config.include('qutr.io')
    config.set_request_factory(Request)
    qutils.setup_queue_manager(config)
    if settings['qutr.worker'] != 'false':
        config.worker = gevent.spawn(qutils.launch_worker, settings)
    config.registry.tasks = load_tasks_list(settings['qutr.tasks'].strip())
    return config.make_wsgi_app()

