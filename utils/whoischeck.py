from datetime import datetime
import time

class DomainQuery:
    def __init__(self, **kwargs) -> str:
        """
        Verilen domain __init__ içerisinde başlıklardan arındırılır. Eğer kişi init"i yazdırırsa __str__ ve __repr__ fonksiyonu geri dönüş yapar.
        :param kwargs: domain(ex:www.enesergun.net)
        :return: str
        """
        self.domain = kwargs.get("domain")

        clear = self.domain.replace('wwww.','')
        clear = clear.replace('http://','')
        clear = clear.replace('https://','')
        self.tld = clear
        fld = clear.split('.')
        self.fld = f'{fld[-2]}.{fld[-1]}'

    def __str__(self) -> str:
        """
        Class direkt olarak yazdırılırsa defaultta ekrana ne bastıralacağını ayarlıyoruz.
        :return: str
        """
        return f"<{self.domain}> Domain TLDs: {self.tld}"

    def __repr__(self) -> str:
        """
        Class direkt olarak yazdırılırsa defaultta ekrana ne bastıralacağını ayarlıyoruz.
        :return: str
        """
        return f"<{self.domain}> Domain TLDs: {self.tld}"

    def connect_whois_server(self, **kwargs) -> str:
        """
        Whois server"a 43 portu üzerinden Socket ile bağlanmak için fonksiyonumuzdur. İlk olarak iana"ya bağlanıp domain için gerekli olan
        whois sunucuyu kullanıp daha sonra aynı fonksiyon ile Expire date getiriyoruz. Default olarak iana"ya bağlanır.
        :param kwargs: whserver(ex:whois.iana.org)
        :return: str
        """
        import socket
        self.whoisserver = kwargs.get("whserver")
        if self.whoisserver == None:
            self.whoisserver = "whois.iana.org"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((self.whoisserver, 43))

        domain = self.tld.encode("utf-8") + b"\r\n"
        sock.send(domain)
        self.resp = ""
        while True:
            try:
                s = sock.recv(4096)
            except ConnectionResetError as e:
                pass
            try:
                self.resp += s.decode("utf-8")
            except UnicodeDecodeError:
                self.resp += s.decode("latin-1")

            if not s:
                break

        sock.close()
        return self.resp

    @property
    def get_whois_server(self) -> str:
        """
        Whois server response'u içerisinde, whois server geçen stringi parse ediyoruz.
        :return: str
        """
        for i in self.resp.splitlines():
            if i.startswith("whois"):
                whois_server = i.split(":")[1].strip()
        return whois_server

    @property
    def get_expire_date(self) -> datetime:
        """
        Sunuculara özel(Dünya geneli ve nic.tr) içerisinde geçen expire date kısmını parse ediyor. Sunucular farklı datetime formatlarında gönderebiliyor.
        :return: datetime
        """
        if self.whoisserver == "whois.nic.tr":
            for i in self.resp.splitlines():
                if i.startswith("Expires on.."):
                    expire_date = i.split(":")[1].strip()
                    expire_date = expire_date.split(".")[0].strip()
                    expire_date = datetime.strptime(expire_date, "%Y-%b-%d")
                    time.sleep(10)
                    return expire_date

        else:
            for i in self.resp.splitlines():
                if "Registry Expiry Date" in i:
                    expire_date = i.split(":")[1].strip()
                    expire_date = expire_date.split("T")[0].strip()
                    expire_date = datetime.strptime(expire_date, "%Y-%m-%d")
                    return expire_date

    def expire_calculate(self, timeobj) -> int:
        """
        Verilen zaman ile günümüz arasında matematiksel işlem yapıp timedelta formatında çıktıyı int olarak döndürüyor.
        :param timeobj: [2019-03-21] formatında tarih objesi
        :return: int
        """
        now = datetime.now().date()
        try:
            whichday = datetime.date(timeobj) - now
            return whichday.days
        except:
            return None
