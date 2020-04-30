from bs4 import BeautifulSoup
import requests
import time
import sys
import json

s = requests.Session()
 
"""
登录
args stu_name: 学生的名字
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
    return time.strftime('%y-%m-%d：') + response.json()['msg']

"""
    获取排行榜
    
    return: 返回排行信息
"""
def ranking():
    rk_url = 'https://wx.app.nbpt.edu.cn/yqtb/weixin/yqtb/rank?date=20' + time.strftime('%y-%m-%d')
    rk = s.get(rk_url)
    html = rk.text
    rank = ''
    soup = BeautifulSoup(html,'lxml')

    rank += '前百名学生排行：\n'
    for item in soup.find_all(class_='tab-page')[0].find_all(class_='weui-cell'):
        result = item.text.split()
        rank += '{}： {}    {}     {}\n'.format(result[0],result[1],result[2],result[3])

    rank += ('-'*80)
            
    rank += '\n班级排行及完成\n'
    for line in soup.find_all(class_='tab-page')[1].find_all(class_='weui-cell'):
        result = line.text.split()
        rank += '第{}：{}  完成率：{}\n'.format(result[0],result[1],result[2])

    rank += ('-'*80)
            
    rank += '\n院系完成率\n'
    for line in soup.find_all(class_='tab-page')[2].find_all(class_='weui-cell'):
        result = line.text.split()
        rank += '{}   完成率：{}\n'.format(result[0],result[1])
    
    print(rank)
    return rank.splitlines()

'''
    把提交日志写入到文件
    
    args msg: 日志
'''
def write_msg_of_file(msg):
    with open('tb_log.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(msg, ensure_ascii=False) + '\n')
        f.close()

'''
    把排行信息写入文件
    
    args ranking: 排行信息
'''
def write_ranking_of_file(ranking):
    with open('ranking.txt', 'w', encoding='utf-8') as f:
        for line in ranking:
            f.write(json.dumps(line, ensure_ascii=False) + '\n')
        f.close()



if __name__ == '__main__':
    if not login(sys.argv[1], sys.argv[2]):
        msg = tb()
        print(msg)
        write_msg_of_file(msg) 
        rank = ranking()
        write_ranking_of_file(rank)
        
        