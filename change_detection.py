


import pandas as pd

df1 = pd.read_csv('data/01_05.csv')
df2 = pd.read_csv('01_05_decible_vh.csv')

# first focus on VH pre and post flood values
# filter data based on if post flood decible appears to be water 

df1
df2

df2.rename(columns={'postflood_vh': 'postflood_vh_decible', 'preflood_vh': 'preflood_vh_decible'}, inplace=True)
df2

df1 = df1.drop('Unnamed: 0', axis=1)
df2 = df2.drop('Unnamed: 0', axis=1)

df = pd.merge(df1,df2, on=['y', 'x'], how='inner')
df

df_filter = df[df['postflood_vh_decible']<=-16]
df_filter

df_filter['change'] = df_filter['preflood_vh_decible'] - df_filter['postflood_vh_decible']
df_filter['change_2'] = df_filter['change'].mul(-1)

df_filter

df_filter.to_csv('change_01_05_decible.csv')
df

df[df['postflood_vh']== 30]

df[df['postflood_vh']== 35]

df[df['postflood_vh']== 100]

df[df['postflood_vh']== 0]

df[df['postflood_vh']== 255]