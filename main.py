import json, yaml
import logging
from sys import argv
from logging import config
from os import path
from utils.whoischeck import *
from utils.sslcheck import *

# Logging Configuration Section
current_dir = path.dirname(path.realpath(__file__))
logconfigfile = path.join(current_dir,'config/log_config.json')

with open(logconfigfile, "r") as e:
    cfg = json.load(e)
config.dictConfig(cfg)

# Config of Websites(SSL and Whois Both)
sitesconfigfile = path.join(current_dir,'config/sites1.yml')

with open(sitesconfigfile) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

# Mail Schema Function
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
# Mail Function
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

    gmail_user = "sender"
    gmail_pass = "password"

    msg = MIMEMultipart("alternative")
    msg["From"] = gmail_user
    msg["Subject"] = subject
    msg["To"] = ",".join(to)
    # msg["Cc"] = cc
    # msg["Bcc"] = bcc
    msg.attach(MIMEText(body, "html"))
    context = ssl.create_default_context()
    server = smtplib.SMTP("smtp.gmail.com")

    try:
        server.login(gmail_user,gmail_pass)
        server.sendmail(gmail_user, ",".join(to), msg.as_string())
        to = ",".join(to)
        logging.info(f"Mailler {to} kişilerine {subject} başlığı ile başarılı bir biçimde gönderilmiştir.")

    except Exception as e:
        logging.error(f"{__name__}: Mail gönderilirken hata meydana gelmiştir. Hata: {e}")

    finally:
        server.quit()

# Functions
def checkWebSite(url):
    try:
        wh = DomainQuery(domain=url)
        wh.connect_whois_server()
        whserver = wh.get_whois_server
        whois_response = wh.connect_whois_server(whserver=whserver)
        expire_date = wh.expire_calculate(wh.get_expire_date)

        if expire_date == None:
            logging.error(f"{url} domaininin kullanım tarihi çekilememiştir.")
            ERRORS.setdefault("DOMAIN", []).append(url)

        else:
            logging.info(
                f"{url} domainin son kullanım tarihi {wh.get_expire_date} olup, dolmasına {expire_date} gün kalmıştır."
            )

            if expire_date < deltavalue:
                DOMAIN_DAYS[url] = [expire_date, whserver]

    except Exception as e:
        logging.error(
            f"{__name__}:Tanımlanmayan hata. Hata:- {e} -"
        )
    except socket.timeout as e:
        logging.error(f"{__name__}: {url} sitesine whois sorgusu yapılırken kritik bir hata meydana gelmiştir. Hata: {e}")
        ERRORS.setdefault("DOMAIN", []).append(url)

def checkCertificate(cert):
    certs = CertInfo(hostname=cert)
    try:

        certs.connect()
        logging.info(
            f"{cert} Sitesinin SSL Süresinin Bitmesine {certs.time_remaining} gün vardır. SSL Süresi {certs.expire_date} tarihinde sonlanacaktır.")

        if certs.time_remaining < deltavalue:
            CERT_DAYS[cert] = f"{certs.time_remaining} Gün"

    except AttributeError as e:
        message = f"{__name__}: {cert} Sitesinin SSL Sorgulamasında hata meydana gelmiştir. <Hata>:{e}"
        ERRORS.setdefault("SSL", []).append(cert)
        logging.warning(message)

    except socket.gaierror as e:
        message = f"{__name__}: {cert} Sitesinin SSL Sorgulamasında hata meydana gelmiştir. <Hata>:{e}"
        ERRORS.setdefault("SSL", []).append(cert)
        logging.warning(message)

    except Exception as e:
        message = f"{__name__}: {cert} Throwing Exception when SSL Certificate Checks. <Error>:{e}"
        ERRORS.setdefault("SSL", []).append(cert)
        logging.warning(message)

# SysArgv Configuration
options = []
argv = argv[1:]

# Conditions for getting timedelta value in arguments
if '-t' in argv:
    getindex = argv.index('-t')

    try:
        optionargument = argv[getindex + 1]
        deltavalue = int(optionargument)
    except IndexError as e:
        logging.warning(f"Argument Error in timedelta argument. Used Arguments:{argv}")
        print("Should be type timedelta values if you typed -t parameter")

if '-d' in argv:
    options.append('websites')
if '-c' in argv:
    options.append('certificates')

logging.info(f"Argument parsing succesfully done. Argument list:{argv}")

# Function Call with Options
## Global Variables for Reporting


## Main Process
for option in options:
    customers = data['customers']
    for customer in customers:

        CERT_DAYS = {}
        DOMAIN_DAYS = {}
        ERRORS = {}
        try:
            objects = customers[customer][option]
            for obj in objects:
                if option == 'websites':
                    checkWebSite(obj)
                if option == 'certificates':
                    checkCertificate(obj)
        except KeyError as e:
            pass
    logging.info("Kontroller tamamlanmış olup, E-Mail atılacaktır.")

    html = render_template("mail.j2", CERT_DAYS=CERT_DAYS, DOMAIN_DAYS=DOMAIN_DAYS, ERRORS=ERRORS)

    to_list = customers[customer]['mails']
    subj = "Domain Kayıtları"
    send_email(to_list, subject=subj, body=html)
    logging.info(f"Tüm işlemler tamamlandı. Rapor çıktısı {to_list} ile paylaşıldı.")





