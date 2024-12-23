import requests as rq
from bs4 import BeautifulSoup

url = input("Enter Link: ")
try:
    # 添加协议检查
    data = rq.get(url if "http" in url else "https://" + url)
except rq.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

soup = BeautifulSoup(data.text, "html.parser")
links = []

# 提取并过滤空链接
for link in soup.find_all("a"):
    href = link.get("href")
    if href:
        links.append(href)

# 写入文件（覆盖模式）
with open("myLinks.txt", 'w') as saved:
    saved.write("\n".join(links[:10]))

print("Saved top 10 links to 'myLinks.txt'.")
