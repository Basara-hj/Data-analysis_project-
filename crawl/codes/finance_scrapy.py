import scrapy
import re
import csv
from datetime import datetime
from bs4 import BeautifulSoup

class FinanceSpider(scrapy.Spider):
    name = "finance"
    start_urls = ["https://finance.naver.com/"]

    def __init__(self):
        self.kospi200_url = 'https://finance.naver.com/sise/entryJongmok.naver?&page={page}'
        self.sise_day_url = 'https://finance.naver.com/item/sise_day.naver?code={code}&page={page}'
        self.code = ''
        self.rows_list = []
        self.output_file = open("./finance_scrapy.csv", "w", encoding='utf-8', newline='')
        self.writer = csv.writer(self.output_file)
        self.writer.writerow(['name', 'date', 'jong_ga', 'si_ga', 'go_ga', 'jeo_ga', 'geo_rae_ryang'])

    def parse(self, response):
        for i in range(1, 20+1):
            target_url = self.kospi200_url.format(page=i)

            req = scrapy.Request(
                url=target_url,
                callback=self.parse_kospi_200
            )
            yield req

    def parse_kospi_200(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='type_1')
        tags = table.find_all('a', target='_parent')

        pattern = f'\d+'
        for tag in tags:
            code = re.findall(pattern, str(tag))
            name = tag.get_text()

            for page in range(1, 85+1):
                # 불러오기
                target_url = self.sise_day_url.format(code=code[0], page=page)

                req = scrapy.Request(
                    url=target_url,
                    headers={'User-agent': 'Mozilla/5.0'},
                    callback=self.parse_semi,
                    cb_kwargs={'name': name}
                )
                yield req

    def parse_semi(self, response, name):
        soup = BeautifulSoup(response.text, 'lxml')
        rows = soup.find_all('tr')

        # 행
        for i in range(len(rows)):
            row_temp = []

            # name, date
            date = rows[i].find('td', align="center")
            if not date:
                continue
            pattern = r'\d{4}\.\d{2}\.\d{2}'
            match = re.search(pattern, str(date))
            date_match = datetime.strptime(match.group(), "%Y.%m.%d").date()
            min_date = datetime.strptime('2020.01.20', "%Y.%m.%d").date()
            max_date = datetime.strptime('2023.05.31', "%Y.%m.%d").date()
            if date_match < min_date or date_match > max_date:
                continue
            row_temp.append(name)
            row_temp.append(date_match)

            # 주식
            numbers = rows[i].find_all('td', class_='num')
            pattern = r','
            for j in range(len(numbers)):
                if j == 1:
                    continue
                number = numbers[j].get_text().strip()
                new_number = int(re.sub(pattern, '', number))
                row_temp.append(new_number)

            self.rows_list.append(row_temp)

        self.writer.writerows(self.rows_list)
        self.rows_list = []