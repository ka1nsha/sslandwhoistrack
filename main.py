from modules.sslcheck import *
from modules.whoischeck import *
import json, yaml
import logging
from logging import config

with open("config/log_config.json", "r") as e:
    cfg = json.load(e)
config.dictConfig(cfg)

with open('config/sites.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

def render_template(template, **kwargs) -> str:
    """
    Parametre olarak verilmiş olan j2 uzantılı dosya içerisinde **kwargs içerisinde verilmiş tüm değişkenleri arayarak bu değişkenleri render eder ve html olarak geri döner.
    :param template: Template dosyasının konumu veya ismi default olarak bulunduğu konumda arar. (Ex: mail.j2)
    :param kwargs: templatevariables(Ex: ERRORS)
    :return: str
    """
    import jinja2
    import os

    templateLoader = jinja2.FileSystemLoader(searchpath=os.getcwd())
    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)

    return templ.render(**kwargs)

def send_email(to, cc=None, bcc=None, subject=None, body=None, To=None) -> None:
    """
    HTML olarak email gönderen fonksiyondur. Fonksiyon içerisinde mail konfigürasyonları yapılması gerekmektedir.
    :param to: Kime gönderileceği. [Liste]
    :param cc: CC Olarak kimlerin görebileceği
    :param bcc: Gizli CC
    :param subject: Mail başlığı
    :param body: Mail içeriği
    :param To: None
    :return: None
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    gmail_user = "@gmail.com"
    gmail_pass = ""

    msg = MIMEMultipart("alternative")
    msg["From"] = gmail_user
    msg["Subject"] = subject
    msg["To"] = ",".join(to)
    # msg["Cc"] = cc
    # msg["Bcc"] = bcc
    msg.attach(MIMEText(body, "html"))
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com",465, context=context)

    try:
        server.login(gmail_user,gmail_pass)
        server.sendmail(gmail_user, ",".join(to), msg.as_string())
        to = ",".join(to)
        logging.info(f"Mailler {to} kişilerine {subject} başlığı ile başarılı bir biçimde gönderilmiştir.")

    except Exception as e:
        logging.error(f"{__name__}: Mail gönderilirken hata meydana gelmiştir. Hata: {e}")

    finally:
        server.quit()


CERT_DAYS = {}
DOMAIN_DAYS = {}
ERRORS = {}

for i in data[sites]:
    cert = CertInfo(hostname=i)
    try:

        cert.connect()
        logging.info(
            f"{i} Sitesinin SSL Süresinin Bitmesine {cert.time_remaining} gün vardır. SSL Süresi {cert.expire_date} tarihinde sonlanacaktır.")

        if cert.time_remaining < 30:
            CERT_DAYS[i] = f"{cert.time_remaining} Gün"

    except AttributeError as e:
        message = f"{__name__}: {i} Sitesinin SSL Sorgulamasında hata meydana gelmiştir. <Hata>:{e}"
        ERRORS.setdefault("SSL", []).append(i)
        logging.warning(message)

    except socket.gaierror as e:
        message = f"{__name__}: {i} Sitesinin SSL Sorgulamasında hata meydana gelmiştir. <Hata>:{e}"
        ERRORS.setdefault("SSL", []).append(i)
        logging.warning(message)

    except ssl.SSLCertVerificationError as e:
        message = f"{__name__}: {i} Sitesinin SSL Sorgulamasında hata meydana gelmiştir. <Hata>:{e}"
        ERRORS.setdefault("SSL", []).append(i)
        logging.warning(message)

logging.info("Sertifika kontrolleri tamamlanmış olup, domain kontrollerine geçilmektedir.")

for i in sites:
    try:
        wh = DomainQuery(domain=i)
        wh.connect_whois_server()
        whserver = wh.get_whois_server

        whois_response = wh.connect_whois_server(whserver=whserver)
        expire_date = wh.expire_calculate(wh.get_expire_date)
        logging.info(
            f"{i} domainin son kullanım tarihi {wh.get_expire_date} olup, dolmasına {expire_date} gün kalmıştır.")

        if expire_date < 30:
            DOMAIN_DAYS[i] = [expire_date, whserver]

    except tld.exceptions.TldBadUrl as e:

        logging.warning(f"{__name__}: {i} sitesine whois sorgusu yapılırken hata meydana gelmiştir. Hata: {e}")
        ERRORS.setdefault("DOMAIN", []).append(i)
    except socket.timeout as e:
        logging.error(f"{__name__}: {i} sitesine whois sorgusu yapılırken kritik bir hata meydana gelmiştir. Hata: {e}")
        ERRORS.setdefault("DOMAIN", []).append(i)

logging.info("Domain kontrolleri tamamlanmış olup, E-Mail atılacaktır.")

html = render_template("mail.j2", CERT_DAYS=CERT_DAYS, DOMAIN_DAYS=DOMAIN_DAYS,ERRORS=ERRORS)

to_list = ["info@enesergun.net","r4wn3ss@gmail.com"]
subj = "Domain Kayıtları"
send_email(to_list,subject=subj,body=html)
logging.info(f"Tüm işlemler tamamlandı. Rapor çıktısı {to_list} ile paylaşıldı.")