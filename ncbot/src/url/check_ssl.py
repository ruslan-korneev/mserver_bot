import json
from datetime import datetime
from urllib.request import socket, ssl


def valid_ssl(dt_url):
    validation = []
    now = datetime.now()

    for dt in dt_url:
        if now > dt:
            validation.append('invalid from {}'.format(dt))
        else:
            validation.append('valid until {}'.format(dt))
    return validation


def check_ssl_cirt(urls):
    port = '443'
    dt = []

    context = ssl.create_default_context()
    for url in urls:
        with socket.create_connection((url['url'], port)) as sock:
            with context.wrap_socket(sock, server_hostname=url['url']) as ssock:
                data = json.dumps(ssock.getpeercert())
                data_2 = json.loads(data)
                data_2 = data_2['notAfter']
                dt.append(datetime.strptime(data_2, '%b %d %H:%M:%S %Y GMT'))
    validation = valid_ssl(dt)

    return validation
