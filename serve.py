from socketio.server import SocketIOServer
from pyramid.paster import get_app
from gevent import monkey; monkey.patch_all()

if __name__ == '__main__':

    app = get_app('development.ini')
    port = 6543
    print 'Listening on port http://0.0.0.0:%s' %port

    SocketIOServer(('0.0.0.0', port),
                   app, resource="socket.io").serve_forever()

