import os
import django
from django.conf import settings
from django.urls import get_resolver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_api_server.settings')
django.setup()

def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, list):
        list_urls(l, acc)
    else:
        # print(l)
        if hasattr(l, 'url_patterns'):
            list_urls(l.url_patterns, acc)
        elif hasattr(l, 'pattern'):
            try:
                print(f"{l.pattern} | Name: {l.name}")
            except:
                pass
    if len(lis) > 1:
        list_urls(lis[1:], acc)

resolver = get_resolver()
list_urls(resolver.url_patterns)
