import hmac
import requests
from hashlib import sha1
from flask import request, json, abort, current_app
from ipaddress import ip_address, ip_network


class Webhooks():
    """Github Webhooks"""

    def __init__(self):
        # Flask.route needs __name__
        self.__name__ = 'webhooks'

    def __call__(self):

        self.event, self.delivery, self.payload = parse_request()
        try:
            fn = getattr(self, self.event)
        except:
            abort(400, "Not Implemented")
        fn()

    def ping(self):
        return "Hello World"

    def push(self):
        pass


def parse_request():
    if current_app.config.get('github_ips_only', True):
        check_ip()

    secret = current_app.config.get('enforce_secret', '')
    if secret:
        check_signature(secret)

    event = request.headers.get('X-GitHub-Event')
    delivery = request.headers.get('X-GitHub-Delivery')

    # Gather data
    try:
        payload = json.loads(request.data)
    except:
        abort(400)

    return event, delivery, payload


def check_ip():
    # Allow Github IPs only
    src_ip = ip_address(request.remote_addr)
    whitelist = requests.get('https://api.github.com/meta').json()['hooks']
    for valid_ip in whitelist:
        if src_ip in ip_network(valid_ip):
            break
    else:
        abort(403, "ipaddress not allowed")


def check_signature(secret):
    # Only SHA1 is supported
    header_signature = request.headers.get('X-Hub-Signature')
    if header_signature is None:
        abort(403, "missing signature")

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        abort(501)

    # HMAC requires the key to be bytes, but data is string
    secret = secret.encode('ascii')
    signature = signature.encode('ascii')
    mac = hmac.new(secret, msg=request.data, digestmod=sha1)
    if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
        abort(403, "bad signature")
