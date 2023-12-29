import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.tsa.stattools import grangercausalitytests
from linearmodels import PanelOLS, RandomEffects
from statsmodels.stats.diagnostic import het_breuschpagan
from linearmodels.panel import compare
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller

# Custom Functions
def merge_and_transform(base_df, irflation_df, control_df, base_col, min_transactions=30, required_count=38):
    base_df=base_df.drop(columns=["LIB_"+base_col])
    df = base_df[base_df['n_transactions'] > min_transactions]
    df['n'] = df.groupby(base_col)[base_col].transform('count')
    df = df[df['n'] == required_count].drop(columns='n')
    df = df.merge(irflation_df, on='Date', how='left')
    df = df.merge(control_df, on=base_col, how='left')
    df['prixM2'] = df['prixM2'] / df['BASE14']
    df['Q219'] = df['Q219'] / irflation['BASE14'][20]
    df['med_change'] = (df['Q219'] / irflation_df['BASE14'][20]) - (df['Q214'] / irflation_df['BASE14'][0])
    df['dens_change'] = df['popdensity2019'] - df['popdensity2014']
    return df

def group_and_calculate_diff(df, group_cols):
    df = df.sort_values(by=group_cols + ['Date'])
    grouped = df.groupby(group_cols)
    df['diff_prixM2'] = grouped['prixM2'].diff().fillna(np.nan)
    df['diff2_prixM2'] = grouped['prixM2'].diff().diff().fillna(np.nan)
    df['prixM2_FE'] = grouped['prixM2'].transform(lambda x: x - x.mean()) #Within transformation
    df['year'] = df['Date'].str[:4]
    df['diff2_prop_maison'] = grouped['prop_maison'].diff().fillna(np.nan)
    df['lag_ir'] = grouped['ir'].shift(1)
    df['lag2_ir'] = grouped['ir'].shift(2)
    df['lag4_ir'] = grouped['ir'].shift(4)
    df['diff_lag_ir'] = grouped['lag_ir'].diff().fillna(np.nan)
    df['diff2_lag_ir'] = grouped['lag_ir'].diff().diff().fillna(np.nan)
    return df.reset_index(drop=True)

def run_regression(df, formula):
    model = smf.ols(formula, data=df)
    results = model.fit()
    return(results)

def aggregate_data(df, group_cols, agg_dict):
    agg_df = df.groupby(group_cols).agg(agg_dict).reset_index()
    agg_df['popdensity2019'] = agg_df['P20_POP'] / agg_df['SUPERF']
    agg_df['popdensity2014'] = agg_df['P14_POP'] / agg_df['SUPERF']
    return agg_df.drop(columns=['P20_POP', 'P14_POP', 'SUPERF'])

def corplot(df, nom):
  plt.figure(figsize=(10, 8))
  sns.heatmap(df, annot=True, cmap='coolwarm')
  plt.title('Correlations intra-ville pour '+nom)
  plt.show()
  
def cor_ville(df, nom):
  df = df[df['LIB_COM']==nom]
  df = df[["prixM2", "ir","lag_ir","lag2_ir","lag4_ir", "prop_maison"]].dropna().corr()
  return(df)


# Reading Data
base_path = "C:/Users/rems9/Desktop/Travail/ENSAE/2A/projet_python/interestnpy/data/interim/"
#base_path = "C:/Users/patry/Documents/GitHub/interestnpy/data/interim/"
immo_epci = pd.read_feather(base_path + "immo_panel_epci_py.feather")
immo_ze = pd.read_feather(base_path + "immo_panel_ze_py.feather")
immo_com = pd.read_feather(base_path + "immo_panel_com_py.feather")
immo_full = pd.read_feather(base_path + "immo_panel_full_py.feather")
unemployment = pd.read_feather(base_path + "TV_controls.feather")
control = pd.read_feather(base_path + "TI_controls.feather")
irflation = pd.read_feather(base_path + "irflation.feather")

