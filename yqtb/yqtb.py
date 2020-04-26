from bs4 import BeautifulSoup
import requests
import time
import sys
#import regex as re

s = requests.Session()
 
"""
登录
args stu_name: 学生名字
args stu_id: 学号
returns: 返回是否登录成功
"""
def login(stu_name, stu_id):
    login_url = 'https://wx.app.nbpt.edu.cn/yqtb/bind?schoolid=5'
    login_data = {
        'schoolid':'5', 
        'name': stu_name, 
        'identity': stu_id
    }
    response = s.post(url=login_url, data=login_data)
    #print(response.text)
    if not response.json()['error']:
        return response.json()['error']
    else:
        print(response.json()['msg'])
        return True

"""
    提交表单上报
  return: 返回提交的信息  
"""
def tb():
    tb_url = 'https://wx.app.nbpt.edu.cn/yqtb/weixin/yqtb/submit?date=20' + time.strftime('%y-%m-%d')
    tb_data = {
        'dqld':'', 
        'frks':'', 
        'jjxhd':'', 
        'sxqgjx':'', 
        'tips7':'',
        'jkm':'绿码', 
        'memo':'', 
        'geo':''
    }

    response = s.post(url=tb_url, data=tb_data)
    #print(response.text)
    return response.json()['msg']

"""
    获取排行榜
"""
def ranking():
    rk_url = 'https://wx.app.nbpt.edu.cn/yqtb/weixin/yqtb/rank?date=20' + time.strftime('%y-%m-%d')
    rk = s.get(rk_url)
    html = rk.text
    
    soup = BeautifulSoup(html,'lxml')

    print('前百名学生排行：')
    for line in soup.find_all(class_='tab-page')[0].find_all(class_='weui-cell'):
        result = line.text.split()
        print('第{}名：{}同学 \t{}  \t{}'.format(result[0],result[1],result[2],result[3]))

    print('\n')
    print('-'*80)
            
    print('\n班级排行及完成率')
    for line in soup.find_all(class_='tab-page')[1].find_all(class_='weui-cell'):
        result = line.text.split()
        print('第{}名\t{}\t\t完成率{}%'.format(result[0],result[1],result[2]))

    print('\n')
    print('-'*80)
            
    print('\n院系完成率')
    for line in soup.find_all(class_='tab-page')[2].find_all(class_='weui-cell'):
        result = line.text.split()
        print('{}   \t完成率{}'.format(result[0],result[1]))


"""
正则写的实在太慢
def ranking():
    rk_url = 'https://wx.app.nbpt.edu.cn/yqtb/weixin/yqtb/rank?date=20' + time.strftime('%y-%m-%d')
    rk = s.get(rk_url)
    html = rk.text
    print(html)
    reg = re.compile('<div.*?ll__bd.*?5px;\">(.*?)</span>(.*?)<span sty.*?or:#999\">(.*?)</span>.*?</div>', re.S)
    result = re.findall(reg, html)
    
    print(result)
    for r in result:
        print("第{}名：\t{}\t{}".format(r[0], r[1].strip(), r[2]))
"""


if __name__ == '__main__':
    if not login(sys.argv[1], sys.argv[2]):
        print(tb()) 
        ranking()
        