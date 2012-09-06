from django.conf import settings
from django.shortcuts import render


def home(request):
    return render(request, 'chat/home.html', {
        'socket_port': settings.SOCKJS_PORT,
        'socket_channel': settings.SOCKJS_CHANNEL
    })
