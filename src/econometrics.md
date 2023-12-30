
## Section X - Économétrie

Dans cette section consacrée à la modélisation, nous ferons appel à des méthodes économétriques afin de tenter de répondre à la problématique centrale de ce projet : dans quelle mesure la hausse récente des taux d'intérêt impacte-t-elle différemment les marchés immobiliers locaux en fonction des caractéristiques de chaque ville ?

Comme mentionné dans les sections précédentes, la disponibilité des variables d'intérêt sous une forme évolutive dans le temps est limitée, ce qui contraint l'usage de méthodes de séries temporelles en panel telles que les PVAR. Par conséquent, nous privilégions des méthodes classiques d'économétrie de panel, telles que les modèles à effets fixes.

Le modèle principal de cette analyse est un modèle à effets fixes. Il intègre comme variables d'intérêt le retard (lag) du taux d'intérêt en interaction avec différentes caractéristiques locales, tout en contrôlant les effets annuels et la structure des transactions effectuées. Des modèles supplémentaires à différents niveaux géographiques sont estimés pour tester la robustesse de nos résultats.

Les prix immobiliers utilisés sont exprimés, sauf indication contraire, en euros 2014.
### Test de Granger

Le marché immobilier, étant moins liquide que les marchés financiers, ne révèle l'impact du taux d'intérêt sur les prix qu'après un certain délai. Il est courant dans la littérature de considérer le retard du taux d'intérêt plutôt que le taux lui-même, comme illustré par Harris (1989) dans _The Effect of Real Rates of Interest on Housing Prices_. Cependant, cette transmission varie selon les caractéristiques des marchés immobiliers et le contexte macroéconomique. Ainsi, pour déterminer le nombre approprié de retards du taux d'intérêt dans l'analyse des marchés locaux en France, nous employons un test de Granger. Ce test évalue si une série temporelle améliore la prédiction d'une autre série temporelle et, par conséquent, si elle est pertinente pour son analyse. $$\Delta ({p}/m^{2})_t \sim \Delta L^n(i_t)$$ Nous cherchons à déterminer si l'utilisation du taux d'intérêt avec plusieurs retards apporte des informations sur les prix immobiliers. L'hypothèse nulle est l'absence de pouvoir prédictif. Pour obtenir des séries stationnaires, nous utilisons la différence. Bien qu'il existe des méthodes pour généraliser le test de Granger à des données en panel (Holtz-Eakin et al., 1988), celles-ci n'ont pas été développées en Python. Pour obtenir une idée générale du nombre de retards requis, nous appliquons le test à quelques villes de tailles variées choisies aléatoirement.

[Résultats]

Il apparaît que, selon la commune, si un effet existe, entre 1 et 4 trimestres sont nécessaires pour que le taux d'intérêt ait un pouvoir explicatif sur les prix immobiliers.

### Corrélations

Afin d'observer les interactions entre les variables d'intérêt choisies et d'obtenir une première impression de ce que la modélisation peut apporter, il est utile de construire des matrices de corrélations. D'abord, une matrice pour l'ensemble du panel, puis pour les trois premières villes utilisées lors du test de Granger.

[Matrice 1 - Total]

Cette matrice révèle une corrélation relativement faible entre les prix et le taux d'intérêt, quel que soit le nombre de retards. En revanche, les corrélations sont significatives entre les prix et la densité en 2020, l'évolution des revenus médians dans la commune, la proportion de maisons dans le total des transactions, et les changements de densité. La faible corrélation entre le taux d'intérêt et les prix s'explique probablement par la dimension N de notre panel, bien plus importante que la dimension T, le taux d'intérêt étant identique pour toutes les villes à chaque période.

Pour vérifier cela, il est possible d'établir des matrices de corrélations pour quelques villes, en excluant les variables constantes dans le temps. Par exemple, pour le 14e arrondissement de Paris : 

[Matrices 2,3,4 - Villes]

Les corrélations avec le taux d'intérêt sont plus fortes, toujours négatives, et généralement plus élevées dans les deux villes de taille supérieur. De plus, la corrélation est plus forte au premier retard à Paris, tandis que pour Clermont-Ferrand et le Grau-du-Roi, elle est plus importante au troisième retard. Cela pourrait indiquer un effet différencié du taux d'intérêt selon la taille de la ville. En utilisant ces matrices de corrélations et le test de Granger nous avons décidé d'utiliser 3 retards, ce qui représente 3 trimestres.

