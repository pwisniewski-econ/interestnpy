


#COLLER CA DANS UNE CELLULE EN DESSOUS DE LA CELLULE QUI COMMENCE PAR #IMPORT AVAILABLE INCOME DATA  
#Densité de revenus en 2019 par commune
sns.kdeplot(income2019[["Q219"]], fill=True, label= "2019",palette='Blues')
sns.kdeplot(income2014[["Q214"]], fill=True, label = "2014",palette='Greens')
plt.xlabel('Revenu médian par an en euros')
plt.ylabel('Densité')
plt.legend()
plt.title("Densité du revenu médian en 2014 et 2019")
plt.show()





#COLLER CA DANS UNE CELLULE EN DESSOUS DE CELLE QUI CONTIENT JUSTE densite.head()
#Densité de population en 2014 et 2020 par commune
sns.kdeplot(densite[["popdensity2020"]], fill=True, label= "2020",palette='Blues')
sns.kdeplot(densite[["popdensity2014"]], fill=True, label = "2014",palette='Greens')
plt.xlabel('Densité de population')
plt.ylabel('Densité')
plt.legend()
plt.title('Densité de la densité de population en 2014 et 2020')
plt.show()

#Densité de population en 2014 et 2020 par commune avec plot tronqué
plt.subplot
sns.kdeplot(densite[["popdensity2020"]], fill=True, label= "2020",palette='Blues')
sns.kdeplot(densite[["popdensity2014"]], fill=True, label = "2014",palette='Greens')
plt.xlabel('Densité de population')
plt.ylabel('Densité')
plt.legend()
plt.title('Densité de la densité de population en 2014 et 2020 (tronque à 2000) ')
plt.xlim(0,2000)
plt.show()


#VERIFER PAS COLLER TOUT DE SUITE (mettre juste au dessus du tableau définition des variables)
#CARTE REVENU MEDIAN PAR ZONE D'EMPLOI

#Création d'un dataframe avec le revenu médian en 2014 par zone d'emploi pour fair une carte
P14_POP_by_ZE = control_var.groupby('ZE')['P14_POP'].sum() #population niveau ZE en 2014
dfQ214 = control_var
dfQ214["Q214_pondere"] = control_var['Q214'] * control_var["P14_POP"] #multiplie revenu médian par la population
dfQ214 = dfQ214.groupby('ZE')['Q214_pondere'].sum() #agrege par ZE en sommant
dfQ214 = pd.merge(dfQ214,P14_POP_by_ZE,on="ZE") 
dfQ214["Q214_ZE"] = dfQ214["Q214_pondere"]/dfQ214["P14_POP"] #divise le revenu médian pondéré par la population de la ZE pour avoir le revenu médian de la ZE
dfQ214 = dfQ214[["Q214_ZE"]]
 
full_map2 = ze_shp.merge(dfQ214, on="ZE", how="left")

plot_map(full_map2, 
         'Q214_ZE', "Revenu médian en 2014 par zone d'emploi", 
         "YlGnBu")





#Création d'un dataframe avec l'accès aux soins par zone d'emploi pour faire une carte
P14_POP_by_ZE = control_var.groupby('ZE')['P14_POP'].sum() #population niveau ZE en 2014
dfQ214 = control_var
dfQ214["Physicist_access_pondere"] = control_var['Physicist_access'] * control_var["P14_POP"] #multiplie Physicist_access par la population
dfQ214 = dfQ214.groupby('ZE')['Physicist_access_pondere'].sum() 
dfQ214 = pd.merge(dfQ214,P14_POP_by_ZE,on="ZE")
dfQ214["Physicist_access_ZE"] = dfQ214["Physicist_access_pondere"]/dfQ214["P14_POP"]
dfQ214 = dfQ214[["Physicist_access_ZE"]]
dfQ214["Physicist_access_ZE"] = dfQ214["Physicist_access_ZE"].astype(float)
 
full_map3 = ze_shp.merge(dfQ214, on="ZE", how="left")




plot_map(full_map3, 
         'Physicist_access_ZE', "Physicist_access en 2014 par zone d'emploi", 
         "YlGnBu")