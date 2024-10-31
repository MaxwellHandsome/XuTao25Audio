import requests, os
from bs4 import BeautifulSoup


def get_url():
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Host' : "www.ximalaya.com"
    }
    name_list = []
    url_list = []

    link = "http://www.ximalaya.com/album/84195687"
    html = requests.get(link,headers=headers,timeout = 100)
    print("相应状态码：",html.status_code)
    soup = BeautifulSoup(html.text, 'html.parser')
    target_div = soup.find('ul', class_='seo-track-list H_g')
    links = target_div.find_all('a')
    for link in links:
        name_list.append(link.text+" "+link["to"])
    return name_list

url = get_url()
print(url)
