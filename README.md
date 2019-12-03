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

**Not**: SSL ve Whois sorgusu sonucu eğer 30 günden daha az bir süre varsa mail içerisinde ilgili domain yer alacaktır. 


# [EN] SSL and Whois Info Tracker
This application does raw query for calculating SSL and domain expiration dates in `config/sites.yml` sites. If that expiration date is lower than 30 days, it sends remaining day about of domain used e-mail. (You can look Email Settings.)

Application uses gmail for default settings, if you want change server or etc. you should edit `gmail_user` and `gmail_pass` variables in main.py. If you don't use gmail (Might be local SMTP), be sure to delete `    context = ssl.create_default_context()` code in main.py



You might take error on runtime. If you take any error you should look at log files for debugging or other information about process time. It has 3 different log files.

These log files:

* log_error.log
* log_warning.log
* log_info.log

**Note**: Documentation pages are written in Turkish Language. Cause of i don't know enough English for that. I'm sorry.
**Note2**: If expiration date higher than 30 days, you couldn't see domain in mail. 
