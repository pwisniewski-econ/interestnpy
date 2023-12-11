#Investigating NaN for CODGEO

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

path = "C:/Users/rems9/Desktop/Travail/ENSAE/2A/projet_python/interestnpy"
#CHANGE PATH AS NEEDED
#year="2019"
years = ["2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014"]

   

TERDEP_DF = pd.read_feather(path+"/data/interim/terrains_py.feather")
IDENT_DF = pd.read_feather(path+"/data/interim/tble_de_passage_py.feather").drop_duplicates()


#This a troncated version of the immo_prices function (see the agreg.py file for the full version) to search for nan in CODGEO
def NaNimmo_prices(year):
  # Read data
  df = pd.read_csv(path+f"/data/external/DFV/valeursfoncieres-{year}.txt", delimiter="|", dtype=str)
  df = df.dropna(axis=1, how='all')  
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
  IDENT_YEAR_DF = IDENT_DF[['COM', 'EPCI', 'ZE', 'LIB_COM', 'LIB_EPCI', 'LIB_ZE', f'CODGEO_{year}']].drop_duplicates()
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
  df = df.drop_duplicates(subset=['Date mutation', 'No voie', 'Valeur fonciere', 'Surface terrain', 'LIB_COM'])
  return df





CODGEO_year = [(lambda x : "CODGEO_" +x)(x)for x in years]
nan_years = [(lambda x : "nan_" +x)(x)for x in years]
dataframes= {} #this dictionnary will store dataframes with 2 columns : Commune and the number of nan for codgeo in the commune for a specific year

for i in nan_years:
    nan_year = i
    df = NaNimmo_prices(nan_year[4:8])
    i = df[["Commune","CODGEO_" + nan_year[4:8]]]
    i = i[pd.isna(i["CODGEO_" + nan_year[4:8]])==True] #keeping only lines with na for codgeo
    i = i[["Commune"]].value_counts() #counts the number of nan for each commune
    #i.columns = ["Commune", nan_year[4:8] + "Number_NaN"]
    t= nan_year[4:8] + "_Number_NaN"
    dataframes[nan_year] = i #put the dataframe in the dictionnary


for z in dataframes:
   print(f"Number of commune with nan for CODGEO in {z[4:8]} : {dataframes[z].size}, total number transactions with nan for CODGEO this year : {sum(dataframes[z][:])}")


#for z in dataframes:
   #print(dataframes[z]) #print commune and associated number of nan for codgeo for each year


