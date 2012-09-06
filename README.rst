django-sockjs-tornado
=====================

Makes it easy to run a SockJS server in Django through Tornado.

This package is basically a thin wrapper on top of `sockjs-tornado
<https://github.com/mrjoes/sockjs-tornado>`_ which makes it dead easy
to write websocket based apps on top of the `sockjs Websocket
emulation library <http://sockjs.org/>`_.

With this wrapper you basically have access to everything else you
need from your Django project such as your models and your various
settings.

Because you need to run two processes (one for `runserver` (or `wsgi`)
and one for `socketserver`) it means that the two really are separate
python processes so you can't easily do things like registering
signals and trigger them in one process and have them fire in another.

Getting started
---------------

Create a class somewhere that looks something like this::

    from sockjs.tornado import SockJSConnection

    class MyConnection(SockJSConnection):
        def on_open(self, request):
             pass
        def on_message(self, message):
             pass
        def on_close(self):
             pass

Next, you need to put the loction of this in a setting in your
`settings.py` something like this::

    SOCKJS_CLASSES = (
        'myproject.myapp.myfile.MyConnection',
    )


Next, to start the server simply run::

    python manage.py socketserver [--help]

You'll still have your regular django server too in a separate terminal::

    python manage.py runserver

Now you should be able to write the juicy Javascript using
`sockjs-client <https://github.com/sockjs/sockjs-client>`_. You can
start by downloading the `latest minified version from the CDN
<http://cdn.sockjs.org/>`_.

A simple app might look like this::

    sock = new SockJS('http://localhost:9999/echo');
    sock.onmessage = function(e) {
      console.log(e.data);
    };
    sock.onclose = function() {
      console.log('closed :(');
    };
    sock.onopen = function() {
      console.log('opened :>');
      letTheMadnessBegin();
    };

    function letTheMadnessBegin() {
      // silly, but you get the idea
      sock.send(JSON.stringify({
        name: $('#name').text(),
        message: $('input').val()
      }));
    }

Getting fancy
-------------

There's a shitload more things you can do with this of course. For
example, you might want to add some form of authentication. Since the
`on_open` handler receives a request you can use that to ask for
`request.get_cookie()` which is left to the reader as an exercise.

There is a slightly more fancy example included in this package under
example which might get you some ideas. It's a fully working chat
application that just works.

This package is built mainly on `Serve Koval
<https://github.com/mrjoes>`_'s amazing work on `sockjs-tornado
<https://github.com/mrjoes/sockjs-tornado>`_ which has lots of more
examples and documentation that might help you. For example, it lists
to a sample HAProxy configuration which you might need once you take
your project live since you can't keep exposing port 9999 on a
production system.
