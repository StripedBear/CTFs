import requests
import xml.etree.ElementTree as ET
import argparse
from bs4 import BeautifulSoup, Comment
import re


def check_joomlav(link):

    ends = ["/administrator/manifests/files/joomla.xml", "/modules/custom.xml", "/language/en-GB/en-GB.xml"]
    for end in ends:
        res = requests.get(link+end)
        if res.status_code == 200:
            xml_content = res.content
            root = ET.fromstring(xml_content)
            version = root.find('version').text
            print("Version is: ", version)
            break


def check_phpv(link):
    res = requests.get(link)
    if 'X-Powered-By' in res.headers:
        php_version = res.headers['X-Powered-By']
        print("Версия PHP:", php_version)


def check_ccscmnt(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'lxml')
    style_links = soup.find_all('link', rel='stylesheet')
    style_urls = []
    for l in style_links:
        url = l.get('href')
        if url and not url.startswith('http'):
            url = f'{link}' + url
        style_urls.append(url)
    for url in style_urls:
        print(url)
        content = requests.get(url).text
        comments = re.findall(r"/\*(.*?)\*/", content, re.DOTALL)
        [print(comment.strip()) for comment in comments]


def check_htmlcnt(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'lxml')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        print(comment)
    		

parser = argparse.ArgumentParser(description='Joomla checker') 
parser.add_argument('-t', '--target', type=str, help='Target: https://example.example')
parser.add_argument('-c', '--css', action='store_const', const=True, default=False)
parser.add_argument('-H', '--html', action='store_const', const=True, default=False)
parser.add_argument('-j', '--joomla', action='store_const', const=True, default=False)
parser.add_argument('-p', '--php', type=str, help='Not now...')
args = parser.parse_args()


if args.css:
    check_ccscmnt(args.target)
elif args.html:
    check_htmlcnt(args.target)
elif args.php:
	check_phpv(args.target)
elif args.joomla:
    check_joomlav(args.target)
else:
	print('No target. check -h for help')
