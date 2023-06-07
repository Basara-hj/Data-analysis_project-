import requests
from bs4 import BeautifulSoup
import kospi200
import csv

url = 'https://navercomp.wisereport.co.kr/v2/company/c1020001.aspx?cmp_cd={code}'
with open('./kospi200_sort.csv','w',encoding='utf-8',newline='') as fw:
    writer = csv.writer(fw)
    writer.writerow(['code','sort'])
    for code in kospi200.title_dict:
        target_url = url.format(code=code)
        resp = requests.get(target_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        table = soup.find('div', id='pArea')
        rows = table.find_all('tr')
        for row in rows:
            if not row.find('th', class_="c1 txt", scope="row"):
                continue
            if row.find('th', class_="c1 txt", scope="row").text == '계열':
                sort = row.find('td', class_="c2 txt").text.strip()
                writer.writerow([code,sort])
                
import pandas as pd

kospi = pd.read_csv('./kospi200.csv')
kospi_sort = pd.read_csv('./kospi200_sort.csv')
merge = pd.merge(kospi, kospi_sort, how='left', on='code')
merge.to_csv('./kospi200_last.csv',index=False)
