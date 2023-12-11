import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#path = "C:/Users/Patryk/Documents/GitHub/interestnpy"
path = "C:/Users/rems9/Desktop/Travail/ENSAE/2A/projet_python/interestnpy"
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

#PART 2 - LOCAL TERRAIN PRICES

#LOADS CONVERSION TABLE REG - DEP
DEPREG_DF = pd.read_excel(path+"/data/external/GEOCOM/table-appartenance-geo-communes-19.xls", 
                          sheet_name="COM", skiprows=5)[['DEP', 'REG']].drop_duplicates()
DEPREG_DF['REG'] = DEPREG_DF['REG'].astype(str)

#LOADS REGIONAL PRICES FOR TERRAINS
TER_DF = pd.read_csv(path+"/data/external/TER/1-Terrains-achetes-nombre-surface-et-prix-moyen-par-region.2021-01.csv", 
                     delimiter=";", skiprows=1, escapechar='\\', skipinitialspace=True)

#CREATING ADDITIONAL CONSTANT VALUES FOR 2014, 2022, and 2023
additional_rows_2014 = TER_DF[TER_DF['ANNEE'] == 2015].copy()
additional_rows_2014['ANNEE'] = 2014
additional_rows_2022_2023 = TER_DF[TER_DF['ANNEE'] == 2021].copy()
additional_rows_2022_2023['ANNEE'] = 2022
additional_rows_2023 = additional_rows_2022_2023.copy()
additional_rows_2023['ANNEE'] = 2023
TER_DF = pd.concat([additional_rows_2014, TER_DF, additional_rows_2022_2023, additional_rows_2023]).sort_values('ANNEE')

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
