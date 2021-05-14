from datetime import datetime
from ssl import SSLCertVerificationError

import requests
from requests.exceptions import ConnectionError, MissingSchema, SSLError


HTTPResponse = requests.packages.urllib3.response.HTTPResponse
orig_HTTPResponse__init__ = HTTPResponse.__init__ # NOQA [N816]


def new_http_response__init(self, *args, **kwargs):
    orig_HTTPResponse__init__(self, *args, **kwargs)
    try:
        self.peer_certificate = self._connection.peer_certificate
    except AttributeError:
        pass


HTTPResponse.__init__ = new_http_response__init


HTTPAdapter = requests.adapters.HTTPAdapter
orig_HTTPAdapter_build_response = HTTPAdapter.build_response # NOQA [N816]


def new_http_adapter_build_response(self, request, resp):
    response = orig_HTTPAdapter_build_response(self, request, resp)
    try:
        response.peer_certificate = resp.peer_certificate
    except AttributeError:
        pass
    return response


HTTPAdapter.build_response = new_http_adapter_build_response

HTTPSConnection = requests.packages.urllib3.connection.HTTPSConnection
orig_HTTPSConnection_connect = HTTPSConnection.connect # NOQA [N816]


def new_https_connection_connect(self):
    orig_HTTPSConnection_connect(self)
    try:
        self.peer_certificate = self.sock.connection.get_peer_certificate()
    except AttributeError:
        pass


HTTPSConnection.connect = new_https_connection_connect


def check_ssl_cirt(urls):
    dt = []
    for url in urls:
        try:
            r = requests.get(url)\
                .peer_certificate\
                .get_notAfter()\
                .decode('utf-8')
        except MissingSchema:
            r = requests.get(f'https://{url}')\
                .peer_certificate\
                .get_notAfter()\
                .decode('utf-8')
        except (SSLError, ConnectionError, SSLCertVerificationError):
            dt.append('')
            continue
        dt.append(datetime.strptime(r[:-1], '%Y%m%d%H%M%S'))

    validation = []
    now = datetime.now()

    for d in dt:
        try:
            if now >= d:
                validation.append(f'invalid from {d}')
            else:
                validation.append(f'valid until {d}')
        except TypeError:
            validation.append('SSL or Connection Error')
    return validation
