#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cgs_nlp.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

if __name__ == '__main__':
    from waitress import serve
    host = os.environ.get('DJANGO_HOST', '0.0.0.0')
    port = int(os.environ.get('DJANGO_PORT', 8000))
    print(f'Starting Waitress server on {host}:{port}...')
    serve(application, host=host, port=port, threads=4)
