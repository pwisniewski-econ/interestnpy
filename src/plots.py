import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# Setting up the file paths using pathlib
path = "C:/Users/patry/Documents/GitHub/interestnpy"

# Reading the data
ze_shp = gpd.read_file(path+"/data/external/ze2020_2023/ze2020_2023.shp")
immo_panel = pd.read_feather(path+"/data/interim/immo_panel_ze_py.feather")
immo_panel_com = pd.read_feather(path+"/data/interim/immo_panel_com_py.feather")
immo_panel_full = pd.read_feather(path+"/data/interim/immo_panel_full_py.feather")
inflation = pd.read_feather(path+"/data/interim/inflation.feather")
interest_rates = pd.read_feather(path+"/data/interim/interest_rates.feather")

# Data manipulation
immo_panel = immo_panel[(immo_panel['Date'] == '20230101') | 
                           (immo_panel['Date'] == '20190101') | 
                           (immo_panel['Date'].isna())]
immo_panel.sort_values(by=['ZE', 'Date'], inplace=True)
immo_panel['dprix'] = immo_panel.groupby('ZE')['prixM2'].transform(lambda x: x - x.shift())

ze_shp['ZE'] = ze_shp['ze2020'].astype(float)
full_map = ze_shp.merge(immo_panel, on="ZE", how="left")

# Plotting
def plot_map(data, variable, title, palette):
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(column=variable, ax=ax, legend=True, cmap=palette,
    missing_kwds={'color': 'lightgrey', 'hatch': '///'})
    plt.title(title)
    plt.xlim(-4.5, 9.5)
    plt.ylim(41.5, 51)
    ax.set_axis_off()
    plt.show()

plot_map(full_map[(full_map['Date'] == '20190101')|(full_map['Date'].isna())], 
         'prixM2', "Prix immobilier par zone d'emploi, premier trimestre 2019", 
         "YlGnBu")

plot_map(full_map[(full_map['Date'] == '20230101')|(full_map['Date'].isna())], 
         'dprix', "Prix immobilier par zone d'emploi, différence 2023T1-2019T1", 
         "RdYlGn_r")

# Plotting time series
def plot_time_series(data, x, y, title, hue=None):
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=data, x=x, y=y, hue=hue)
    plt.legend(title=hue, loc='upper left', bbox_to_anchor=(1, 1))
    plt.title(title)
    plt.show()

plot_time_series(inflation, "AN", "INFLATION", "Inflation entre 2014 et 2023")

interest_rates['Date'] = pd.to_datetime(interest_rates['Date'], format='%Y%m%d')

plot_time_series(interest_rates, "Date", "ir", "Taux d'interet moyen entre 2014 et 2023")

immo_panel_com['DateF'] = pd.to_datetime(immo_panel_com['Date'], format='%Y%m%d')

immo_panel_com_grouped = immo_panel_com.groupby('DateF').agg({'n_transactions': 'sum'}).reset_index()
plot_time_series(immo_panel_com_grouped, 'DateF', 'n_transactions', 
                 "Évolution du nombre de transactions, France DVF, 2014T1-2023T2")
  
immo_panel_full['DateF'] = pd.to_datetime(immo_panel_full['Date'], format='%Y%m%d')

plot_time_series(immo_panel_full, 'DateF', 'prixM2', 
                 "Évolution des prix immonilier, France DVF, 2014T1-2023T2")

# Evolution des prix parisiens ---
paris_data = immo_panel_com[immo_panel_com['LIB_COM'].str.startswith('Paris ')]
paris_data = paris_data.sort_values(by='DateF')
window_size = 5  
paris_data['Moving_Average'] = paris_data.groupby('LIB_COM')['prixM2'].transform(lambda x: x.rolling(window=window_size).mean())
plt.figure(figsize=(12, 8))
sns.lineplot(data=paris_data, x='DateF', y='prixM2', hue='LIB_COM', alpha=0.3)
sns.lineplot(data=paris_data, x='DateF', y='Moving_Average', hue='LIB_COM', alpha=0.8, legend=None)
plt.title('Évolution des prix immobiliers avec moyenne mobile, Paris, 2014T1-2023T2')
plt.xlabel('Date')
plt.ylabel('Prix M2')
plt.xticks(rotation=45)
sns.set_theme(style="whitegrid")
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles=handles[1:], labels=labels[1:], loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=len(paris_data['LIB_COM'].unique()))
plt.show()




