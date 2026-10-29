import pandas as pd

# 1. Lendo o arquivo CSV com os dados limpos do Brasileirão
df_analise = pd.read_csv('BRA_cleaned.csv')

# 2. convertendo a coluna Date para o tipo datetime
df_analise['Date'] = pd.to_datetime(df_analise['Date'], errors='coerce')

# 3. Imprime o numero total de partidas e uma lista com todas as temporadas distintas presentes no DataFrame
print(f"\nNumero total de partidas: {len(df_analise)}")
print(f"Temporadas distintas: {df_analise['Season'].unique()}")

# 4. Criando uma tabela para analisar o desempenho dos clubes
def calcular_tabela(df_base, temporada_alvo):
    df_temporada = df_base[df_base['Season'] == temporada_alvo].copy()
    if df_temporada.empty:
        return None # Retorna None se não houver dados para a temporada especificada
    
    # Obtendo a lista de times únicos que participaram da temporada
    times = pd.unique(df_temporada[['Home', 'Away']].values.ravel())
    tabela = []
    
    # Calculando estatísticas para cada time na temporada
    for time in times:
        casa = df_temporada[df_temporada['Home'] == time]
        fora = df_temporada[df_temporada['Away'] == time]
        
        jogos = len(casa) + len(fora)
        vitorias = len(casa[casa['Res'] == 'H']) + len(fora[fora['Res'] == 'A'])
        empates = len(casa[casa['Res'] == 'D']) + len(fora[fora['Res'] == 'D'])
        derrotas = len(casa[casa['Res'] == 'A']) + len(fora[fora['Res'] == 'H'])
        
        gols_pro = casa['HG'].sum() + fora['AG'].sum()
        gols_contra = casa['AG'].sum() + fora['HG'].sum()
        saldo_gols = gols_pro - gols_contra
        pontos = (vitorias * 3) + (empates * 1)
        
        tabela.append({
            'Season': temporada_alvo,
            'Time': time,
            'J': jogos,
            'V': vitorias,
            'E': empates,
            'D': derrotas,
            'GP': gols_pro,
            'GC': gols_contra,
            'SG': saldo_gols,
            'Pts': pontos
        })
    
    # Criando um DataFrame a partir da lista de dicionários e ordenando pela pontuação, vitórias e saldo de gols    
    df_tabela = pd.DataFrame(tabela)
    df_tabela = df_tabela.sort_values(by=['Pts', 'V', 'SG'], ascending=[False, False, False]).reset_index(drop=True)
    df_tabela['Posicao'] = df_tabela.index + 1 # Adiciona a coluna de posição com base na classificação    
    return df_tabela

# 5. Função para calcular a tabela de uma temporada específica
anos = range(2015, 2026)  # Anos de 2015 a 2025
lista_tabela_historica = []

# 6. Calculando a tabela para cada ano e armazenando em uma lista
for ano in anos:
    tabela_ano = calcular_tabela(df_analise, ano)
    if tabela_ano is not None:
        lista_tabela_historica.append(tabela_ano)   

# 7. Concatenando todas as tabelas anuais em um único DataFrame
df_tabela_historica = pd.concat(lista_tabela_historica, ignore_index=True)

# 8. Reorganizando as colunas para melhor visualização
df_tabela_historica = df_tabela_historica[['Season', 'Posicao', 'Time', 'Pts', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG']]

# 9. Configurando opções de exibição do Pandas para melhor visualização
pd.set_option('display.max_columns', None)  # Exibir todas as colunas
pd.set_option('display.width', None)  # Ajustar a largura de exibição

# 10. Exibindo as primeiras linhas do DataFrame da tabela histórica para verificação
print("\n--- Tabela Historica do Brasileirao ---")
print(df_tabela_historica.head(20))  

# 11. Criar uma função para analisar a trajetória de um time específico ao longo dos ultimos 10 anos

def analisar_trajetoria_time(df_base, nome_time):
    df_time = df_base[df_base['Time'].str.contains(nome_time, case=False, na=False )].copy()
    
    if df_time.empty:
        print(f"\nNenhum dado encontrado para o time {'nome_time'} no periodo de 2015 a 2025.")
        return None
    
    # Engenharia de Atributos: Calculando o aproveitamento (%)
    # Pontos possíveis = total de jogos * 3
    df_time['Pontos_Disputados'] = df_time['J'] * 3
    
    # Aproveitamento = (Pontos Ganhos / Pontos_Disputados) * 100
    df_time['Aproveitamento'] = (df_time['Pts'] / df_time['Pontos_Disputados']) * 100
    
    # Formato para 2 casas decimais
    df_time['Aproveitamento'] = df_time['Aproveitamento'].round(2)
    
    # Removendo a coluna temporária de calculos e organizando as colunas
    df_time = df_time[['Season', 'Posicao', 'Time', 'Pts', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG', 'Aproveitamento']]
    
    # Ordenar por temporada (mais antiga para a mais recente)
    df_time = df_time.sort_values(by='Season').reset_index(drop=True)
    
    return df_time

# 12. Exemplo de uso da função para analisar a trajetória de um time específico
nome_time = "Vasco"  # Substitua pelo nome do time desejado 
trajetoria = analisar_trajetoria_time(df_tabela_historica, nome_time)

if trajetoria is not None:
    print(f"\n--- Trajetoria do time {nome_time} de 2015 a 2025 ---")
    print(trajetoria.to_string(index=False))  # Exibe a tabela sem o índice

# 13. Exemplo de uso da função para calcular a tabela do Brasileirao de 2025    
tabela_2025 = calcular_tabela(df_analise, 2025)

print(f"\n--- Tabela do Brasileirao 2025 ---")
print(tabela_2025)

# 14. Salvar a base analítica para o Power BI
df_tabela_historica.to_excel("analise_brasileirao.xlsx", index=False)
print("\nBase analitica salva como 'analise_brasileirao.xlsx' para uso no Power BI.")