# Aggregate data
agg_dict_control = {
    'Q219': 'mean', 'Q214': 'mean',
    'P20_POP': 'sum', 'P14_POP': 'sum',
    'SUPERF': 'sum', 'Physicist_access': 'mean',
    'assault_for_1000': 'mean'
}
control_ze = aggregate_data(control, ['ZE', 'LIB_ZE'], agg_dict_control)
control_epci = aggregate_data(control, ['EPCI', 'LIB_EPCI'], agg_dict_control)

# Processing for immo_reg_com
immo_reg_com = merge_and_transform(immo_com, irflation, control, 'COM')
immo_reg_com_diff = group_and_calculate_diff(immo_reg_com, ['COM'])

# Total 
immo_reg_corr =immo_reg_com_diff[["prixM2", "ir","lag_ir","lag2_ir","lag4_ir","popdensity2019", "med_change", "Physicist_access", "Q219", "prop_maison", "assault_for_1000", "dens_change"]].dropna().corr()
corplot(immo_reg_corr, "Total")

# Intra villes
for i in ["Paris 14","Clermont-Ferrand","Le Grau-du-Roi"]:
  corplot(cor_ville(immo_reg_com_diff, i), i)

# Processing for immo_reg_ze
immo_reg_ze = merge_and_transform(immo_ze, irflation, control_ze, 'ZE')
immo_reg_ze_diff = group_and_calculate_diff(immo_reg_ze, ['ZE', 'LIB_ZE'])
immo_reg_ze_diff = immo_reg_ze_diff.merge(unemployment[['ZE2020', 'Date', 'UNEMP']], left_on=['ZE', 'Date'], right_on=['ZE2020', 'Date'], how='left')
immo_reg_ze_diff['lag_UNEMP'] = immo_reg_ze_diff.groupby(['ZE', 'LIB_ZE'])['UNEMP'].shift(1)
immo_reg_ze_diff['diff2_lag_unemp'] = immo_reg_ze_diff.groupby(['ZE', 'LIB_ZE'])['UNEMP'].shift().diff().diff()

# Processing for immo_reg_epci
immo_reg_epci = merge_and_transform(immo_epci, irflation, control_epci, 'EPCI')
immo_reg_epci_diff = group_and_calculate_diff(immo_reg_epci, ['EPCI', 'LIB_EPCI'])

# Granger Causality Test
granger_test3 = grangercausalitytests(immo_reg_com[['prixM2', 'ir']], maxlag=5, verbose=True)

# Hausman test
immo_reg_com_diff['Date'] = pd.to_datetime(immo_reg_com_diff['Date'], format='%Y%m%d')
immo_reg_com_diff = immo_reg_com_diff.set_index(['LIB_COM', 'Date'])

for var in ['popdensity2019', 'med_change', 'Physicist_access', 'Q219', 'prop_maison', 'assault_for_1000', 'dens_change']:
    immo_reg_com_diff[f'lag_ir_{var}'] = immo_reg_com_diff['lag_ir'] * immo_reg_com_diff[var]

formula = 'prixM2 ~ 1 + lag_ir+ prop_maison+popdensity2019+Physicist_access+Q219+assault_for_1000+dens_change+ lag_ir_popdensity2019 + lag_ir_med_change + lag_ir_Physicist_access + lag_ir_Q219 + lag_ir_prop_maison + lag_ir_assault_for_1000 + lag_ir_dens_change + C(year)'

mod = PanelOLS.from_formula(formula, data=immo_reg_com_diff, drop_absorbed=True)
fixed_effects_results = mod.fit()

random_effects = RandomEffects.from_formula(formula, data=immo_reg_com_diff)
random_results = random_effects.fit()

hausman_results = compare({"Fixed Effects": fixed_effects_results, "Random Effects": random_results}, precision='tstats')


# Model 1a
model1a = 'prixM2_FE ~ lag_ir + prop_maison + C(year)'
run_regression(immo_reg_com_diff, model1a).summary()

# Model 1b
model1b_formula = 'prixM2_FE ~ lag_ir * (popdensity2019 + med_change + Physicist_access + Q219 + prop_maison + assault_for_1000 + dens_change) + prop_maison + C(year)'
mod1b = run_regression(immo_reg_com_diff, model1b_formula)

