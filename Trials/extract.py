# Column names:: 

# Sample_ID,file_id,WL Code
# Poço,Tipo da amostra,Direção Amostra,Número do testo
# Profundidade m, Porosidade %,Densidade,Permeab. Long. (mD),Pressão Conf. (psi), DATA_INICIO POÇO,Fluido Deslocante,Fluido Deslocado,
# Permeabilidade Absoluta (%),Pressão (psid),Saturação (%),Método,Curva, Coeficiente litológico, Coeficiente de cimentação, Expoente de Saturação, Unidade, Fluxo Fracionário, 
# Permeabilidade do Fluido Deslocante (%), Permeabilidade do Fluido Deslocado (%), Kg (abs), Saturação Água (%)



import pandas as pd

# Read the Excel sheet into a Pandas DataFrame
df = pd.read_excel('excel.xlsx', skiprows = 1, header = 0)

# Define the columns that should be included in the table of tabulated data
table1_columns = ['Sample_ID', 'file_id', 'WL Code', 'Poço', 'Tipo da amostra', 'Direção Amostra',
                  'Número do testo', 'Profundidade, m', 'Porosidade %', 'Densidade', 'Permeab. Long. (mD)',
                  'Pressão Conf. (psi)', 'DATA_INICIO POÇO', 'Fluido Deslocante', 'Fluido Deslocado',
                  'Permeabilidade Absoluta (%)', 'Pressão (psid)', 'Saturação (%)', 'Método', 'Curva',
                  'Coeficiente litológico', 'Coeficiente de cimentação', 'Expoente de Saturação',
                  'Unidade', 'Fluxo Fracionário', 'Permeabilidade do Fluido Deslocante (%)',
                  'Permeabilidade do Fluido Deslocado (%)', 'Kg (abs)', 'Saturação Água (%)']

# Define the columns that should be included in the table of database fields
table2_columns = ['Field Name']

# Create a DataFrame for table 1
table1 = df[table1_columns]

# Create a DataFrame for table 2
table2 = pd.DataFrame(table1_columns, columns=table2_columns)

# Print the resulting tables
print("Table 1 (Tabulated Data):\n", table1)
print("Table 2 (Database Fields):\n", table2)