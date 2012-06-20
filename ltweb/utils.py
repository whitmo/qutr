def simple_route(config, name, url, fn, renderer=None):
    if not renderer:
        renderer = "ltweb:templates/%s.html" % name

    config.add_route(name, url)
    config.add_view(fn, route_name=name, renderer=renderer)
