import requests


class DD(object):

    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password

    def fetch(self, page):
        r = requests.get("%s/%s.live.asp" % (self.address, page), auth=(self.user, self.password))
        for line in r.text.split("\n"):
            kv = line[1:-1].split('::', 2)
            if kv != ['']:
                yield kv


if __name__ == '__main__':
    import os
    from urlparse import urlparse

    b = urlparse(os.environ['DD_URL'])
    dd = DD('%s://%s%s' % (b.scheme, b.hostname, b.path), b.username, b.password)
    for page in ['Status_Router', 'Status_Internet', 'Info', 'Status_Wireless', 'Status_Lan']:
        for k, v in dd.fetch(page):
            print k, v
