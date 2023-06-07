#코로나 확진자수 데이터 가져오기

from tqdm import tqdm
import requests
import json

year_ls = []
male_ls = []
female_ls = []
year_ls_f = []

for j in tqdm(range(1, 32)):
    covid_url = "http://apis.data.go.kr/1352000/ODMS_COVID_05/callCovid05Api?serviceKey=&apiType=JSON&pageNo=" + str(j)
    resq = requests.get(covid_url)
    data = resq.json()
    covid_list = data["items"]

    for item in covid_list:
        if item["gubun"] == "남성":
            year = item["createDt"]
            if year not in year_ls:
                year_ls.append(year)
                male = item["confCase"]
                male_ls.append(male)

        if item["gubun"] == "여성":
            year_f = item["createDt"]
            if year_f not in year_ls_f:
                year_ls_f.append(year_f)
                female = item["confCase"]
                female_ls.append(female)
                
#날짜, 남자 누적 확진자 수, 남자 일일 확진자 수 파일 생성
import pandas as pd

df1 = pd.DataFrame({'year': year_ls, 'male': male_ls})
df1 = df1.sort_values(by='year', ascending=True)
# df1 = df1.drop_duplicates(subset=['year'], keep='first')

df1['male'] = df1['male'].astype(int)
df1['male_diff'] = df1['male'].diff()
df1['male_diff'] = df1['male_diff'].fillna(0)
df1.to_csv('./male_data19.csv', index=False)

#날짜, 여자 누적 확진자 수, 여자 일일 확진자 수 파일 생성
df2 = pd.DataFrame({'year2': year_ls_f, 'female': female_ls})
df2 = df2.sort_values(by='year2', ascending=True)
# df2 = df2.drop_duplicates(subset=['year2'], keep='first')  # Remove duplicate rows based on 'year2' column

df2['female'] = df2['female'].astype(int)
df2['female_diff'] = df2['female'].diff()
df2['female_diff'] = df2['female_diff'].fillna(0)

df2.to_csv('./female_data19.csv', index=False)

#날짜, 남자 일일 확진자 수, 여자 일일 확진자 수, 총 일일 확진자 수 파일 생성
merged_df = pd.merge(df1, df2, left_on='year', right_on='year2', how='inner')
merged_df = merged_df.drop(['male', 'female', 'year2'], axis=1)
merged_df = merged_df.assign(total=merged_df['male_diff'] + merged_df['female_diff'])
merged_df.rename(columns={'year':'date','male_diff':'male','female_diff':'female'}, inplace=True)
merged_df['male'] = merged_df['male'].astype(int)
merged_df['female'] = merged_df['female'].astype(int)
merged_df['total'] = merged_df['total'].astype(int)
merged_df = merged_df[merged_df['date'] <= '2023-05-31']
merged_df.to_csv('./covid19_daily.csv', index=False)
