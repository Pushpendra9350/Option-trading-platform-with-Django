from django.urls import path
from .consumers import *

ws_urlpatterns = [
    # paht('url address', 'Handlers') in django handlers are called views but in django channels they are called consumers
    path('ws/tick/',AsyncAOCosumer.as_asgi())
]