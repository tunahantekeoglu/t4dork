import requests
from bs4 import BeautifulSoup
import time
import argparse
from termcolor import colored
from colorama import init
import random

# for colorama to work on Windows
init()

# Google dorks listesi
dorks = [
    'inurl:login',
    'intitle:"index of"',
    'inurl:admin',
    'intext:password',
    'ext:sql',
    'inurl:login',
    'filetype:txt',
    'intitle:index.of',
    'ext:doc | ext:docx | ext:odt',
    'filetype:xls | filetype:xlsx | filetype:ods',
    'filetype:log',
    'intext:username',
    'inurl:php?id=',
    'ext:xml | intext:password',
    'ext:conf inurl:wp-',
    'ext:env',
    'inurl:wp-content | inurl:wp-includes',
    'inurl:.git',
    'inurl:test/ | inurl:demo/',
    'ext:bak',
    'inurl:phpinfo.php',
    'inurl:robots.txt',
    'ext:csv | intext:email',
    'intitle:"index of /"',
    'inurl:debug',
    'inurl:ftp://',
    'intext:"access denied for user" intext:"using password"',
    'ext:swf',
    'ext:asp',
    'intitle:"webcam inurl:"ViewerFrame?Mode="',
    'inurl:public/',
    'inurl:private/',
    'ext:old',
    'inurl:attachments/',
    'ext:tmp | ext:temp',
    'inurl:download/',
    'intext:confidential',
    'intitle:"report" filetype:xls',
    'ext:json',
    'inurl:admin/',
    'inurl:500.shtml',
    'inurl:trace.axd',
    'ext:yml | intext:password',
    'intext:db_password',
    'ext:rb | intext:password',
    'filetype:ldif ldif',
    'intitle:"web service" filetype:asmx',
    'inurl:"web.config" filetype:config',
    'ext:jsp',
    'inurl:"id=" & intext:"Warning: mysql_fetch_assoc()',
    'inurl:"ViewerFrame?Mode="',
    'intext:"enable secret 5 $"',
    'intitle:"Apache::Status" (inurl:server-status | inurl:status.html | inurl:apache.html)',
    'intext:"MOBOTIX M1" intext:"Open Menu" intext:"MOBOTIX M10" intext:"Open Menu" intext:"MOBOTIX D10" intext:"Open Menu"',
    'intitle:"FTP root at"',
    'filetype:bak',
    'inurl:top.htm inurl:currenttime',
    'allinurl:/examples/jsp/snp/snoop.jsp',
    'intitle:"Under construction" "does not currently have"',
    'intitle:"Test Page for Apache Installation"',
    'inurl:5800',
    '"phone * * *" "address *" "e-mail" intitle:"curriculum vitae"',
    '"robots.txt" "Disallow:" filetype:txt',
    'intext:"Network Vulnerability Assessment Report"',
    'filetype:pwd service',
    'inurl:"webalizer.conf" intext:passwd -sample',
    'filetype:sql ("passwd values ****" | "password values ****" | "pass values ****")',
    'filetype:xls inurl:"email.xls"',
    'intitle:index.of passwd passwd.bak',
    'intitle:"index of" people.lst',
    'intitle:"usage statistics" "Microsoft-IIS/6.0"',
    'intitle:index.of administrators.pwd',
    'intitle:index.of trillian.ini',
    'intitle:index.of ws_ftp.ini',
    'inurl:admin inurl:backup intitle:index.of',
    'inurl:ospfd.conf intext:password -sample -test -tutorial -download',
    'intitle:index.of master.passwd',
    'filetype:inc dbconn',
    'intitle:index.of cfide',
    'inurl:temp | inurl:tmp | inurl:backup | inurl:bak',
    'inurl:"/phpmyadmin/"',
    'inurl:"/cacti/"',
    'inurl:webvpn.html',
    'inurl:.htpasswd',
    'inurl:"server-status"',
    'inurl:"/phpinfo.php"',
    'intitle:"PHPMyAdmin" "running on" inurl:"main.php"',
    'inurl:":2082/frontend"',
    'inurl:"/zabbix/"',
    'inurl:"/jenkins/script"',
    'inurl:"webdav/xmlrpc"',
    'inurl:"/horde/imp/test.php"',
    'inurl:"servlet/webacc"',
    'inurl:".nsf"',
    'inurl:"axis-cgi/mjpg"',
    'inurl:"/names.nsf"',
    'intitle:"index of" "wp-admin"',
    'intitle:"index of" ".well-known"',
    'intitle:"index of" ".git"',
    'intitle:"index of" ".svn"',
    'intitle:"index of"',
    'inurl:php?id=',
    'inurl:login.php',
    'inurl:admin.php',
    'inurl:wp-login.php',
    'inurl:upload.php',
    'inurl:shell.php',
    'inurl:config.php',
    'inurl:database.php',
    'inurl:backup.sql',
    'inurl:backup.zip',
    'inurl:db.sql',
    'inurl:db.bak',
    'inurl:config.ini',
    'inurl:config.bak',
    'inurl:secret.txt',
    'inurl:.env',
    'inurl:.gitignore',
    'inurl:.htaccess',
    'inurl:.htpasswd',
    'inurl:config.xml',
    'inurl:web.config',
    'inurl:phpinfo.php',
    'inurl:info.php',
    'inurl:test.php',
    'inurl:debug.php',
    'inurl:phpmyadmin/',
    'inurl:admin/',
    'inurl:administrator/',
    'inurl:panel/',
    'inurl:filemanager/',
    'inurl:uploadify/',
    'inurl:fckeditor/',
    'inurl:tiny_mce/',
    'inurl:ckeditor/',
    'inurl:upload/',
    'inurl:uploadify/',
    'inurl:fileupload/',
    'inurl:upload.php',
    'inurl:phpinfo.php',
    'inurl:info.php',
    'inurl:test.php',
    'inurl:debug.php',
    'inurl:backup.tar',
    'inurl:backup.zip',
    'inurl:backup.rar',
    'inurl:backup.sql',
    'inurl:backup.bak',
    'inurl:db.sql',
    'inurl:db.bak',
    'inurl:config.php',
    'inurl:config.bak',
    'inurl:config.ini',
    'inurl:secret.txt',
    'inurl:.env',
    'inurl:.gitignore',
    'inurl:.htaccess',
    'inurl:.htpasswd',
    'inurl:config.xml',
    'inurl:web.config',
    'inurl:wp-config.php',
    'inurl:wp-config.bak',
    'inurl:wp-config.old',
    'inurl:wp-config.txt',
    'inurl:wp-config.bak',
    'inurl:wp-config.old',
    'inurl:wp-config.txt',
    'inurl:wp-settings.php',
    'inurl:wp-settings.bak',
    'inurl:wp-settings.old',
    'inurl:wp-settings.txt',
    'inurl:wp-settings.bak',
    'inurl:wp-settings.old',
    'inurl:wp-settings.txt',
]

]

def google_dork(target, dork):
    headers = {'User-agent':'Mozilla/11.0'}
    url = f'https://www.google.com/search?q=site:{target}+{dork}'
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        result = []
        for link in links:
            href = link.get('href')
            if "url?q=" in href and not "webcache" in href:
                result.append(href.split("url?q=")[1].split("&")[0])
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main(target):
    # Google dorkları üzerinde dön
    for dork in dorks:
        print(colored(f"Google Dork: {dork}", 'red', attrs=['bold']))
        results = google_dork(target, dork)
        # Her bir dork için bulunan sonuçları yazdır
        if results:
            for i, result in enumerate(results, 1):
                print(colored(f"{i}. {result}", 'blue'))
        else:
            print("No results found.")
        # Google tarafından engellenmeyi önlemek için rastgele bir bekleme süresi
        time.sleep(random.uniform(3, 5))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Google Dork tool')
    parser.add_argument('-u', '--url', help='Target URL', required=True)
    args = parser.parse_args()
    main(args.url)

