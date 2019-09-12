from tld import get_fld
from subprocess import Popen, PIPE

class DomainQuery:
    def __init__(self,**kwargs):
        domain = kwargs.get('domain')
        if 'http' not in domain or 'https' not in domain:
            generate_tld_schema = f'http://{domain}'
            self.tld = get_fld(generate_tld_schema)
        else:
            self.tld = get_fld(domain)
    
    def __str__(self):
        return self.tld
    
    def __repr__(self):
        return self.tld
    
    
    def do_whois(self):
        process = Popen(['whois',self.tld], stdout=PIPE, stderr=PIPE)
        standartoutput,standarterror = process.communicate()