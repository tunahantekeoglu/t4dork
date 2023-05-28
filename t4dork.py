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
    # buraya diğer dorklarınızı ekleyin
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
        # her bir dork için bulunan sonuçları yazdır
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
