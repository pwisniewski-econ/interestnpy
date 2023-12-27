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
income2014_2019["CODGEO"] = income2014_2019["CODGEO"].astype(str) #preventive bug correction

#IMPORT POPULATION AND SURFACE
#source https://www.insee.fr/fr/statistiques/3698339
#source https://www.insee.fr/fr/statistiques/2521169
population = pd.read_excel(path+"/data/external/pop_density/base-pop-historiques-1876-2020.xlsx", 
                               sheet_name="pop_1876_2020", skiprows=5)
population = population[["CODGEO","PMUN14","PMUN19"]]


surface = pd.read_excel(path+"/data/external/pop_density/base_cc_comparateur.xlsx",sheet_name="COM",skiprows=5) #IF NOT RUNNING SAVE THE EXCEL FILE AND IT WILL WORK
surface = surface[["CODGEO","SUPERF"]]
surface["CODGEO"] = surface["CODGEO"].astype(str) #bug correction
#MERGE
densite = pd.merge(population,surface,how="inner",on=["CODGEO"])

#create popdensity2014 and popdensity2019 : population/surface
densite["popdensity2014"] = densite["PMUN14"] / densite["SUPERF"]
densite["popdensity2019"] = densite["PMUN19"] / densite["SUPERF"]
densite = densite[["CODGEO","popdensity2014","popdensity2019"]]
densite["CODGEO"] = densite["CODGEO"].astype(str) #preventive bug correction


#MERGE INCOME2014_2019 AND DENSITE
control_var = pd.merge(income2014_2019,densite,how="inner",on=["CODGEO"])


#IMPORT PHYSICISTS accessibility
#source https://data.drees.solidarites-sante.gouv.fr/explore/dataset/530_l-accessibilite-potentielle-localisee-apl/information/
physicist = pd.read_excel(path+"/data/external/physicist/Indicateur d'accessibilité potentielle localisée (APL) aux médecins généralistes.xlsx",sheet_name="APL_2019", skiprows=8)
physicist= physicist[["Code commune INSEE","APL aux médecins généralistes de moins de 65 ans"]]
#renaming variables 
physicist = physicist.rename(columns ={"Code commune INSEE": "CODGEO", "APL aux médecins généralistes de moins de 65 ans" : "Physicist_access"})

#MERGE
control_var = pd.merge(control_var,physicist,how="inner",on="CODGEO")

#IMPORT CRIMINALITY
#source https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-et-departementale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/#/resources
criminality = pd.read_csv(path+"/data/external/criminality/donnee-data.gouv-2022-geographie2023-produit-le2023-07-17.csv",sep=";")
criminality = criminality.rename(columns = {"CODGEO_2023":"CODGEO"})
#For year 2019
criminality19 = criminality[criminality["annee"].isin([19])]

burglary19 = criminality19[criminality19["classe"].isin(["Cambriolages de logement"])] #around 70% of Nan in the column tauxpourmille
burglary19 = burglary19[["CODGEO","tauxpourmille"]]
burglary19 = burglary19.rename(columns = {"tauxpourmille":"burglary_for_1000"})


otherassault19 = criminality19[criminality19["classe"].isin(["Autres coups et blessures volontaires"])] #around 45% of Nan in the column faits (number of occurence)
otherassault19= otherassault19[["CODGEO","faits"]]
otherassault19 = otherassault19.rename(columns = {"faits":"other_assault"})

assault19 = criminality19[criminality19["classe"].isin(["Coups et blessures volontaires"])] #around 60% of Nan in the column faits (number of occurence)
assault19= assault19[["CODGEO","faits"]]
assault19 = assault19.rename(columns = {"faits":"assault"})

destruction19 = criminality19[criminality19["classe"].isin(["Destructions et dégradations volontaires"])] #around 70% of Nan in the column faits (number of occurence)
destruction19 = destruction19[["CODGEO","faits"]]
destruction19 = destruction19.rename(columns = {"faits":"destruction"})

#MERGE WITH control_var
control_var = pd.merge(control_var,burglary19,how="left",on="CODGEO")
control_var = pd.merge(control_var,assault19,how="left",on="CODGEO")
control_var = pd.merge(control_var,otherassault19,how="left",on="CODGEO")
control_var = pd.merge(control_var,destruction19,how="left",on="CODGEO")
