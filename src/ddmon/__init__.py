#!/usr/bin/env python
import requests


class DD(object):

    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password

    def fetch(self, page):
        r = requests.get("%s/%s.asp" % (self.address, page), auth=(self.user, self.password))
        for line in r.text.split("\n"):
            kv = line[1:-1].split('::', 2)
            if kv != ['']:
                yield kv


def parse(blob):
    for line in blob.split('\n'):
        kv = line[1:-1].split('::', 2)
        if kv != ['']:
            yield kv


def fetch(url):
    resp = r.get(url)
    for kv in parse(resp.body_string()):
        yield kv


if __name__ == '__main__':
    import os
    from urlparse import urlparse

    b = urlparse(os.environ['DD_URL'])
    dd = DD('%s://%s%s' % (b.scheme, b.hostname, b.path), b.username, b.password)
    for k, v in dd.fetch('Status_Wireless.live'):
        print k, v
    for k, v in dd.fetch('Status_Lan.live'):
        print k, v
