from tld import get_tld, get_fld
from datetime import datetime

class DomainQuery:
    def __init__(self,**kwargs) -> str:
        self.domain = kwargs.get('domain')
        #self.tld = self.get_tld(self.domain)
        self.tld = get_tld(self.domain, as_object=True)
        self.fld = get_fld(self.domain,fix_protocol=True)
    
    def __str__(self) -> str:
        return f"<{self.domain}> Domain TLDs: {self.tld}"

    def __repr__(self):
        return f"<{self.domain}> Domain TLDs: {self.tld}"

    def connect_whois_server(self, **kwargs):
        import socket
        self.whoisserver = kwargs.get('whserver','whois.iana.org')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((self.whoisserver,43))

        domain = self.fld.encode('utf-8') + b"\r\n"
        sock.send(domain)
        resp = ""
        while True:
            s = sock.recv(4096)
            try:
                resp += s.decode('utf-8')
            except UnicodeDecodeError:
                resp += s.decode('latin-1')

            if not s:
                break
        sock.close()

        self.resp = resp
        return self.resp

    @property
    def get_whois_server(self):
        whois_server = None
        for i in self.resp.splitlines():
            if i.startswith('whois'):
                whois_server = i.split(':')[1].strip()
        return whois_server

    @property
    def get_expire_date(self):
        if self.whoisserver=='whois.nic.tr':
            for i in self.resp.splitlines():
                if i.startswith('Expires on'):
                    expire_date = i.split(':')[1].strip()
                    expire_date = expire_date.split('.')[0].strip()
                    expire_date = datetime.strptime(expire_date,'%Y-%b-%d')
                    now = datetime.today().date()
                    whichday = expire_date - now
                    return whichday.days()

                else:
                    pass