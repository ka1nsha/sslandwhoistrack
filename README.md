# SSL and Whois Tracker

İlgili uygulama `config/sites.yml` içerisinde verilen URL'lere ait SSL Sertifika ve Whois sorgularının takibini yapmaktadır. Eğer ilgili domainlerde herhangi bir Expiration date 30 günden az ise bunu mail olarak yollamaktadır. 

Default olarak Gmail ayarlarıyla gelmekte olup, ayarlarınızı yapabilmek için `main.py` içerisinden aşağıda ki değişkenlerin değiştirilmesi gerekmektedir. 
```
"gmail_user = "@gmail.com" 
gmail_pass = ""
```

İlgili değişiklikler yapıldıktan sonra `Jinja2` sayesinde HTML sayfası Render edilerek mail gönderimi gerçekleşecektir. Ayrıca eğer `çalışma zamanınında`  bir problem ile karşılaşırsanız aşağıda ki dosyalardan durum hakkında bilgi alabilir veya herhangi bir SIEM yazılımına log dosyalarını gönderebilirsiniz.


Log dosyaları:
* log_error.log
* log_warning.log
* log_info.log


İçerisinde kullanılan kodlarda açıklama yapmaya dikkat ettim. Eğer gözümden kaçan bir şey varsa `Pull Request` atmaktan çekinmeyiniz. Tüm repo master branch'i altında geliştirilmiştir. Başka bir branch kullanılmamıştır.

Otomatik generate edilen dökümantasyona ulaşmak için /html klasörünü altında `index.html` dosyasını açabilirsiniz.


