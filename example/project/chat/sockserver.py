import json
from sockjs.tornado import SockJSConnection
from .models import Message


class ChatConnection(SockJSConnection):
    _connected = set()

    def on_open(self, request):
        #print "OPEN"
        #print request.get_cookie('name')
        self._connected.add(self)
        for each in Message.objects.all().order_by('date')[:10]:
            self.send(self._package_message(each))

    def on_message(self, data):
        data = json.loads(data)
        #print "DATA", repr(data)
        msg = Message.objects.create(
            name=data['name'],
            message=data['message']
        )
        self.broadcast(self._connected, self._package_message(msg))

    def on_close(self):
        #print "CLOSE"
        self._connected.remove(self)

    def _package_message(self, m):
        return {'date': m.date.strftime('%H:%M:%S'),
                'message': m.message,
                'name': m.name}