test_breuschpagan = het_breuschpagan(mod1b.resid,  mod1b.model.exog)
test_breuschpagan

mod1b.get_robustcov_results(cov_type='HC3').summary()

residuals = mod1b.resid
plt.figure(figsize=(8, 6))
sns.kdeplot(residuals, bw_adjust=7, shade=True)  # Adjust bandwidth as needed
plt.title('Distribution des erreurs')
plt.xlim(-5000, 5000)
plt.xlabel('Residuals')
plt.ylabel('Density')
plt.show()
  
# Model 1c
model1c_formula = 'prixM2 ~ lag_ir * (popdensity2019 + med_change + Physicist_access + Q219 + prop_maison + assault_for_1000 + dens_change) + C(year)'
mod1c = run_regression(immo_reg_com_diff, model1b_formula)

test_breuschpagan = het_breuschpagan(mod1c.resid,  mod1c.model.exog)
test_breuschpagan

mod1c.get_robustcov_results(cov_type='HC2').summary()

#DETRENDED REGRESSION
immo_reg_com_diff['time'] = immo_reg_com_diff.groupby('COM').cumcount() + 1
df_reg = immo_reg_com_diff.groupby('COM').apply(lambda x: smf.ols('prixM2 ~ time', data=x).fit().resid + x['prixM2']).reset_index(name='detrended_variable')
reg_immo2 = immo_reg_com_diff.groupby('COM').apply(lambda x: smf.ols('prixM2 ~ time', data=x).fit().params['time']).reset_index(name='estimate')
vroom = immo_reg_com_diff.reset_index(drop=False).merge(reg_immo2, on='COM')
vroom['prixM2_dt'] = vroom['prixM2'] - vroom['time'] * vroom['estimate']

model_detrend= 'prixM2_dt ~ lag_ir * (popdensity2019 + med_change + Physicist_access + Q219 + prop_maison + assault_for_1000 + dens_change) + prop_maison + C(AN)'
mod2 = run_regression(vroom, model_detrend)

test_breuschpagan = het_breuschpagan(mod2.resid,  mod2.model.exog)
test_breuschpagan

mod2.get_robustcov_results(cov_type='HC2').summary()

#PRICE EVOLUTION COMPARISON
plot_data = vroom[vroom['LIB_COM'].str.startswith('Paris 14')].copy()
plot_data['prixM2_noncorrige'] = plot_data['prixM2'] * plot_data['BASE14']
plot_data['Date'] = pd.to_datetime(plot_data['Date'], format='%Y%m%d')
plot_data_melted = plot_data.melt(id_vars='Date', value_vars=['prixM2', 'prixM2_dt', 'prixM2_noncorrige'])

plt.figure(figsize=(10, 6))
sns.lineplot(data=plot_data_melted, x='Date', y='value', hue='variable')
plt.title("Évolution des prix, Paris 14e, nominal, euros 2014 et euros 2014 detrend")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend(title='Variable')
plt.show()

# Part 4: Linear Regression Models
# Model mod3
mod3_formula = 'prixM2_FE ~ lag_ir * (popdensity2019 + med_change + Physicist_access + Q219 + prop_maison + assault_for_1000 + dens_change+lag_UNEMP) + prop_maison + C(year)'
mod3 = run_regression(immo_reg_ze_diff, mod3_formula)

test_breuschpagan = het_breuschpagan(mod3.resid,  mod3.model.exog)
test_breuschpagan

mod3.get_robustcov_results(cov_type='HC2').summary()

# Model mod5
mod5_formula = 'prixM2_FE ~ lag_ir * (popdensity2019 + med_change + Physicist_access + Q219 + prop_maison + assault_for_1000 + dens_change) + prop_maison + C(year)'
mod5 = run_regression(immo_reg_epci_diff, mod5_formula)

test_breuschpagan = het_breuschpagan(mod5.resid,  mod5.model.exog)
test_breuschpagan

mod5.get_robustcov_results(cov_type='HC2').summary()
