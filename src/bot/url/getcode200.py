from urllib.error import HTTPError, URLError
from urllib.request import socket

import requests
from requests.exceptions import ConnectionError, SSLError


def check_80(url):
    returned_message = ''
    url = check_http(url)
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        if response.status_code == 200 and response.history == []:
            returned_message = 'True'
        elif response.status_code == 200 and response.history != []:
            returned_message = 'True with Redirects'
        elif response.status_code == 301 or response.status_code == 302:
            returned_message = str(response.status_code)
        else:
            returned_message = 'False ' + str(response.status_code)

    except socket.timeout:
        returned_message = 'timed out'
    except URLError:
        returned_message = 'False URLError'
    except HTTPError:
        returned_message = 'False HTTPError'
    except UnicodeError:
        returned_message = 'UnicodeError'
    except (SSLError, ConnectionError):
        returned_message = 'SSL and Connection Error'
    if returned_message == '':
        return 'empty'
    else:
        return returned_message


def check_443(url):
    returned_message = ''
    url = check_http_s(url)
    try:
        response = requests.get(url, allow_redirects=True, timeout=5)
        if response.status_code == 200 and response.history == []:
            returned_message = 'True'
        elif response.status_code == 200 and response.history != []:
            returned_message = 'True with Redirects'
        elif response.status_code == 301 or response.status_code == 302:
            returned_message = str(response.status_code)
        else:
            returned_message = 'False ' + str(response.status_code)
    except socket.timeout:
        returned_message = 'timed out'
    except URLError:
        returned_message = 'False URLError'
    except HTTPError:
        returned_message = 'False HTTPError'
    except UnicodeError:
        returned_message = 'UnicodeError'
    except (SSLError, ConnectionError):
        returned_message = 'SSL and Connection Error'
    if returned_message == '':
        return 'empty'
    else:
        return returned_message


def check_http(url):
    if not('http://' in url) and not('https://' in url):
        url = 'http://' + url
    return url


def check_http_s(url):
    if not('https://' in url) and not('http://' in url):
        url = 'https://' + url
    return url
