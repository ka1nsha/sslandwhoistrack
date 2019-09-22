from tld import get_tld, get_fld
from subprocess import Popen, PIPE
import socket,re
import json

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
    
#    @property
#    def choose_whois_server(self):
#        with open('modules/serverlist.json') as fd:
#            json_file = json.load(fd)
#            key = f"{self.tld}"
#            whois_server = json_file[key][0]
#        return whois_server
    
    
    def connect_whois_server(self, **kwargs):
        import socket
        whoisserver = kwargs.get('whserver','whois.iana.org')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((whoisserver,43))
        print(whoisserver)
        domain = self.fld.encode() + b"\r\n"
        sock.send(domain)
        resp = ""
        while True:
            s = sock.recv(4096)
            resp += s.decode()

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
                whois_server = i
        return whois_server

