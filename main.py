from modules.sslcheck import *
from modules.whoischeck import *
#cert = CertInfo(hostname="enesergun.net")
#cert.connect()
#print(cert.return_json)
wh = DomainQuery(domain='https://enesergun.net')

print(wh.connect_whois_server)