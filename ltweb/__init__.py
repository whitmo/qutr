from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_renderer('.html', renderer_factory)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=360)
    config.add_route('home', '/')
    config.add_route('job_log', '/api/jobs/{job_id}')
    config.add_route('job_stream', '/{job_id}')
    config.scan()
    config.include('ltweb.io')
    return config.make_wsgi_app()

