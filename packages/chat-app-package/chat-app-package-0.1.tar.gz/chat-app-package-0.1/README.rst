=====
Chat
=====

Chat is a Django app to conduct Web-based Chat. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "chat" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'chat',
    ]

    USE_DEFAULT_TEMPLATES=False

2. Include the chat URLconf in your project urls.py like this::

    path('chat/', include('chat.urls')),

3. Run ``python manage.py migrate`` to create the chat models.

4. Add to settings.py this::

    ASGI_APPLICATION = 'your_project_name.asgi.application'

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('127.0.0.1', 6379)],
            },
        },
    }

    WEBSOCKETPATH='127.0.0.1:8000'

5. Create routing.py file in project folder::

    from django.urls import path
    from channels.routing import URLRouter
    from chat.consumers import ChatConsumer

    ws_application = [
        path("ws/chat/",ChatConsumer.as_asgi())
    ]

6. Write in asgi.py file in project folder::

    import os
    from channels.routing import URLRouter,ProtocolTypeRouter
    from channels.security.websocket import AllowedHostsOriginValidator
    from channels.auth import AuthMiddlewareStack
    from django.core.asgi import get_asgi_application
    from .routing import ws_application

    application = ProtocolTypeRouter({
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
            URLRouter(
                ws_application
            )
            )
        )
    })

7. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a chat (you'll need the Admin app enabled).

8. Visit http://127.0.0.1:8000/chat/ to participate in the chat.

9. If you want to use your template::

    write views.py
   
    from chat.use_customs import CustomTemplate

    CustomTemplate.chat_template_name='mychat.html'
    CustomTemplate.login_template_name='mylogin.html'
    CustomTemplate.signup_template_name='mysignup.html'
