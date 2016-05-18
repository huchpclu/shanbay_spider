import sys
import requests
import time
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup

login_url = 'https://www.shanbay.com/accounts/login/'
xiaozu_url = 'https://www.shanbay.com/team/members/?page=%s'
checkin_url = 'http://www.shanbay.com/api/v1/checkin/?for_web=true'
names = []

username = '账号'
password = '密码'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',}

s = requests.session()

csrftoken = s.get(login_url).cookies['csrftoken']


login_data = {'username': username,
              'password': password,
              'csrfmiddlewaretoken': csrftoken}

r = s.post(login_url, data=login_data, headers=headers)
print('Login successful...')
url = xiaozu_url % '1'
html = s.get(url)
bsObj = BeautifulSoup(html.text, 'lxml')
end = bsObj.find_all("a", {"class": "endless_page_link"})[-2].text
page = 1
while True:
    url = xiaozu_url % page
    xiaozu_html = s.get(url)
    bsObj = BeautifulSoup(xiaozu_html.text, 'lxml')
    users = bsObj.find_all("tr", {"class": "member"})
    for user in users:
        it = user.text
        if it.find("已打卡") == -1:
            name = user.find("a", {"class": "nickname"}).text
            names.append(name)
    if page == int(end) or len(users) == 0:
        break
    else:
        page += 1
i = 1
with open('skuids.txt', mode='w', encoding='utf8') as s:
    s.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'\n')
    for name in names:
        if i%5 == 0:
            s.write('@' + name + '\n')
            i+=1
        else:
            s.write('@' +name)
            i+=1
