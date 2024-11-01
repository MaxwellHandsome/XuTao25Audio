import requests, os, random, re
from bs4 import BeautifulSoup

# Fetch playlist from XMLY and save into dictionary. ADT: title - playerURL
def get_url():
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Host' : "www.ximalaya.com"
    }
    url_dict = {}
    link = "http://www.ximalaya.com/album/84195687"
    html = requests.get(link,headers=headers,timeout = 100)
    print("Status code：",html.status_code)
    soup = BeautifulSoup(html.text, 'html.parser')
    target_div = soup.find('ul', class_='seo-track-list H_g')
    links = target_div.find_all('a')
    for link in links:
        url_dict[link.text]=link["to"]
    return url_dict
    

# Randomize cookie token
def random_token(length=10):
    characters = '0123456789abcde'
    random_string = ''.join(random.choice(characters) for _ in range(length))
    print("Randomized token:"+random_string)
    return random_string


# ENTRY OF SCRIPT

# Fetch playlist from XMLY
url_dict = get_url()
print(url_dict)


# Get latest playerURL from dictionary above
latest_title = next(iter(url_dict))
latest_webplayerUrl = url_dict[latest_title]
print("\n")
print("[latest] "+latest_title+" -> "+latest_webplayerUrl)
if input("Continue?(Y/n)\n") == "n":
    print("Abort.")
    exit()


# Grab CDN URL from gljw
url = 'https://3g.gljlw.com/diy/ximalaya.php?url='+latest_webplayerUrl
headers = {
    'cookie': 'weixin114514=popup-ad; security_session_verify=114514'+random_token(),
    'priority': 'u=0, i',
    'referer': 'https://3g.gljlw.com/diy/ximalaya.php',
    'user-agent': 'Mozilla/5.0 (X114514; Linux riscv64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.5.1.4 Safari/191.98'
}
# Raw text of HTML
response = requests.get(url, headers=headers)
fetcher_content = response.text


# Match CDN URL with https://aod.cos.tx.xmcdn.com by regex
pattern = r'https://aod\.cos\.tx\.xmcdn\.com[^\s]*'
cdn_url=""
try:
    cdn_url = re.findall(pattern, fetcher_content)[0][0:-1]
    print("CDN URL fetched!")
    print(cdn_url)
except Exception as e:
    print(f"{e} \nfetch error. see debug.html")
    with open("debug.html", 'w', encoding='utf-8') as file:
        file.write(fetcher_content)
    exit()


# Save to hexo source
print("Now adding url to hexo source file...")
os.system("./appendDailyLink.sh "+latest_title+" "+cdn_url)
print("Added, now enjoy studying it..")