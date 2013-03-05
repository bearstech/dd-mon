#!/usr/bin/env python
import os
from restkit import Resource


r = Resource(os.environ['DD_URL'])


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
    for k, v in fetch('Status_Wireless.live.asp'):
        print k, v
    for k, v in fetch('Status_Lan.live.asp'):
        print k, v
