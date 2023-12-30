
## Section X - Économétrie

Dans cette section consacrée à la modélisation, nous ferons appel à des méthodes économétriques afin de tenter de répondre à la problématique centrale de ce projet : dans quelle mesure la hausse récente des taux d'intérêt impacte-t-elle différemment les marchés immobiliers locaux en fonction des caractéristiques de chaque ville ?

Comme mentionné dans les sections précédentes, la disponibilité des variables d'intérêt sous une forme évolutive dans le temps est limitée, ce qui contraint l'usage de méthodes de séries temporelles en panel telles que les PVAR. Par conséquent, nous privilégions des méthodes classiques d'économétrie de panel, telles que les modèles à effets fixes.

Le modèle principal de cette analyse est un modèle à effets fixes. Il intègre comme variables d'intérêt le retard (lag) du taux d'intérêt en interaction avec différentes caractéristiques locales, tout en contrôlant les effets annuels et la structure des transactions effectuées. Des modèles supplémentaires à différents niveaux géographiques sont estimés pour tester la robustesse de nos résultats.

### Test de Granger

Le marché immobilier, étant moins liquide que les marchés financiers, ne révèle l'impact du taux d'intérêt sur les prix qu'après un certain délai. Il est courant dans la littérature de considérer le retard du taux d'intérêt plutôt que le taux lui-même, comme illustré par Harris (1989) dans _The Effect of Real Rates of Interest on Housing Prices_. Cependant, cette transmission varie selon les caractéristiques des marchés immobiliers et le contexte macroéconomique. Ainsi, pour déterminer le nombre approprié de retards du taux d'intérêt dans l'analyse des marchés locaux en France, nous employons un test de Granger. Ce test évalue si une série temporelle améliore la prédiction d'une autre série temporelle et, par conséquent, si elle est pertinente pour son analyse. $$\Delta ({p}/m^{2})_t \sim \Delta L^n(i_t)$$ Nous cherchons à déterminer si l'utilisation du taux d'intérêt avec plusieurs retards apporte des informations sur les prix immobiliers. L'hypothèse nulle est l'absence de pouvoir prédictif. Pour obtenir des séries stationnaires, nous utilisons la différence. Bien qu'il existe des méthodes pour généraliser le test de Granger à des données en panel (Holtz-Eakin et al., 1988), celles-ci n'ont pas été développées en Python. Pour obtenir une idée générale du nombre de retards requis, nous appliquons le test à quelques villes de tailles variées choisies aléatoirement.

[Résultats]

Il apparaît que, selon la commune, si un effet existe, entre 1 et 3 trimestres sont nécessaires pour que le taux d'intérêt ait un pouvoir explicatif sur les prix immobiliers.

### Corrélations

Afin d'observer les interactions entre les variables d'intérêt choisies et d'obtenir une première impression de ce que la modélisation peut apporter, il est utile de construire des matrices de corrélations. D'abord, une matrice pour l'ensemble du panel, puis pour les trois premières villes utilisées lors du test de Granger.

[Matrice 1 - Total]

Cette matrice révèle une corrélation relativement faible entre les prix et le taux d'intérêt, quel que soit le nombre de retards. En revanche, les corrélations sont significatives entre les prix et la densité en 2020, l'évolution des revenus médians dans la commune, la proportion de maisons dans le total des transactions, et les changements de densité. La faible corrélation entre le taux d'intérêt et les prix s'explique probablement par la dimension NN de notre panel, bien plus importante que la dimension TT, le taux d'intérêt étant identique pour toutes les villes à chaque période.

Pour vérifier cela, il est possible d'établir des matrices de corrélations pour quelques villes, en excluant les variables constantes dans le temps. Par exemple, pour le 14e arrondissement de Paris : 

[Matrices 2,3,4 - Villes]

Les corrélations avec le taux d'intérêt sont plus fortes, toujours négatives, et généralement plus élevées dans les deux villes de taille supérieur. De plus, la corrélation est plus forte au premier retard à Paris, tandis que pour Clermont-Ferrand et le Grau-du-Roi, elle est plus importante au troisième retard. Cela pourrait indiquer un effet différencié du taux d'intérêt selon la taille de la ville.

### Modèles communaux

#### Modèle 1a - Modèle simple du taux d'intérêt

#### Modèle 1b - Modèle complet avec effets fixes

#### Modèle 1c - Modèle logarithmique sans effets fixes

#### Modèle 2 - Modèle avec prix dé-tendanciés

### Modèles ZE (Zone d'Emploi)

#### Modèle 3 - Spécification ZE du modèle complet

### Modèles EPCI (Établissement Public de Coopération Intercommunale)

#### Modèle 4 - Spécification EPCI du modèle complet
