import requests, os, random, re
from bs4 import BeautifulSoup


def get_url():
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Host' : "www.ximalaya.com"
    }
    url_dict = {}

    link = "http://www.ximalaya.com/album/84195687"
    html = requests.get(link,headers=headers,timeout = 100)
    print("相应状态码：",html.status_code)
    soup = BeautifulSoup(html.text, 'html.parser')
    target_div = soup.find('ul', class_='seo-track-list H_g')
    links = target_div.find_all('a')
    for link in links:
        url_dict[link.text]=link["to"]
    return url_dict
    

def random_token(length=10):
    # 定义字符集：包括0-9和a-e
    characters = '0123456789abcde'
    # 随机选择字符并组合成字符串
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string



url_dict = get_url()
print(url_dict)


# 获取第一个键值对
latest_title = next(iter(url_dict))
latest_webpageUrl = url_dict[latest_title]

print("latest: "+latest_title+" -> "+latest_webpageUrl)



# 调用外部api获取直链
url = 'https://3g.gljlw.com/diy/ximalaya.php?url='+latest_webpageUrl
headers = {
    'cookie': 'weixin114514=popup-ad; security_session_verify=114514'+random_token(),
    'priority': 'u=0, i',
    'referer': 'https://3g.gljlw.com/diy/ximalaya.php',
    'user-agent': 'Mozilla/5.0 (X114514; Linux riscv64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.5.1.4 Safari/191.98'
}

response = requests.get(url, headers=headers)
fetcher_content = response.text  # 获取纯文本格式的网页内容



# 正则表达式匹配以 https://aod.cos.tx.xmcdn.com 开头的链接
pattern = r'https://aod\.cos\.tx\.xmcdn\.com[^\s]*'
cdn_url=""

try:
    cdn_url = re.findall(pattern, fetcher_content)[0][0:-1]
    print(cdn_url)
except:
    print("fetch error. see debug.html")
    with open("debug.html", 'w', encoding='utf-8') as file:
        file.write(fetcher_content)
    exit()

os.system("./appendDailyLink.sh "+latest_title+" "+cdn_url)