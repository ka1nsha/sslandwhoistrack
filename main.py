from modules.sslcheck import *
from modules.whoischeck import *
#cert = CertInfo(hostname="enesergun.net")
#cert.connect()
#print(cert.return_json)
wh = DomainQuery(domain='https://enesergun.net')

wh.connect_whois_server()

whois_response = wh.connect_whois_server(whserver=wh.get_whois_server)
print(whois_response)