import pandas as pd

# read in the data
# Use encoding utf-8 to make sure spanish characters are mainteined
df = pd.read_excel('excel.xlsx', skiprows=1)

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

print(column_names[2:])
# rename the columns using the mapping
df = df.rename(columns=column_map)
print(df)
df[2:] = df[2:].replace(',','.',regex=True)

df = df.drop_duplicates(subset=column_names[2:])


# write the transformed data to a new file
df.to_csv('transformed_data.csv', index=False, encoding='latin-1')