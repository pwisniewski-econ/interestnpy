import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

path = "C:/Users/patry/Documents/GitHub/interestnpy"
#CHANGE PATH AS NEEDED

#PART 1 - TRANSLATION TABLE:

#IMPORTS AND FILTER INSEE TRANSLATION TABLE
PASSAGE1423_DF = pd.read_excel(path+"/data/external/GEOCOM/table_passage_annuelle_2023.xlsx", 
                               sheet_name="COM", skiprows=5)
PASSAGE1423_DF = PASSAGE1423_DF.filter(regex='^CODGEO').iloc[:, :10]
PASSAGE1423_DF = PASSAGE1423_DF[PASSAGE1423_DF['CODGEO_2023'].notna()]

#IMPORTS 2023 EPCI DEFINITIONS
FCOM_DF = pd.read_excel(path+"/data/external/GEOCOM/ZE2020_au_01-01-2023.xlsx", 
                            sheet_name="Composition_communale", skiprows=5)

EPC_COM = pd.read_excel(path+"/data/external/GEOCOM/Intercommunalite_Metropole_au_01-01-2023.xlsx", 
                            sheet_name="Composition_communale", skiprows=5)

FCOM_DF = pd.merge(FCOM_DF, EPC_COM, how='left', on=['CODGEO','LIBGEO', 'DEP', 'REG'])

#CREATES COM BASED ON 2023 TOWN CODES AND ZE BASED ON EPCI
FCOM_DF['COM'] = FCOM_DF['CODGEO']
FCOM_DF['LIB_COM'] = FCOM_DF['LIBGEO']
FCOM_DF['ZE'] = FCOM_DF['ZE2020']
FCOM_DF['LIB_ZE'] = FCOM_DF['LIBZE2020']
FCOM_DF['EPCI'] = FCOM_DF['ZE2020']
FCOM_DF['LIB_ZE'] = FCOM_DF['LIBZE2020']
FCOM_DF['EPCI'] = FCOM_DF.apply(
    lambda row: row['CODGEO'] if any(x in row['LIBEPCI'] for x in ["Métropole du Grand Paris", "Métropole de Lyon", "Métropole d'Aix-Marseille-Provence"]) else row['EPCI'],
    axis=1
)
FCOM_DF['LIB_EPCI'] = FCOM_DF.apply(
    lambda row: row['LIBGEO'] if any(x in row['LIBEPCI'] for x in ["Métropole du Grand Paris", "Métropole de Lyon", "Métropole d'Aix-Marseille-Provence"]) else row['LIBEPCI'],
    axis=1
)
FCOM_DF['LIB_EPCI'] = FCOM_DF.apply(
    lambda row: "Iles-FR" if row['EPCI'] == "ZZZZZZZZZ" else row['LIB_EPCI'],
    axis=1
)
FCOM_DF.rename(columns={'CODGEO': 'CODGEO_2023'}, inplace=True)
FCOM_DF = FCOM_DF[['CODGEO_2023', 'COM', 'LIB_COM', 'ZE', 'LIB_ZE', 'EPCI', 'LIB_EPCI']]

#MERGES WITH INSEE TABLE TO CREATE THE TRANSLATION TABLE 
IDENT1423_DF = pd.merge(PASSAGE1423_DF, FCOM_DF, how='left', on='CODGEO_2023')

#FIXES PROBLEMS RELATED TO CITIES WITH "ARRONDISSEMENTS"
conditions_arr = [
    IDENT1423_DF['CODGEO_2023'].str.startswith("75"),
    IDENT1423_DF['CODGEO_2023'].str.startswith("132"),
    IDENT1423_DF['CODGEO_2023'].str.startswith("6938")
]

ze_arr = [1109, 9312, 8421]
lib_arr = ["Paris", "Marseille", "Lyon"]

IDENT1423_DF['COM'] = IDENT1423_DF.apply(
    lambda row: row['CODGEO_2023'] if pd.isna(row['COM']) else row['COM'],
    axis=1
)

IDENT1423_DF['EPCI'] = IDENT1423_DF.apply(
    lambda row: row['CODGEO_2023'] if pd.isna(row['EPCI']) else row['EPCI'],
    axis=1
)

IDENT1423_DF['ZE'] = np.select(
  conditions_arr, 
  ze_arr, 
  default=IDENT1423_DF['ZE'])

def create_lib_ident(row, col_name):
    if pd.isna(row[col_name]):
        if row['COM'][:2] == "75":
            return f"Paris {row['COM'][3:5]}"
        elif row['COM'][:2] == "69":
            return f"Lyon {int(row['CODGEO_2019']) - 80}"
        elif row['COM'][:2] == "13":
            return f"Marseille {row['COM'][3:5]}"
    else:
        return row[col_name]

IDENT1423_DF['LIB_COM'] = IDENT1423_DF.apply(create_lib_ident, col_name='LIB_COM', axis=1)

IDENT1423_DF['LIB_EPCI'] = IDENT1423_DF.apply(
    lambda row: row['LIB_COM'] if pd.isna(row['LIB_EPCI']) else row['LIB_EPCI'],
    axis=1
)

