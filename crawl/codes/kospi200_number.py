import requests
import csv
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/sise/sise_index_day.naver?code=KPI200&page={page}'

with open('./kospi200_numbers.csv','w',encoding='utf-8',newline='') as fw:
    writer = csv.writer(fw)
    writer.writerow(['date','kospi200'])
    for i in range(1,139+1): # 날짜에 따라 변화 필요
        target_url = url.format(page=str(i))
        resp = requests.get(target_url, headers={'User-agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', class_='type_1')
        rows = table.find_all('tr')
        for i in range(2,11+1):
            if not rows[i].find('td',class_='date'):
                continue
            date = rows[i].find('td',class_='date').text
            if date > '2023.05.31' or date < '2020.01.20':
                continue
            date = datetime.strptime(date, '%Y.%m.%d').date()
            number = rows[i].find('td',class_='number_1').text
            writer.writerow([date, number])
            
df = pd.read_csv('./kospi200_number.csv')
df = df.sort_values('date', ascending=True)
df.to_csv('./kospi200_numbers.csv', index=False)
