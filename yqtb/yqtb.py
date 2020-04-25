import requests
import time
import sys

s = requests.Session()
 
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
    
if __name__ == '__main__':
    if not login(sys.argv[1], sys.argv[2]):
        print(tb()) 
        