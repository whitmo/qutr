from StringIO import StringIO
from retools import global_connection as cxn
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
import json


class JobNamespace(BaseNamespace):
    job_key = "qutr:job:{job_id}"
    sub_key = 'qutr:job:{0}'

    def handle_data(self, data):
        data = json.loads(data)
        if 'event' in data:
            return self.emit(data.pop('event'), data)
        return self.emit("update", data)

    def listener(self, job_id):
        r = cxn.redis.pubsub()
        chan = self.sub_key.format(job_id)
        r.subscribe(chan)
        for m in r.listen():
            if m['type'] == 'message':
                data = m['data']
                if data.startswith("{"): #@@ why deserialize?
                    self.handle_data(data)
                elif data:
                    self.emit("lineOut", data) 

    def on_subscribe(self, data):
        self.job_id = data['job_id']
        self.jobkey = self.job_key.format(job_id=self.job_id)
        self.spawn(self.listener, self.job_id)

    # def on_chat(self, job_id, msg):
    #     r = cxn.redis
    #     assert job_id
    #     r.lpush(self.jobkey, msg)

    #     # we got a new chat event from the client, send it out to
    #     # all the listeners
    #     r.publish('out', dumps(chat.serialize()))

jns = JobNamespace


## class IndexNamespace(BaseNamespace):
##     def on_subscribe(self, data):
##         self.job_id = data['job_id']
##         self.jobkey = self.job_key.format(job_id=self.job_id)
##         self.spawn(self.listener, self.job_id)


def socketio_service(request):
    retval = socketio_manage(request.environ,
                             {'/jobs': JobNamespace}, 
                             request=request)
    return retval


class JobIO(StringIO):
    """
    A stream-like object that write output to a redis pub channel and
    a list.
    """
    list_key = jns.job_key
    pub_key = jns.sub_key

    def __init__(self, uid, publish):
        self.publish = publish

    def flush(self):
        pass
    
    def write(self, line):
        line = line.strip() # remove trailing newlines
        if line:
            self.publish(line)

    def close(self):
        pass

    def __repr__(self):
        #@@ test
        return "<JobIO(log[{0}],sub[{1}])>".format(self.lkey, self.skey)


def includeme(config):
    name = 'socket_io'
    config.add_route(name, 'socket.io/*remaining')
    config.add_view(socketio_service, route_name=name)





