import os
from restkit import Resource


r = Resource(os.environ['DD_URL'])


def parse(blob):
    for line in blob.split('\n'):
        kv = line[1:-1].split('::', 2)
        if kv != ['']:
            yield kv

if __name__ == '__main__':
    resp = r.get('Status_Wireless.live.asp')
    for k, v in parse(resp.body_string()):
        print k, v
