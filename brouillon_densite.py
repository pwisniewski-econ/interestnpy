


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