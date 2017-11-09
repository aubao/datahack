# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:00:08 2017

@author: jbh
"""

from bs4 import BeautifulSoup
import xlsxwriter
import urllib.request, urllib.parse, http.cookiejar
import re
from selenium import webdriver
import pandas as pd
import time
haved = pd.read_csv('d:\wx.csv')

chromedriver = "D:\Anaconda2\Scripts\chromedriver.exe"
driver = webdriver.Chrome(chromedriver)
driver.get("http://weixin.sogou.com/")
driver.find_element_by_id("loginBtn").click()
driver.find_element_by_id("query").send_keys("育儿")
driver.find_element_by_class_name("swz2").click()
#driver.find_element_by_class_name("code").click()
qrcode = [] 
url = []
update_time = []
wx = {} 
#the num of article every month
#for x in bs.find_all(class_="info"):
    #print(re.findall(r"</span>(.+?)</p>",str(x)))

def getHtml(url):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'),
    ('Cookie', '4564564564564564565646540')]
    
    urllib.request.install_opener(opener)
    
    html_bytes = urllib.request.urlopen(url).read()
    html_string = html_bytes.decode('utf-8')
    return html_string


def get_url(url):
    bs = BeautifulSoup(driver.page_source, "lxml")
    for a in bs.find_all('p'):
        try:
            url.append(a.a['href'])
        except:
            pass
    return url
#    for x in bs.find_all('span'):
#        time = re.findall(r"</script>(.+?)</span>",str(x))
#        if time:
#            update_time.extend(time)


def get_wx(wx,url):
    html_doc = getHtml(url)
    soup = BeautifulSoup(html_doc, 'html.parser')    
    wx_name = soup.find_all(class_="profile_nickname")[0].contents
    try:
        wx_id = soup.find_all(class_="profile_account")[0].contents
    except:
        wx_id='unknown'
    wx_desc = soup.find_all(class_="profile_desc_value")[0].contents
    wx_qrcode = soup.find_all('img',id="js_pc_qr_code_img") [0].get('src')
    wx_qrcode_url = 'https://mp.weixin.qq.com'+wx_qrcode
    wx[wx_name[0].strip()] = (wx_id[0],wx_desc[0],wx_qrcode_url)
    #save_img(wx_name[0].strip(),wx_qrcode_url)

def get_qrcode(qrcode):
    bs = BeautifulSoup(driver.page_source, "lxml")
    for x in bs.find_all('img',height='104'):
        tmp = re.findall(r"qrcodeShowError\('(.+?)',4,",str(x))
        tmp = tmp[0].replace('amp;','')
        qrcode.append(tmp)
    return qrcode


def save_img(img_name,url):
    image = urllib.request.urlopen(url)
    with open(str(img_name)+'.png', 'wb') as f:
        f.write(image.read())

def write_xlsx():
    book = xlsxwriter.Workbook('pict1.xlsx')
    sheet = book.add_worksheet('demo')
    sheet.write('A1', '微信公众号名称')
    sheet.write('B1', '微信公众号ID')
    sheet.write('C1', '微信公众号描述')
    sheet.write('D1', '二维码')
    #sheet.write('E1', '二维码地址')
    i = 2
    for k,v in wx.items():
        if k not in list(haved.name):
            sheet.write('A'+str(i),k)
            sheet.write('B'+str(i), v[0])
            sheet.write('C'+str(i), v[1])
            sheet.write('E'+str(i), v[2])
            #sheet.insert_image('D'+str(i),k+'.png',{'x_scale': 0.25, 'y_scale': 0.25})
            i += 1
        else:
            print(k)
    book.close()

def get_all_urls():
    flag = True
    while flag:
        get_url(url)
        try:
            driver.find_element_by_id("sogou_next").click()
            time.sleep(10)    
        except:
            flag = False
def run(no):
    i = no
    for link in url[no:]:
        print (i)
        get_wx(link)
        time.sleep(10)
        i += 1