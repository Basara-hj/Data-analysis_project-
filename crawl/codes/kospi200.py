import requests
import re
import csv
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/sise/entryJongmok.naver?&page={page}'
industry_url = 'https://finance.naver.com/item/main.naver?code={code}'
title_dict = {}
count = 1

with open('./kospi200.csv','w',encoding='utf-8',newline='') as fw:
    writer = csv.writer(fw)
    writer.writerow(['name','code','rank','industry'])
    for i in range(1,20+1):
        target_url = url.format(page=i)
        resp = requests.get(target_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', class_='type_1')
        names = table.find_all('a', target='_parent')

        pattern = f'\d+'

        for i in range(len(names)):
            name = names[i].get_text()
            code = re.findall(pattern, str(names[i]))
            
            target_url = industry_url.format(code=code[0])
            resp = requests.get(target_url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            upjong = soup.find('h4', class_="h_sub sub_tit7")
            industry = upjong.find('a').get_text()
            
            title_dict[code[0]] = [name, count, industry]
            writer.writerow([name, code[0], count, industry])
            count += 1
