# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def load_txt_file_to_df(file_path, column_names):
    data = np.loadtxt(file_path, comments='%', unpack=True)
    data_dict = dict(zip(column_names, data))
    df = pd.DataFrame(data_dict)
    # for column in column_names:
    #     df[column] = df[column].astype(np.float32)
    return df

file_path = 'sxx.txt'
column_names = ['X', 'Y', 'sxx', 'u', 'v']
df_sxx = load_txt_file_to_df(file_path, column_names)
print(df_sxx.describe())
print(df_sxx.info())
print(df_sxx.tail())


file_path = 'sxy.txt'
column_names = ['X', 'Y', 'sxy', 'u', 'v']
df_sxy = load_txt_file_to_df(file_path, column_names)
print(df_sxy.describe())
print(df_sxy.info())
print(df_sxy.tail())


file_path = 'syy.txt'
column_names = ['X', 'Y', 'syy', 'u', 'v']
df_syy = load_txt_file_to_df(file_path, column_names)
print(df_syy.describe())
print(df_syy.info())
print(df_syy.tail())


# %%
# Merge the dataframes on X and Y coordinates
df_merged = df_sxx.merge(df_sxy, on=['X', 'Y'], suffixes=('', '_sxy'), how='left')
# print(df_merged.head())
df_merged = df_merged.drop(['u_sxy', 'v_sxy'], axis=1)
# print(df_merged.head())
df_merged = df_merged.merge(df_syy, on=['X', 'Y'], suffixes=('', '_syy'), how='left')
# print(df_merged.head())
df_merged = df_merged.drop(['u_syy', 'v_syy'], axis=1)

# Reorder columns to desired order
df_merged = df_merged[['X', 'Y', 'u', 'v', 'sxx', 'sxy', 'syy']]

print("\nMerged dataframe info:")
print(df_merged.info())
print("\nFirst few rows of merged data:")
print(df_merged.head())



#%%
def principal_stresses(sxx, sxy, syy):
    s1 = (sxx + syy) / 2 + np.sqrt((sxx - syy)**2 / 4 + sxy**2)
    s2 = (sxx + syy) / 2 - np.sqrt((sxx - syy)**2 / 4 + sxy**2)
    return s1, s2

def principal_angles(sxx, sxy, syy):
    theta = np.arctan2(2 * sxy, sxx - syy) / 2
    return theta


# %%
df_merged['s1'], df_merged['s2'] = principal_stresses(df_merged['sxx'], df_merged['sxy'], df_merged['syy'])
df_merged['theta'] = principal_angles(df_merged['sxx'], df_merged['sxy'], df_merged['syy'])

print(df_merged.head())
# %%
# save the df_merged to a csv file
df_merged.to_csv('COMSOL_simulation_stresses.csv', index=False)

# %%

df_merged = pd.read_csv('COMSOL_simulation_stresses.csv')
color_map = 'jet'
fig, ax = plt.subplots(3, 1, figsize=(10, 15))
ax[0].tricontourf(df_merged['X'], df_merged['Y'], df_merged['s1'], cmap=color_map)
plt.colorbar(ax[0].collections[0], ax=ax[0], label='s1')
ax[0].set_xlabel('X')
ax[0].set_ylabel('Y')
ax[0].set_title('s1-principal stress')
ax[1].tricontourf(df_merged['X'], df_merged['Y'], df_merged['s2'], cmap=color_map)
plt.colorbar(ax[1].collections[0], ax=ax[1], label='s2')
ax[1].set_xlabel('X')
ax[1].set_ylabel('Y')
ax[1].set_title('s2-principal stress')
ax[2].tricontourf(df_merged['X'], df_merged['Y'], df_merged['theta'], cmap=color_map)
plt.colorbar(ax[2].collections[0], ax=ax[2], label='theta')
ax[2].set_xlabel('X')
ax[2].set_ylabel('Y')
ax[2].set_title('theta-principal angle')
plt.show()


# %%
