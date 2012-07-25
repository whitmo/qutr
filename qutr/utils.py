from . import io
from pyramid.path import DottedNameResolver
from retools import global_connection as cxn


resolve = DottedNameResolver(None).maybe_resolve


def load_redis(**kwargs):
    if not kwargs:
        return cxn.redis
    raise NotImplementedError


def simple_route(config, name, url, fn, renderer=None):
    if not renderer:
        renderer = "qutr:templates/%s.html" % name

    config.add_route(name, url)
    config.add_view(fn, route_name=name, renderer=renderer)

















