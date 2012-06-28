from pyramid.config import Configurator
from pyramid.response import Response

def hello_world(request):
    if request.matchdict:
        return Response('Hello %(name)s!' % request.matchdict)
    return Response("Howdy")

config = Configurator()
config.add_route('hello', '/hello/{name}')
config.add_route('index', '/')
config.add_view(hello_world, route_name='hello')
config.add_view(hello_world, route_name='index')
application = config.make_wsgi_app()