IDENT1423_DF['EPCI'] = IDENT1423_DF['EPCI'].astype(str) 

IDENT1423_DF['LIB_ZE'] = np.select(
  conditions_arr, 
  lib_arr, 
  default=IDENT1423_DF['LIB_ZE'])


#REORDERS AND EXPORTS THE TRANSLATION TABLE
reord_cols = ['COM', 'ZE', 'LIB_COM', 'LIB_ZE', 'EPCI', 'LIB_EPCI']
IDENT1423_DF = IDENT1423_DF[reord_cols + [col for col in IDENT1423_DF.columns if col not in reord_cols]]
IDENT1423_DF.to_feather(path+"/data/interim/tble_de_passage_py.feather")

#PART 2 - LOCAL LAND PRICES

#LOADS CONVERSION TABLE REG - DEP
DEPREG_DF = pd.read_excel(path+"/data/external/GEOCOM/table-appartenance-geo-communes-19.xls", 
                          sheet_name="COM", skiprows=5)[['DEP', 'REG']].drop_duplicates()
DEPREG_DF['REG'] = DEPREG_DF['REG'].astype(str)

#LOADS REGIONAL PRICES FOR LAND
TER_DF = pd.read_csv(path+"/data/external/TER/1-Terrains-achetes-nombre-surface-et-prix-moyen-par-region.2022-01.csv", 
                     delimiter=";", skiprows=1, escapechar='\\', skipinitialspace=True)

#CREATING ADDITIONAL CONSTANT VALUES FOR 2023
additional_rows_2023 = TER_DF[TER_DF['ANNEE'] == 2022].copy()
additional_rows_2023['ANNEE'] = 2023
TER_DF = pd.concat([additional_rows_2014, TER_DF, additional_rows_2023]).sort_values('ANNEE')
TER_DF = TER_DF[TER_DF['ANNEE'] > 2013]

#MERGES TO GO FROM REGIONAL LEVEL TO DEPARTMENT LEVEL AND EXPORTS
TERDEP_DF = pd.merge(DEPREG_DF, TER_DF, left_on='REG', right_on='ZONE_CODE', how='left')
TERDEP_DF = TERDEP_DF.dropna().reset_index(drop=True)[['ANNEE', 'DEP', 'PTM2_MED']]
TERDEP_DF.to_feather(path+"/data/interim/terrains_py.feather")

#PLOT TO SEE REGIONAL RESULTS (to delete?)
sns.lineplot(data=TER_DF, x='ANNEE', y='PTM2_MED', hue='ZONE_LIBELLE')
plt.title("Terrain prices per region")
plt.xlabel("Quarter")
plt.ylabel("")
plt.legend(title="Region")
plt.show()

#INFLATION TABLE
inflation = pd.read_excel(path+"/data/external/INFLATION/econ-gen-taux-inflation.xlsx", 
                          sheet_name="Données", skiprows=3, nrows=9)
inflation.rename(columns={"Année": "AN", "Taux d'inflation": "INFLATION"}, inplace=True)
inflation['AN'] = inflation['AN'].astype(str)
inflation = inflation._append({'AN': str(2023), 'INFLATION': 2.3}, ignore_index=True)
#Why 2.3? first 3 months inflation
#either way it does not matter as we will work in basis 2023
inflation.sort_values(by="AN", inplace=True)
inflation['Date'] = inflation['AN']+"0101"
inflation.loc[len(inflation)] = ["2023",0, "20230401"]
inflation['TOT'] = (1 + inflation['INFLATION'].shift(1) / 100).cumprod()
inflation['TOT'] = inflation['TOT'].fillna(1)

# INTEREST RATES TABLE
interest_rates = pd.read_excel(path+"/data/external/INFLATION/series_panorama_202309.xlsx", 
                               sheet_name="G3", 
                               skiprows=6, 
                               names=["Date", "ir", "ir10_avg", "ir20_avg"])

interest_rates = interest_rates[interest_rates['Date'] > '2013-12-31']

interest_rates['quarter'] = interest_rates['Date'].dt.to_period('Q').astype(str)
interest_rates = interest_rates.groupby('quarter').agg({'ir': 'mean'}).reset_index()

def get_month_from_quarter(quarter):
    quarter_num = quarter.split("Q")[1]
    return {'1': '01', '2': '04', '3': '07', '4': '10'}.get(quarter_num, None)

interest_rates['themonth'] = interest_rates['quarter'].apply(get_month_from_quarter)
interest_rates['Date'] = (interest_rates['quarter'].str[:4] + interest_rates['themonth'] + "01")
interest_rates = interest_rates[['Date', 'ir']]

# Combine inflation and interest rates
irflation = pd.merge(interest_rates, inflation, on='Date', how='left')
irflation = irflation.interpolate(method="slinear", fill_value="extrapolate", limit_direction="both")
irflation['BASE14'] = irflation['TOT'] / irflation['TOT'].iloc[0]
irflation['BASE23'] = irflation['BASE14'] / irflation['BASE14'].iloc[37]
irflation.to_feather(path+"/data/interim/irflation.feather")

