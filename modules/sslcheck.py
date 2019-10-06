import socket, ssl, datetime
import json, tld


class CertInfo:
    def __init__(self, **kwargs):
        # Eğer port girilmemişse default olarak 443 portu üzerinden bağlantı kurmaya çalışıyor.
        kwargs.setdefault('port', 443)
        # Tüm fonksiyonlarda kullanabilmek adına değişkenler self olarak belirtiliyor.
        self.hostname = kwargs.get('hostname')
        self.hostname = tld.get_fld(self.hostname, fix_protocol=True)
        # self.hostname = socket.gethostbyname(self.hostname)
        self.port = kwargs.get('port')

    def connect(self):
        # SSL bağlantısı burada gerçekleştirilmektedir.
        context = ssl.create_default_context()
        con = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=self.hostname)
        # Eğer bağlantı gerçekleşmez veya beklerse maksimum bekleme saniyesi verilmiştir.
        con.settimeout(3.0)
        con.connect((self.hostname, self.port))
        # Tüm modül içerisinde kullanabilmek için bağlantı sırasında gelen sertifika bilgilerini global bir değişkene self ile alıyoruz.
        self.cert_info = con.getpeercert()

    @property
    def expire_date(self) -> datetime.datetime:
        # Expire olacağı tarihi SSL bilgileri içerisinde notAfter üzerinden alabilmekteyiz.
        expire_date = self.cert_info['notAfter']
        ssldateformat = r'%b %d %H:%M:%S %Y %Z'
        format_time = datetime.datetime.strptime(expire_date, ssldateformat)
        return format_time

    @property
    def time_remaining(self) -> datetime.timedelta:
        time_remaining = self.expire_date - datetime.datetime.utcnow()
        return time_remaining.days

    @property
    def return_json(self) -> str:
        return json.dumps(self.cert_info)