### Modèles communaux
Nous sommes en présence de données de panel qui posent donc différents problème à l'estimateur OLS (MCO en français) dans ce contexte souvent appelé Pooled-OLS (voir _On The Pooling Of Time Series And Cross Section Data_ Yair Mundlak, 1978). Deux méthodes souvent utilisées pour résoudre les problèmes de POLS sont l'estimation avec fixed-effects ou random-effects. Un modèle à effets fixes semble préférable dans le cadre de ce projet, car il permet d'évaluer les variations intra-groupe en controlant pour toute l'hétérogéinité innobservable constante dans le temps (par exemple une rivière est présente dans la ville), c'est également un choix assez commun dans la littérature du pricing immobilier.  Pour plus de détails sur la méthodologie générale de travail sur des données de panel voir _Econometric Analysis of Cross Section and Panel Data_ Wooldridge, 2001.
#### Modèle Introductif - Modèle simple du taux d'intérêt
Pour introduire le modèle principal une régression simple est réalisée via un pooled-OLS sans effets croisés (l'utilisation d'effets fixes est pour l'instant impossible car cela controlerait pour toute l'hétérogéinité innobservable constante dans le temps par individu et certaines de nos variables explicatives sont constantes dans le temps) : $$p_{nt}= \beta_0+\beta_iL^3(i_t)+\beta_MM_{nt} + \beta_c X_{nc}+\beta_{D}D+\varepsilon_t$$ avec $p_{nt}$ le prix des appartements et maisons dans ville $n$ à la période t, $L^3(i_t)$ le troisième retard du taux d'interet à la période t, $M_{nt}$ la proportion de maisons dans le total des transactions immobilières à la période t pour la ville n, $X_{nc}$ la matrice des variables des contrôles constante dans le temps pour la ville $n$ (densité de population en km2 en 2019, revenus médian en 2019, accès à un médecin généraliste, taux d'agressions pour 1000, et la différence de densité et de revenus entre respectivement, 2020/2014 et 2019/2014). $D$ est une variable muette servant à controler les effets fixes de chaque trimestre (par exemple, la situation macroéconomique nationale ou les confinements pendant la période covid). 

Ainsi, cette régression a pour objectif de vérifier la cohérence des résultats et d'identifier certains problèmes de données (par exemple des valeurs manquantes au niveau des arrondissements de Paris, Lyon ou Marseille). 
[Résultats]
Les résultats ne sont pas surprenant, la densité de population a un effet positif sur les prix immobiliers, tout comme le revenu médian communal et la croissance de celui-ci. Les maisons ont généralement un prix au mètre carré inférieur aux appartements le coefficient associé à prop_maison est donc bien un effet négatif. Le taux d'interet aurait un impact significatif de l'ordre de -787€ par m2 pour un point de taux en plus. La seule surpris vient de la criminalité qui a un effet positif.
#### Modèle 1 - Modèle complet avec effets fixes
Le modèle principal de cette analyse est similaire au modèle introductif mais à une différence notable, c'est qu'il inclut des coefficients d'interactions entre le taux d'interet et le reste des variables, ce qui en plus de permettre de répondre à la questions initiale de ce projet permet d'utiliser un modèle à effet fixes puisque les variables constante dans le temps deviennent dynamiques grâce au croisement avec le taux d'interet, le modèle devient donc après application d'une transformation within : $$p_{nt}-\bar{p_{n}}= \beta_0+\beta_i[L^3(i_t)-\bar{L^3(i_t)}]+\beta_M[M_{nt}-\bar{M_{n}}] + \beta_{ic}[L^3(i_t)X_{nc}-\bar{L^3(i_t)X_{nc}}]+\beta^{FE}_{D}D+\varepsilon_t$$ $$\iff \ddot{p_{nt}}= \beta^{FE}_0+\beta^{FE}_i\ddot{L^3(i_t)}+\beta^{FE}_M\ddot{M_{nt}} + \beta^{FE}_{ic}[\ddot{L^3(i_t)X_{nc}}]+\beta^{FE}_{D}D+\varepsilon_t$$ Remarque: Inclure une variable muette permet directement d'obtenir l'estimation à effets-fixe (c'est ce qui a été utilisé pour les effets fixe trimestriels) cependant cette approche présente un coût calculatoire élevé avec beaucoup de groupes, la transformation within y est donc souvent préféré (où pour chaque variable est réduite de la moyenne du groupe, ici la ville)
[Résultats]
Ainsi, il semblerait qu'une hausse du taux d'interet à un effet plus fort, dans des villes plus densément peuplé avec une baisse de 0.0248€ des prix au m2 par point de taux d'interet en plus par personne par km2. Pour paris cet effet serait d'environ 500€ par point de taux d'interet. Pour la médiane des revenus c'est 0.0414€ de baisse par points d'interet en plus, par exemple, pour Paris ce serait environ 1200€ de baisse lié à cet effet par point de taux d'interet supplémentaire. Un effet similaire est observé dans des villes en croissance (économique et démographique). Les villes avec un bon niveau d'accès au soins serait également plus touché comme les villes avec plus d'agressions (variable qui se comporte peut-être comme un proxy des zones métropolitaines), cependant ces deux variables ont une significativité pratique assez faible (l'échelle sur laquelle ces variables sont distribuées est assez petite). Le $R^2$ affiché est "within" c'est à dire qu'il représente la partie de la variance expliquée à l'intérieur du groupe, dans le cas présent notre modèle explique environ 25% de la variance des prix immobilier dans une même ville dans la dimension temporelle. 

Ces résultats semblent cohérents avec l'hypothèse d'effets spéculatifs et/ou de substitutions. Pour vérifier la robustesse de ces résultats plusieurs spécifications supplémentaires sont dévelopées. 
#### Modèle 1c - Modèle log-niveau
Une critique possible de notre modèle est l'existance d'effets d'échelles relativement fort sur les prix, les prix immobilier pouvant varier fortement d'une ville à une autre. Ce modèle utilise donc une spécification log-niveau.
$$ \ddot{log(p_{nt})}= \beta^{FE}_0+\beta^{FE}_i\ddot{L^3(i_t)}+\beta^{FE}_M\ddot{M_{nt}} + \beta^{FE}_{ic}[\ddot{L^3(i_t)X_{nc}}]+\beta^{FE}_{D}D+\varepsilon_t$$
[Résultat]
Les résultats sont cohérents avec le premier modèle on remarque par ailleurs que le $R^2$ a augmenté sensiblement, le modèle explique ici 60% de la variance du log des prix dans une  même commune.

#### Modèle 2 - Modèle avec prix dé-tendanciés
Les prix immobiliers n'étant pas un processus stationaire il existe un risque de corrélations falacieuse, en enlevant la tendance de l'évolution des prix le processus ne devient pas stationaire mais ceci réduit le risque d'obtenir des résultats liée à la hausse des prix sur la période, pour simplifier les calculs ce modèle n'inclus pas d'effets fixes. Il s'agit une estimation en deux étapes. 
1) Régression des prix sur le temps avec t le nombre de trimestres depuis le début du panel pour chaque groupe : $$ p_{nt}=\beta_0+\beta_{tn}t$$ 

