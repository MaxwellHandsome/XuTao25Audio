import requests, os, random, re
from bs4 import BeautifulSoup

# 从喜马拉雅获取播放列表，封装到dictionary里。数据结构：title-playerURL
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
    

# 随机化query的token
def random_token(length=10):
    characters = '0123456789abcde'
    random_string = ''.join(random.choice(characters) for _ in range(length))
    print("Randomized token:"+random_string)
    return random_string


# 主程序入口

#获取播放列表
url_dict = get_url()
print(url_dict)


# 获取播放列表里最新的音频链接
latest_title = next(iter(url_dict))
latest_webplayerUrl = url_dict[latest_title]
print("latest: "+latest_title+" -> "+latest_webplayerUrl)


# 调用外部api获取直链
url = 'https://3g.gljlw.com/diy/ximalaya.php?url='+latest_webplayerUrl
headers = {
    'cookie': 'weixin114514=popup-ad; security_session_verify=114514'+random_token(),
    'priority': 'u=0, i',
    'referer': 'https://3g.gljlw.com/diy/ximalaya.php',
    'user-agent': 'Mozilla/5.0 (X114514; Linux riscv64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.5.1.4 Safari/191.98'
}
# 获取fetcher的纯文本html结果
response = requests.get(url, headers=headers)
fetcher_content = response.text


# 正则表达式匹配以 https://aod.cos.tx.xmcdn.com 开头的链接
pattern = r'https://aod\.cos\.tx\.xmcdn\.com[^\s]*'
cdn_url=""


# 获取CDN链接
try:
    cdn_url = re.findall(pattern, fetcher_content)[0][0:-1]
    print(cdn_url)
except Exception as e:
    print(f"发生错误: {e} \nfetch error. see debug.html")
    with open("debug.html", 'w', encoding='utf-8') as file:
        file.write(fetcher_content)
    exit()


# 调用shell script保存到播放列表
os.system("./appendDailyLink.sh "+latest_title+" "+cdn_url)