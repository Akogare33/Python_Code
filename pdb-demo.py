import os
import time
import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

damai_url = "https://www.damai.cn/"
login_url = "https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
target_url = 'https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.285c47b0tDH0Ru&id=764264835969&clicktitle=%E3%81%9A%E3%81%A3%E3%81%A8%E7%9C%9F%E5%A4%9C%E4%B8%AD%E3%81%A7%E3%81%84%E3%81%84%E3%81%AE%E3%81%AB%E3%80%82%EF%BC%88%E6%B0%B8%E8%BF%9C%E6%98%AF%E6%B7%B1%E5%A4%9C%E6%9C%89%E5%A4%9A%E5%A5%BD%E3%80%82%EF%BC%892024%E4%B8%8A%E6%B5%B7%E6%BC%94%E5%94%B1%E4%BC%9A'

class Concert:
    def __init__(self):
        self.status = 0         # 状态,表示如今进行到何种程度
        self.login_method = 1  
        self.driver = webdriver.Chrome()       # 默认Chrome浏览器
    
    def set_cookie(self):
        self.driver.get(damai_url)
        print("###请点击登录###")
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:
            sleep(1)
        print('###请扫码登录###')

        while self.driver.title != '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
            sleep(1)
        print("###扫码成功###")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")
        self.driver.get(target_url)


    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain':'.damai.cn',  
                    'name': cookie.get('name'),
                    'value': cookie.get('value')
                }
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)
    
    def login(self):
        if self.login_method == 0:
            self.driver.get(login_url)
            print('###开始登录###')

        elif self.login_method == 1:
            if not os.path.exists('cookies.pkl'):
                self.set_cookie()
            else:
                self.driver.get(target_url)
                self.get_cookie()
    
    def isElementExistByClass(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element_by_xpath(element)
            return flag
    
        except:
            flag = False
            return flag
        
    def enter_concert(self):
        """打开浏览器"""
        print('###打开浏览器，进入大麦网###')
        self.driver.maximize_window()           # 最大化窗口
        # 调用登陆
        self.login()                            # 先登录再说
        # self.driver.refresh()                   # 刷新页面
        self.status = 2                         # 登录成功标识
        print("###登录成功###")
    
    def choose_ticket(self):
        if self.status == 2:                  #登录成功入口
            print("="*30)
            print("###检查是否开始售票###")
            while not self.isElementExistByClass('buy-link'):
                self.driver.refresh()
                print("###售票尚未开始,刷新等待开始###")
            #TODO 选择票型
            #========begin=========


            #========end===========
            self.driver.find_element(By.CLASS_NAME, 'buy-link').click()    #点击购票二维码下的购买连接
            time.sleep(1.5)
            self.check_order()
    
    def check_order(self):
        if self.status == 2:
            print('###开始确认订单###')
            if self.driver.title == '订单确认页':
                print('###检查是否需要填写观影人')
                if self.isElementExistByXPATH('//*[@id="dmViewerBlock_DmViewerBlock"]'):
                    self.driver.find_element(By.XPATH, '//*[@id="dmViewerBlock_DmViewerBlock"]/div[2]/div/div').click()
                    time.sleep(0.5)
                print('###跳转支付选择界面###')
                self.driver.find_element(By.XPATH, '//*[@id="dmOrderSubmitBlock_DmOrderSubmitBlock"]/div[2]/div/div[2]/div[2]/div[2]').click()
                time.sleep(2)
                self.pay_order()
    
    def pay_order(self):
        if self.driver.title == "支付宝付款":
            print('###支付订单###')
            if self.isElementExistByXPATH('//*[@id="app"]/div[3]/div[1]/button[2]'):
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[1]/button[2]').click()
                print('###跳转至浏览器支付###')
                time.sleep(1.5)
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div[1]/div[2]/input').clear()
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div[1]/div[2]/input').send_keys('支付宝账号')      #输入支付宝账号
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/button').click()
                time.sleep(1.5)
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/button').click()
                while True:
                    time.sleep(1)
                    print('###请输入支付密码###')
    
    def finish(self):
        self.driver.quit()


if __name__ == '__main__':
    try:
        con = Concert()  # 具体如果填写请查看类中的初始化函数
        con.enter_concert()  # 打开浏览器
        con.choose_ticket()  # 开始抢票

    except Exception as e:
        print(e)
        con.finish()
