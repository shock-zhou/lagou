# -*- coding UTF-8 -*-
"""
title:抓取拉勾网的全国的数据分析岗位数据
time:2018-08-10
代码原网址：https://blog.csdn.net/qq_40717846/article/details/78405586
"""

import json,requests
import math,time,random
import csv
import os

def get_headers():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
        'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    ]
    #随机选择一个
    agent = random.choice(user_agent_list)
    headers = {
        "Cookie": "JSESSIONID=ABAAABAAAGFABEF42BEF59E4399E6803A6C5828361037D8; _ga=GA1.2.2021525041.1533343081; user_trace_token=20180804083732-92e4f5d4-977e-11e8-b189-525400f775ce; LGUID=20180804083732-92e4f8db-977e-11e8-b189-525400f775ce; _gid=GA1.2.330084222.1533688355; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533819692,1533861545,1533861558,1533861568; LGSID=20180810101909-c3932359-9c43-11e8-a37b-5254005c3644; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533869874; LGRID=20180810105743-270542b3-9c49-11e8-a37b-5254005c3644; SEARCH_ID=24a7effd344f4e779fd8c91aa2b93e24",
        "Host": "www.lagou.com",
        "Origin": "https://www.lagou.com",
        "Referer": "https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=",
        "User-Agent": agent
    }
    return headers

# page_headers = {
#     "Cookie": "JSESSIONID=ABAAABAAAGFABEF42BEF59E4399E6803A6C5828361037D8; _ga=GA1.2.2021525041.1533343081; user_trace_token=20180804083732-92e4f5d4-977e-11e8-b189-525400f775ce; LGUID=20180804083732-92e4f8db-977e-11e8-b189-525400f775ce; _gid=GA1.2.330084222.1533688355; index_location_city=%E5%85%A8%E5%9B%BD; TG-TRACK-CODE=search_code; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533819692,1533861545,1533861558,1533861568; LGSID=20180810101909-c3932359-9c43-11e8-a37b-5254005c3644; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533869874; LGRID=20180810105743-270542b3-9c49-11e8-a37b-5254005c3644; SEARCH_ID=24a7effd344f4e779fd8c91aa2b93e24",
#     "Host": "www.lagou.com",
#     "Origin": "https://www.lagou.com",
#     "Referer": "https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=",
#     "User-Agent": 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'
# }

def get_page_nums(url,pn=1,kd="数据分析"):
    page_data = {'first':'false','pn':pn,'kd': kd}
    page_headers = get_headers()
    html = requests.post(url+str(pn), data=page_data,headers=page_headers)
    page = json.loads(html.text)
    totalCount = page.get('content').get('positionResult').get('totalCount')
    pns = math.ceil(totalCount / 15)
    return pns,totalCount

def get_page_pagesize(url, pn, kd="数据分析"):  
    if pn == 1: 
        boo = 'true'
    else:
        boo = 'false'
    page_data = {'first':boo,'pn':pn,'kd': kd}
    page_headers = get_headers()
    html = requests.post(url+str(pn), data=page_data,headers=page_headers)
    html_text = html.text
    page = json.loads(html_text) 
    page_size = page.get('content').get('positionResult').get('resultSize')
    return page,page_size

def csv_writer_by_dict(csvfile,data):
    headers = ['companyId','createTime','companyShortName','positionAdvantage','salary','workYear','education','city', 'positionName','financeStage',\
    'industryField','jobNature','companySize','companyLabelList','district','positionLables','firstType','secondType','companyFullName']
    rows = data
    with open(csvfile, 'w', encoding='utf8') as f:
        writer = csv.DictWriter(f, headers)    #csv自带DictWriter方法
        writer.writeheader()                   #writeheader自带写入头部方法
        writer.writerows(rows)
        
if __name__ == '__main__':
    cityList = [u'上海',u'深圳',u'广州',u'杭州',u'成都',u'南京',u'武汉'] #选择部分城市进行分析
    for city in cityList:
        data = []
        url =  'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false&pn='.format(city) 
        items = ['companyId','createTime','companyShortName','positionAdvantage','salary','workYear','education','city', 'positionName','financeStage',\
         'industryField','jobNature','companySize','companyLabelList','district','positionLables','firstType','secondType','companyFullName'] #想抓取的岗位信息
        page_nums = get_page_nums(url)[0] #该城总页码数
        totalCount = get_page_nums(url)[1] #该城总岗位数
        print('---开始爬取%s市岗位信息，共计%d页，总岗位数%d---' % (city,page_nums,totalCount))
        for pn in range(1,page_nums+1):
            page_size = get_page_pagesize(url,pn)[1]
            print('---爬取%s市岗位信息，第%d页，岗位数%d---'  % (city,pn,page_size))
            for i in range(page_size):
                result = get_page_pagesize(url,pn)[0]['content']['positionResult']['result'][i]
                new_res = {key:value for key,value in result.items() if key in items}
                data.append(new_res)
            print('---成功爬取%s市岗位信息，第%d页，岗位数%d---'  % (city,pn,page_size))
            time.sleep(20)
        print('---成功爬取%s市岗位所有信息！---' % city)
        print(len(data))
        file_name = city + ".csv"
        csv_writer_by_dict(file_name,data)
    print('END!')
