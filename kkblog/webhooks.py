# coding: utf-8
from __future__ import unicode_literals, absolute_import, print_function
import requests
import six
from flask import request, json, abort
from ipaddress import ip_address, ip_network


class Webhooks():
    """Github Webhooks"""

    def __init__(self):
        self.__name__ = "webhooks"

    def __call__(self):

        self.event, self.delivery, self.payload = parse_request()
        try:
            fn = getattr(self, self.event)
        except:
            abort(404, "Not Implemented")
        fn()

    def ping(self):
        return "Hello World"

    def push(self):
        pass


def parse_request():
    if config.get('github_ips_only', True):
        check_ip()

    secret = config.get('enforce_secret', '')
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
    src_ip = ip_address(
        '{}'.format(request.remote_addr)  # Fix stupid ipaddress issue
    )
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
    secret = ensure_bytes(secret)
    signature = ensure_bytes(signature)
    mac = hmac.new(secret, msg=request.data, digestmod=sha1)
    digest = ensure_bytes(mac.hexdigest())
    # Python prior to 2.7.7 does not have hmac.compare_digest
    if hasattr(hmac, "compare_digest"):
        if not hmac.compare_digest(digest, signature):
            abort(403, "bad signature")
    else:
        # What compare_digest provides is protection against timing
        # attacks; we can live without this protection for a web-based
        # application
        if digest != strsignature:
            abort(403, "bad signature")


def ensure_bytes(text):
    if six.PY2:
        return str(text)
    else:
        return bytes(text, encoding="ascii")
