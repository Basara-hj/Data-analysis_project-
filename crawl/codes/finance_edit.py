import pandas as pd

df1 = pd.read_csv('./finance_scrapy.csv')
df2 = pd.read_csv('./kospi200.csv')
df = pd.merge(df1, df2, how='left', on='name')
df = df.sort_values(['rank','date']).iloc[:,:7]
df = df.reset_index(drop=True)
df = df.rename_axis('id')
df.to_csv('./finance.csv',index=True)
