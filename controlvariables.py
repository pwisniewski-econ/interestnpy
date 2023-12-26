import pandas as pd
import numpy as np
import pyarrow.feather as feather

#CHANGE PATH AS NEEDED
path = "C:/Users/rems9/Desktop/Travail/ENSAE/2A/projet_python/interestnpy"

#IMPORT UNEMPLOYMENT DATA
#source https://www.insee.fr/fr/statistiques/1893230
unemployement = pd.read_excel(path+"/data/external/unemployment/chomage-zone-t1-2003-t3-2023.xlsx", 
                               sheet_name="txcho_ze", skiprows=5)



#IMPORT AVAILABLE INCOME DATA  
#source https://www.insee.fr/fr/statistiques/3126151
#source https://www.insee.fr/fr/statistiques/6036907

income2014 = pd.read_excel(path+"/data/external/revenus/indic-struct-distrib-revenu-2014-COMMUNES/indic-struct-distrib-revenu-2014-COMMUNES/FILO_DISP_COM.xls", 
                               sheet_name="ENSEMBLE", skiprows=5)

income2019 = pd.read_excel(path+"/data/external/revenus/indic-struct-distrib-revenu-2019-COMMUNES/FILO2019_DISP_COM.xlsx", 
                               sheet_name="ENSEMBLE", skiprows=5)

#MERGE 
income2014_2019 = pd.merge(income2014, income2019, how='inner', on = ["CODGEO","LIBGEO"])

#Keep CODGEO, LIBGEO , quartiles and Gini 
income2014_2019 = income2014_2019[["CODGEO","LIBGEO","Q114","Q214","Q314","GI14","Q119","Q219","Q319","GI19"]]

#ADD column Mediane_evol_diff to observe the evolution of available income between 2019 and 2019
income2014_2019["Mediane_evol_diff"] = income2014_2019["Q219"] - income2014_2019["Q214"]


#IMPORT POPULATION DENSITY

