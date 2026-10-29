import pandas as pd

# 1. Lendo o arquivo CSV com os dados do Brasileirão
try:
    df_futebol = pd.read_csv('BRA.csv', encoding='utf-8')
except UnicodeDecodeError:
    df_futebol = pd.read_csv('BRA.csv', encoding='latin1')

# 2. Removendo colunas desnecessárias para a análise
df_futebol = df_futebol.loc[:, ~df_futebol.columns.str.contains('^Unnamed')]

# 3. Limpando espaços e caracteres especiais dos nomes das colunas
df_futebol.columns = df_futebol.columns.str.replace(r'[^a-zA-Z0-9_]', '', regex=True)

# 4. Convertendo a coluna Date deixando o Pandas inferir o formato automaticamente (errors='coerce' transforma erros em NaT)
df_futebol['Date'] = pd.to_datetime(df_futebol['Date'], dayfirst=True, errors='coerce')

# 5. Criando coluna apenas com informações esportivas para faciliar a análise
colunas_esportivas = ['Country', 'League', 'Season', 'Date', 'Time', 'Home', 'Away', 'HG', 'AG', 'Res']

# 6. Mantendo apenas as colunas esportivas no DataFrame
df_futebol = df_futebol[colunas_esportivas].copy()

# 7. Verificando resultado das limpezas e conversões
print("\nColunas atuais:")
print(df_futebol.columns.tolist())

# 8. Configurando opções de exibição do Pandas para melhor visualização
pd.set_option('display.max_columns', None)  # Exibir todas as colunas
pd.set_option('display.width', None)  # Ajustar a largura de exibição

# 9. Exibindo as primeiras linhas do DataFrame para verificação
print("Primeiras linhas do DataFrame do Brasileirao:")
print(df_futebol.head(10))

# 10. Salvando o DataFrame limpo em um novo arquivo CSV
df_futebol.to_csv('BRA_cleaned.csv', index=False)