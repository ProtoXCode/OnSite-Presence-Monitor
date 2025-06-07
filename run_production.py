from waitress import serve
from app import app

import socket
from logger import logger


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
