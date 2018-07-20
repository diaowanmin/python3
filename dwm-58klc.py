#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import urllib
import ssl
import csv

from urllib import request
from bs4 import BeautifulSoup


'''
提取58klc 项目数据
'''


class Extract:
    __url = ''
    __html = ''
    __data = []

    def __init__(self, url):
        self.__url = url

    def getData(self):
        self.__getHtml()
        self.__composingData()
        self.__writeCsv('./58klc.csv', self.__data)

    ''' 获取页面html '''
    def __getHtml(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
         #ssl创建未经验证的上下文
        context = ssl._create_unverified_context()
        request = urllib.request.Request(self.__url, headers=headers)
        response = urllib.request.urlopen(request, context=context)
        self.__html = response.read().decode('UTF-8')

    ''' 组装数据 '''
    def __composingData(self):
        soup = BeautifulSoup(self.__html, 'html.parser')

        #项目标题
        projectTitles = soup.find_all(name='div', attrs=('class', 'project-title'))

        #历史收益
        historicalIncomes = []
        yearMoneys = soup.find_all(name='div', attrs=('class', 'year-money'))
        for yearMoney in yearMoneys:
            ps = yearMoney.find_all('p')
            historicalIncomes.append(ps[1])

        #项目期限、总额
        projectDurations = []
        projectTotalPrices = [] 
        projectDays = soup.find_all(name='div', attrs=('class', 'project-day'))
        for projectDay in projectDays:
            spans = projectDay.find_all('span')
            projectDurations.append(spans[0])
            projectTotalPrices.append(spans[2])

        #进度、金额
        progresss = []
        prices = []
        klcInvestItems = soup.find_all(name='div', attrs=('class', 'klc-invest-item'))
        for klcInvestItem in klcInvestItems:
            spans = klcInvestItem.find_all('span')
            progresss.append(spans[-1])
            prices.append(spans[-2])

        #状态
        buyButtons = soup.find_all(name='div', attrs=('class', 'buy-button'))

        #组装数据
        i = 0
        for projectTitle in projectTitles:
            ds = [
                projectTitle.text.replace(' ', ''),
                historicalIncomes[i].text.replace(' ', ''),
                projectDurations[i].text.replace(' ', ''),
                projectTotalPrices[i].text.replace(' ', ''),
                progresss[i].text.replace(' ', ''),
                prices[i].text.replace(' ', ''),
                buyButtons[i].text.replace(' ', '')
            ]
            self.__data.append(ds)
            i += 1

    ''' 写入csv '''
    def __writeCsv(
        self,
        path = './58klc.csv', 
        data = [],
        head = ['项目名称', '历史收益', '项目期限', '项目金额', '项目进度', '投资金额/项目金额', '项目状态']):
        try:
            with open(path, 'w', newline='', encoding='utf-8-sig') as csv_file:  
                writer = csv.writer(csv_file, dialect='excel')  
  
                if head is not None:  
                    writer.writerow(head)  
    
                for row in data:  
                    writer.writerow(row)  
  
                print("Write a CSV file to path %s Successful." % path)  
        except Exception as e:
            print("Write an CSV file to path: %s, Case: %s" % (path, e))

url = 'https://www.58klc.com/'
e = Extract(url)
e.getData()