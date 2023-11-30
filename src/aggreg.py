import pandas as pd
import numpy as np
import pyarrow.feather as feather

path = "C:/Users/Patryk/Documents/GitHub/interestnpy"

TERDEP_DF = pd.read_feather(path+"/data/interim/terrains_py.feather")
IDENT_DF = pd.read_feather(path+"/data/interim/tble_de_passage_py.feather").drop_duplicates()

def aggreg_fun(data, ID, LIB_ID):
  quantiles = data.groupby([ID, LIB_ID, 'Date', 'Type local'])['prixM2'].quantile([0.05, 0.95]).unstack()
  quantiles.columns = ['quantile_05', 'quantile_95']
  data = data.merge(quantiles, left_on=[ID, LIB_ID, 'Date', 'Type local'], right_index=True)
  filtered_data = data[(data['prixM2'] <= data['quantile_95']) & (data['prixM2'] >= data['quantile_05'])]
  print("filtered!")
  # Further aggregation
  data_agreg = filtered_data.groupby([ID, LIB_ID,'Date']).agg(
     n_transactions=('prixM2', 'size'),
     prop_maison=('Type local', lambda x: np.mean(x == 'Maison')),
    prixM2=('prixM2', 'median')
  ).reset_index()
  return data_agreg
  
def immo_prices(year):
  # Read data
  df = pd.read_csv(path+f"/data/external/DFV/valeursfoncieres-{year}.txt", delimiter="|", dtype=str)
  df = df.dropna(axis=1, how='all')  # Equivalent to select_if in R

  # Filter and mutate
  df = df[df['Nature mutation'] == "Vente"]
  df = df[df['Code type local'].isin(['1', '2'])]
  df = df[~df['Code departement'].isin(['971', '972', '973', '974'])]
  df['Code commune'] = df['Code commune'].str.pad(width=3, side='left', fillchar='0')
  df['depcom'] = df['Code departement'] + df['Code commune']
  df['Valeur fonciere'] = df['Valeur fonciere'].str.replace(",", ".").astype(float)
  print("ok-1")
  # Quarter and date manipulation
  df['quarter_num'] = df['Date mutation'].str[3:5].astype(int)
  df['qmonth'] = np.select([df['quarter_num'].isin(range(1, 4)), df['quarter_num'].isin(range(4, 7)), df['quarter_num'].isin(range(7, 10)), df['quarter_num'].isin(range(10, 13))], ["01", "01", "07", "07"], default=np.nan)
  df['Date'] = pd.to_datetime(str(year) + df['qmonth'] + "01", format='%Y%m%d')
  print("ok-2")
  # Merging with IDENT_YEAR_DF
  IDENT_YEAR_DF = IDENT_DF[['IDENT', 'IDENT_ROBUST', 'LIB_IDENT', 'LIB_IDENT_ROBUST', f'CODGEO_{year}']].drop_duplicates()
  df = df.merge(IDENT_YEAR_DF, left_on='depcom', right_on=f'CODGEO_{year}', how='left')
  print("ok-3")
  # Merging with TERDEP_DF
  df = df.merge(TERDEP_DF[TERDEP_DF['ANNEE'] == int(year)], left_on='Code departement', right_on='DEP', how='left')
  print("ok-4")
  # Calculating prixM2
  df['Surface terrain'] = df['Surface terrain'].replace(np.nan, 0).astype(float)
  df['prixM2'] = (df['Valeur fonciere'] - df['Surface terrain'] * df['PTM2_MED']) / df['Surface reelle bati'].astype(float)
  df = df[(df['prixM2'] > 10) & (df['prixM2'] < 100000)].drop_duplicates()
  print("ok-5")
  # Further processing
  df = df.drop_duplicates(subset=['Date mutation', 'No voie', 'Valeur fonciere', 'Surface terrain', 'LIB_IDENT'])
  df4_robust = aggreg_fun(df,"IDENT_ROBUST","LIB_IDENT_ROBUST")
  print("ok-6")
  df4 = aggreg_fun(df,"IDENT", "LIB_IDENT")
  print("ok-7")

  return [df4, df4_robust]


years = ["2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014"]
results = []

for i in years:
  results.append(immo_prices(i))

# Merging results
IMMO1423 = pd.concat([result[0] for result in results])
IMMO1423_robust = pd.concat([result[1] for result in results])
  
# Writing output
feather.write_feather(IMMO1423, path+"/data/interim/immo_panel_py.feather")
feather.write_feather(IMMO1423_robust, path+"/data/interim/immo_panel_robust_py.feather")
