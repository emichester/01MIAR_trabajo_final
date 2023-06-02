import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime


def clean_input_df(df: pd.DataFrame)-> tuple:
    df[['Serial Number', 'List Year']]= df[['Serial Number', 'List Year']].astype(int)
    df[['Assessed Value', 'Sale Amount', 'Sales Ratio']]= df[['Assessed Value', 'Sale Amount', 'Sales Ratio']].astype(float)
    df= df[df['Date Recorded'].apply(lambda x: len(x)) == 10]


    df['year']= df['Date Recorded'].apply(lambda x: x[6:])
    df['month']= df['Date Recorded'].apply(lambda x: x[3:5])
    df['day']= df['Date Recorded'].apply(lambda x: x[:2])
    df= df[(df['month'].astype(int) <= 12) & (df['day'].astype(int) != 0)]
    df['is_weekend']= df[['year', 'month', 'day']].astype(int).apply(lambda x: datetime.date(*x.values.tolist()).weekday(), axis=1)
    df['is_weekend']= df['is_weekend'].apply(lambda x: 1 if x in (6, 7) else 0)

    df['year_and_month']= df['year'] + '/' + df['month']

    df_sales_stat= pd.DataFrame(df[['year_and_month', 'Sale Amount']].groupby('year_and_month').mean()['Sale Amount'])
    df['Date Recorded']= pd.to_datetime(df['Date Recorded'])
    df.sort_values(by= 'Date Recorded', ascending= True, inplace= True)
    df['Street']= df['Address'].apply(lambda x: ' '.join(x.split(' ')[1:]))

    return df, df_sales_stat