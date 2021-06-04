import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import statsmodels.api as sm 
from patsy import dmatrices

link = '/Users/yangzixuan/Desktop/source_file/COVID-19 Analysis/COVID19Tracker.ca Data.xlsx'

def repl(name):
    match = re.search('(^data » )([\w]*)', name)
    return match.group(2) if match else name

def data_cleaning(data):
    data.rename(columns={c: repl(c.strip()) for c in data.columns}, inplace=True)
    del data['province']
    del data['last_updated']
    data = data.set_index('date')
    return data.dropna()



national = data_cleaning(pd.read_excel(link, sheet_name='National'))
print(national.head())

ds = national.index.to_series()
national['MONTH'] = ds.dt.month
national['DAY_OF_WEEK'] = ds.dt.dayofweek
national['DAY'] = ds.dt.day
formula = """change_cases ~ DAY + DAY_OF_WEEK + MONTH + change_vaccinated + change_tests"""
y, X = dmatrices(formula, national, return_type='dataframe')
poisson_reg = sm.GLM(y, X, family=sm.families.Poisson()).fit()
predict = poisson_reg.get_prediction(X)
prediction_summary_frame = predict.summary_frame()
print(prediction_summary_frame)
predict_counts = prediction_summary_frame['mean']
fig, ax = plt.subplots()
ax.plot(X.index, predict_counts, label='prediction')
ax.plot(X.index, national['change_cases'], label='actual')
ax.set_title('actual vs. prediction')
ax.legend()
plt.show()



ON = data_cleaning(pd.read_excel(link, sheet_name='ON'))
QC = data_cleaning(pd.read_excel(link, sheet_name='QC'))
BC = data_cleaning(pd.read_excel(link, sheet_name='BC'))
AB = data_cleaning(pd.read_excel(link, sheet_name='AB'))