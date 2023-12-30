
# Interestnpy

## Dynamic analysis of communal real estate price determinants and the impact of interest rates on the housing market
This project, a part of the Python course in the second year of the engineering program at ENSAE, aims to study the impact of interest rates on real estate prices at the local level, considering local town characteristics. By employing advanced econometric techniques and data analysis in Python, we seek to understand how fluctuations in interest rates influence the real estate market across various municipalities.

## Objective
The primary goal is to analyze the dynamic determinants of municipal real estate prices and study the impact of interest rates on the housing market using econometric methods. This involves exploring both time-series and panel data to provide a comprehensive understanding.

## Data and Methodology

-   **Data Sources**
	-  Ministry of Economics DVF  lists all real-estate transactions in France, except in 3 eastern departments. The data from the last few years [2019-2023](https://www.data.gouv.fr/en/datasets/demandes-de-valeurs-foncieres/) is available on data gouv. For [2014-2018]() the data was kindly archived by [Christian Quest](https://www.etalab.gouv.fr/author/christian/).
	- INSEE Filosofi provides local statistics on household income for [2014](https://www.insee.fr/fr/statistiques/3126151) and [2019](https://www.insee.fr/fr/statistiques/6036907)
	- INSEE Recensement de la population used for population data available for [1968-2020](https://www.insee.fr/fr/statistiques/7632565)
	- INSEE Local quarterly unemployment data used for zone d'emploi controls data available for [2004-2023](https://www.insee.fr/fr/statistiques/1893230)
	- INSEE Découpage data with [town code changes](https://www.insee.fr/fr/information/2028028) and [town groups](https://www.insee.fr/fr/information/2510634) used to create a dynamic conversion table between different levels
	- INSEE Zone d'emploi [shapefiles](https://www.insee.fr/fr/information/4652957) used to create geographic data vizualizations
	- DREES Accessibilité potentielle localisée measuring access to physicians used as a proxy for the quality of local services available for [2015-2022](https://data.drees.solidarites-sante.gouv.fr/explore/dataset/530_l-accessibilite-potentielle-localisee-apl/information/)
	- Interior Ministry local criminality data which is available at open data gouv for [2016-2022](https://www.data.gouv.fr/fr/datasets/bases-statistiques-communale-et-departementale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/#/resources)
	- Ministry of ecology regional terrain prices database used to substract terrain prices from transaction amounts in the DVF data available for [2008-2022](https://www.statistiques.developpement-durable.gouv.fr/catalogue?page=dataset&datasetId=63b8281ec113d45936722df2)
	- Banque de France real estate loans [survey](https://www.banque-france.fr/fr/publications-et-statistiques/statistiques/panorama-des-prets-lhabitat-des-menages) used to get effective interest rate 
-  **Aggregation** : For this project DVF data was aggregated quarterly using a custom function at 3 distinct levels: town, town group and zone d'emploi. The data was filtered and after aggregation at each level 3 variables of interest were kept, the number of transactions, the median price and the share of houses in the transaction total. This proportion is used to control for structural changes in local real estate markets as houses are often cheaper per square meter than apartments. 
-   **Econometric Approach**: Due to the limited data availability and the presence of time invariant controls  the project cannot employ time-series methods and as such must focus on a more classic panel data approach to study the effects of interest rates. However to avoid the risk of spurious correlations many alternative specifications were used. 

## Tools and Technologies

-   **Python**: The entire project is developed using Python, leveraging its powerful libraries for data analysis, data viz, and econometrics.
-   **Libraries**: Key Python libraries used include pandas for data manipulation, NumPy for numerical computations, statsmodels and linearmodels for regressions, Matplotlib and Seaborn for data visualization. The project also uses pyarrow to make use of the .feather file format, openpyxl and xlrd to read excel files very commonly used in data from ministries. 

## How to Use
1.  Clone the repository
2. [Download DVF data for 2014-2023Q1](https://1drv.ms/u/s!AiYfDSSg7esDhJNMMs6ZL9lOATBSFA), extract the files and add them to `data/external/DVF`. Or download [the uncompressed DVF data](https://1drv.ms/f/s!AiYfDSSg7esDhJNBwoKJV1DUBHZcVA).
3.  Install required Python packages (openpyxl, xlrd, pandas, numpy, pyarrow, geopandas, seaborn, matplotlib, statsmodels and linearmodels)
4.  Explore the notebook in the `root` directory to understand the analysis workflow, the `src/` folder contains scripts that were used to build the notebook. 

## Contributors
- [CALVET Rémi](https://www.linkedin.com/in/r%C3%A9mi-calvet-9674a81bb/)
- [LU Julia](https://www.linkedin.com/in/julia-lu-773272218/)
- [WISNIEWSKI Patryk](https://www.linkedin.com/in/pwisniewski02/)
