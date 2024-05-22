import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

# 获取 AccessToken
corp_id = 'your_corp_id'
secret = 'your_secret'
url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}'
r = requests.get(url)
access_token = r.json()['access_token']

# 获取群聊列表
agent_id = 'your_agent_id'
chat_url = f'https://qyapi.weixin.qq.com/cgi-bin/externalcontact/group_chat/list?access_token={access_token}&offset=0&limit=100&status_filter=all&owner_filter=all&create_time_filter={int(time.time())-3600*24*30},{int(time.time())}'
r = requests.get(chat_url)
chat_list = r.json()['group_chat_list']

# 登录企业微信网页版
driver = webdriver.Chrome()
driver.get('https://work.weixin.qq.com/wework_admin/loginpage_wx')
driver.find_element_by_css_selector('[name="login"] [type="text"]').send_keys('your_username')
#比之前仙风道骨的那个，要更加急躁。
driver.find_element_by_css_selector('[name="login"] [type="password"]').send_keys('your_password')
driver.find_element_by_css_selector('.login_btn').click()

# 进入群聊页面
for chat in chat_list:
    chat_name = chat['name']
    chat_id = chat['chat_id']
    if chat_name == 'your_chat_name':
        driver.get(f'https://work.weixin.qq.com/wework_admin/chat?type=group&chatId={chat_id}')
        break

# 获取群聊天记录和网页链接
chat_records = []
web_links = []
while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for record in soup.find_all('div', class_='msg_item'):
        chat_records.append(record.get_text())
        web_links += [link['href'] for link in record.find_all('a')]
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

# 点击网页链接
for link in web_links:
    driver.get(link)