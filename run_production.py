from waitress import serve
from app import app
import socket

from logger import logger

"""
Run OnSite Presence Monitor in Production Mode
==============================================

Author: Tom Erik Harnes
Created: 2025-06
Version: 1.1.1

Starts the OnSite Presence Monitor using the Waitress WSGI server for
production-ready deployment.

This script should be used instead of app.py in all real deployments,
as it ensures a stable, multi-threaded server environment.

The app must be accessible on the same network for connected kiosks or
display clients to show real-time presence data via web browser.

Access:
    http://<server-ip>:8050

Note:
- Waitress is used as the WSGI server (pip install waitress)
- Configuration and ERP integration is managed by the app itself
"""


def get_lan_ip():
    """ Returns the LAN IP of the current machine. """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        logger.error(f'get_lan_ip error: {e}')
        ip_address = '127.0.0.0.1'
    finally:
        s.close()
    return ip_address


if __name__ == '__main__':
    ip = get_lan_ip()
    port = 8050
    logger.info(f'OnSite Presence Monitor running at: http://{ip}:{port}')
    serve(app.server, host='0.0.0.0', port=port)
