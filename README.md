# COVID-19-analysis

## Some basic analysis and simple predictions on the COVID-19 data in Canada
- Data source: https://docs.google.com/spreadsheets/d/1PjkemMdFSZgA-M8Esr6rbNjHiyfcXcBxPeMjselJIso/edit#gid=669830005
- Table of Content (An overview of the project):
  - Import the data and conduct data cleaning:
  ```python
  def data_cleaning(data):
    data.rename(columns={c: repl(c.strip()) for c in data.columns}, inplace=True)
    del data['province']
    del data['last_updated']
    data = data.set_index('date')
    return data.dropna()
  
  def repl(name):
    match = re.search('(^data » )([\w]*)', name)
    return match.group(2) if match else name
    
  national = data_cleaning(pd.read_excel(link, sheet_name='National'))
  ```
  
  - Prediction: Poisson regression on the data of the entire country:
  
  ```python
  ds = national.index.to_series()
  national['MONTH'] = ds.dt.month
  national['DAY_OF_WEEK'] = ds.dt.dayofweek
  national['DAY'] = ds.dt.day
  formula = """change_cases ~ DAY + DAY_OF_WEEK + MONTH + change_vaccinated + change_tests"""
  y, X = dmatrices(formula, national, return_type='dataframe')
  poisson_reg = sm.GLM(y, X, family=sm.families.Poisson()).fit()
  ```
  
  - Comparison across different states
  - [Code](covid-19_ca.py)
  - Results and graphs:
  
  <img src="Poisson.png" alt="Poisson regression"/>
   
