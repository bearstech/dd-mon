import requests


class DD(object):

    def __init__(self, address, user, password):
        self.address = address
        self.user = user
        self.password = password
        self.data = {}

    def fetch(self, page):
        r = requests.get("%s/%s.live.asp" % (self.address, page), auth=(self.user, self.password))
        for line in r.text.split("\n"):
            kv = line[1:-1].split('::', 2)
            if kv != ['']:
                yield kv

    def clear(self):
        self.data = {}

    def refresh(self, page):
        self.data[page] = {}
        for k, v in self.fetch(page):
            self.data[page][k] = v

    def wireless_clients(self):
        d = self.data['Status_Wireless']['active_wireless'][1:-1].split("','")
        for a in range(0, len(d) - 9, 9):
            (mac, interface, uptime, tx, rx, signal, noise, SNR, stuff) = d[a :a + 9]
            signal = ununit(unquote(signal))
            noise = ununit(unquote(noise))
            SNR = unquoteint(SNR)
            yield unquote(mac), {
                'if': unquote(interface),
                'uptime': unquote(uptime),
                'tx': unquote(tx),
                'rx': unquote(rx),
                'signal': signal,
                'noise': noise,
                'SNR': SNR,
                'quality': round(signal * 1.0 / noise * SNR, 1)
            }


def unquote(txt):
    if txt[0] == "'":
        start = 1
    else:
        start = 0
    if txt[-1] == "'":
        return txt[start:-1]
    else:
        return txt[start:]


def unquoteint(txt):
    return int(unquote(txt))


def ununit(txt):
    try:
        return int(txt)
    except ValueError:
        if txt[-1] == 'K':
            return int(txt[:-1]) * 1000
        if txt[-1] == 'M':
            return int(txt[:-1]) * 1000000
        if txt[-1] == 'G':
            return int(txt[:-1]) * 1000000000
        raise Exception("Unknown unit : %s" % txt[-1])

if __name__ == '__main__':
    import os
    from urlparse import urlparse

    b = urlparse(os.environ['DD_URL'])
    dd = DD('%s://%s%s' % (b.scheme, b.hostname, b.path), b.username, b.password)
    #for page in ['Status_Router', 'Status_Internet', 'Info', 'Status_Wireless', 'Status_Lan']:
        #for k, v in dd.fetch(page):
            #print k, "\n\t", v
    dd.refresh('Status_Wireless')
    for mac, values in dd.wireless_clients():
        print mac, values
        print