2) Régression des prix réduit de la tendance linéaire estimé sur le taux d'interet et les interactions : $$(p_{nt}-\beta_{nt}\times t)= \beta_0+\beta_iL^3(i_t)+\beta_MM_{nt} + \beta_c X_{nc}+\beta_{ic}L^3(i_t)X_{nc}+\beta_{iM}L^3(i_t)M_{nt}+\beta_{D}D+\varepsilon_t $$

Ce modèle souffre  d'hétoskédacticité comme le montre le test Breuschpagan les coefficients sont donc affichés sous forme robuste
[Résultats]
Ce modèle à la particularité d'avoir peu de coefficients statistiquement signifactifs mais les effets croisés taux d'interets densité reste significatifs à un niveau inférieur à 1% et l'interactions avec les revenus est significative à un niveau d'environ 6%. Il semblerait donc que l'essentiels de nos conclusions soit robuste à un retranchement de tendance. 

### Modèles ZE (Zone d'Emploi)
#### Modèle 3 - Spécification ZE du modèle complet
En estimant notre modèle zone d'emploi (ie. $n$ représente une zone d'emploi) et y ajoutant le taux de chomage au même retard que le taux d'interet (pour simplifier l'interprétation) : $$\ddot{p_{nt}}= \beta^{FE}_0+\beta^{FE}_i\ddot{L^3(i_t)}+\beta^{FE}_V\ddot{Z_{nt}} + \beta^{FE}_{IC}[\ddot{L^3(i_t)X_{nc}}]+\beta^{FE}_{IV}[\ddot{L^3(i_t)Z_{nt}}]+\beta^{FE}_{D}D+\varepsilon_t$$
 $Z_{nt}$ inclus toutes les charactéristiques variante dans le temps par zone d'emploi (ie. chomage et proportion de maisons vendues dans le total). Ce modèle souffre également d'hétoskédacticité comme le montre le test Breuschpagan les coefficients sont donc affichés sous forme robuste
 [Résultat]
Les résultats sont cohérents avec nos résultats précédents mais on remarque que le coefficients associés au chomage capture la majorité de l'effet précédement attribué aux revenus. Il semblerait que les revenus médians soit un proxy général de la santé économique locale.
### Modèles EPCI (Établissement Public de Coopération Intercommunale)

#### Modèle 4 - Spécification EPCI du modèle complet
Pour finir, nous estimons notre modèle au niveau EPCI : $$\ddot{p_{nt}}= \beta^{FE}_0+\beta^{FE}_i\ddot{L^3(i_t)}+\beta^{FE}_M\ddot{M_{nt}} + \beta^{FE}_{ic}[\ddot{L^3(i_t)X_{nc}}]+\beta^{FE}_{D}D+\varepsilon_t$$ Ce modèle souffre également d'hétoskédacticité comme le montre le test Breuschpagan les coefficients sont donc affichés sous forme robuste.
 [Résultat]
Ces résultats sont similaires même si l'effet total du taux d'interet est réduit à cause du coefficient associé à $E[B^{FE}_i|(\ddot{L^3(i_t)X_{nc}})=0]$  qui est positif et est égal à 1882 même si il n'est pas significatif à 5%. L'effet de l'évolution des revenus est par ailleurs plus fort que dans les autres modèles. 
