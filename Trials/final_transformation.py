# Import all dependencies for the final transformation
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read the initial transformed file:
df = pd.read_csv('transformed_data.csv', skiprows=0, encoding='ISO-8859-1')

# create a mapping of column names to database fields
column_map = {
    'Sample_ID': 'sample_id',
    'file_id': 'file_id',
    'WL Code': 'wl_code',
    'Poço': 'poco',
    'Tipo da amostra': 'tipo_amostra',
    'Direção Amostra': 'direcao_amostra',
    'Número do testo': 'numero_testo',
    'Profundidade, m': 'profundidade',
    'Porosidade %': 'porosidade',
    'Densidade': 'densidade',
    'Permeab. Long. (mD)': 'permeabilidade_long',
    'Pressão Conf. (psi)': 'pressao_conf',
    'DATA_INICIO POÇO': 'data_inicio_poco',
    'Fluido Deslocante': 'fluido_deslocante',
    'Fluido Deslocado': 'fluido_deslocado',
    'Permeabilidade Absoluta (%)': 'permeabilidade_absoluta',
    'Pressão (psid)': 'pressao',
    'Saturação (%)': 'saturacao',
    'Método': 'metodo',
    'Curva': 'curva',
    'Coeficiente litológico': 'coeficiente_litologico',
    'Coeficiente de cimentação': 'coeficiente_cimentacao',
    'Expoente de Saturação': 'expoente_saturacao',
    'Unidade': 'unidade',
    'Fluxo Fracionário': 'fluxo_fracionario',
    'Permeabilidade do Fluido Deslocante (%)': 'permeabilidade_fluido_deslocante',
    'Permeabilidade do Fluido Deslocado (%)': 'permeabilidade_fluido_deslocado',
    'Kg (abs)': 'kg_abs',
    'Saturação Água (%)': 'saturacao_agua'
}

column_names = []
for value in column_map.values():
    column_names.append(value)

# rename the columns using the mapping
df = df.rename(columns=column_map)

# Since the language seems to be portugese, replaces all commas with full stops:
df[2:] = df[2:].replace(',','.',regex=True)

# Identify all the columns with numerical data to convert into float datatype from string
columns = ['profundidade', 'porosidade', 'densidade', 'permeabilidade_long', 
'pressao_conf', 'pressao', 'saturacao', 'coeficiente_cimentacao', 'expoente_saturacao', 
'fluxo_fracionario', 'permeabilidade_fluido_deslocado', 'kg_abs', 'saturacao_agua']

# Convert the columns to float, excluding non-numeric values
df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')

# Sort the data by well name then by depth.
df = df.sort_values(by=['poco', 'profundidade'])

df = df.drop_duplicates(subset=column_names[2:])

        # if sorted_data.iloc[idx]['porosidade'] < 1 and sorted_data.iloc[idx]['densidade'] < 1 and sorted_data.iloc[idx]['permeabilidade_long'] < 1:
        #     return val

# Fill in the empty space

df = df.replace('', np.nan).fillna(0)

print(df[df['tipo_amostra'] == 'Amostra Plug'])
print(df[df['tipo_amostra'] == 'P - Amostra Plug'])
df_merged = pd.merge(df[df['tipo_amostra'] == 'Amostra Plug'], df[df['tipo_amostra'] == 'P - Amostra Plug'], 'right',)


# def update_zeroes(val, sorted_data, col_list):
#     if val == 0:
#         # Find the index of the current value
#         sub_df = sorted_data.loc[sorted_data[col_list].apply(tuple, axis=1) == val]
#         if not sub_df.empty:
#             idx = sub_df.index[0]

#             # Find the index of the previous and next non-zero values with the same 'poco' value
#             prev_idx = idx - 1
#             while prev_idx >= 0 and sorted_data.iloc[prev_idx]['poco'] != sorted_data.iloc[idx]['poco']:
#                 prev_idx -= 1

#             next_idx = idx + 1
#             while next_idx < len(sorted_data) and sorted_data.iloc[next_idx]['poco'] != sorted_data.iloc[idx]['poco']:
#                 next_idx += 1

#             # If the previous and next values have the same 'poco' value, use their average as the new value
#             if prev_idx >= 0 and next_idx < len(sorted_data):
#                 if sorted_data.iloc[prev_idx]['poco'] == sorted_data.iloc[next_idx]['poco']:
#                     new_val = sorted_data.iloc[prev_idx:next_idx+1][col_list].mean(axis=0).values
#                     return new_val

#             # If the previous or next value does not have the same 'poco' value, use the previous value in the same 'poco'
#             if prev_idx < 0:
#                 new_val = sorted_data.iloc[next_idx][col_list].values
#             elif next_idx >= len(sorted_data):
#                 new_val = sorted_data.iloc[prev_idx][col_list].values
#             elif sorted_data.iloc[prev_idx]['poco'] == sorted_data.iloc[idx]['poco']:
#                 new_val = sorted_data.iloc[prev_idx][col_list].values
#             else:
#                 new_val = sorted_data.iloc[next_idx][col_list].values

#             return new_val
#     return val


# def fill_zeros(data):
#     '''
#     Replaces 0 values with the mean of values above and below if they have the same 'poco' value

#             Parameters:
#                     data (dataframe): The dataframe to be modified

#             Returns:
#                     filled_data (dataframe): The modified dataframe with 0 values filled in
#     '''
#     filled_data = data.copy()
#     col_list = [col for col in filled_data.columns if col not in ['poco', 'profundidade']]
#     for col in col_list:
#         sub_df = filled_data.loc[filled_data[col] != 0]
#         filled_data[col] = filled_data[col].apply(lambda x: update_zeroes(x, sub_df, col_list))
#     return filled_data

# df_filled = fill_zeros(df)



df_merged.to_csv('final_transformation.csv', index=False, encoding='latin-1')