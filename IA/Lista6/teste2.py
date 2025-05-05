import pandas as pd
from apyori import apriori

# Carregar os dados (aqui você pode substituir pelo seu arquivo CSV, se estiver usando um)
dados = [
    ['Não', 'Sim', 'Não', 'Sim', 'Sim', 'Sim', 'Não'],
    ['Sim', 'Não', 'Sim', 'Sim', 'Sim', 'Não', 'Não'],
    ['Não', 'Sim', 'Sim', 'Não', 'Sim', 'Não', 'Sim'],
    ['Sim', 'Sim', 'Não', 'Sim', 'Sim', 'Não', 'Não'],
    ['Não', 'Não', 'Sim', 'Não', 'Não', 'Sim', 'Não'],
    ['Não', 'Não', 'Não', 'Sim', 'Sim', 'Sim', 'Sim'],
    ['Sim', 'Não', 'Sim', 'Sim', 'Não', 'Não', 'Sim'],
    ['Não', 'Sim', 'Não', 'Sim', 'Sim', 'Sim', 'Não'],
    ['Não', 'Não', 'Não', 'Sim', 'Sim', 'Sim', 'Sim'],
    ['Não', 'Não', 'Não', 'Sim', 'Não', 'Sim', 'Não']
]

colunas = ['Leite', 'Café', 'Cerveja', 'Pão', 'Manteiga', 'Arroz', 'Feijão']
df = pd.DataFrame(dados, columns=colunas)

# Preparar transações
transacoes = []
for i in range(df.shape[0]):
    transacoes.append([colunas[j] for j in range(df.shape[1]) if df.iloc[i, j] == 'Sim'])

# Executar Apriori
regras = apriori(transacoes, min_support=0.3, min_confidence=0.6)
resultados = list(regras)

# Imprimir itemsets com seus suportes
print("Itemsets gerados com seus suportes:\n")
for i, item in enumerate(resultados):
    itens = ', '.join(item.items)
    suporte = item.support
    print(f"ItemSet {i+1}: {itens} | Suporte: {suporte:.2f}")
