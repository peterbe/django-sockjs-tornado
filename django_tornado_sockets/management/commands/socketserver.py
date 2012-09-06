from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.importlib import import_module
from tornado import web, ioloop
from sockjs.tornado import SockJSRouter


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '--port',
            action='store',
            dest='port',
            default=getattr(settings, 'SOCKJS_PORT', 9999),
            help='What port number to run the socket server on'),
        make_option(
            '--no-keep-alive',
            action='store_true',
            dest='no_keep_alive',
            default=False,
            help='Set no_keep_alive on the connection if your server needs it')
    )

    def handle(self, **options):
        if len(settings.SOCKJS_CLASSES) > 1:
            from django.core.exceptions import ImproperlyConfigured
            raise ImproperlyConfigured(
                "Multiple connections not yet supported"
            )

        module_name, cls_name = settings.SOCKJS_CLASSES[0].rsplit('.', 1)
        module = import_module(module_name)
        cls = getattr(module, cls_name)
        channel = getattr(settings, 'SOCKJS_CHANNEL', '/echo')
        if not channel.startswith('/'):
            channel = '/%s' % channel

        router = SockJSRouter(cls, channel)
        app_settings = {
            'debug': settings.DEBUG,
        }

        PORT = int(options['port'])
        app = web.Application(router.urls, **app_settings)
        app.listen(PORT, no_keep_alive=options['no_keep_alive'])
        print "Running sock app on port", PORT, "with channel", channel
        try:
            ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            # so you don't think you errored when ^C'ing out
            pass
