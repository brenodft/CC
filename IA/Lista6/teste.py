import pandas as pd
from apyori import apriori

# Dados extraídos da imagem
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

# Transformar em lista de transações
transacoes = []
for i in range(df.shape[0]):
    transacoes.append([colunas[j] for j in range(df.shape[1]) if df.iloc[i, j] == 'Sim'])

# Aplicar Apriori
regras = apriori(transacoes, min_support=0.3, min_confidence=0.6)
resultados = list(regras)

# Impressão amigável
print("Resposta\n")

for i, item in enumerate(resultados):
    itens = list(item.items)
    print(f"ItemSets {i+1}: {', '.join(itens)}")
    
print("\nRegras:")
for item in resultados:
    for regra in item.ordered_statistics:
        if len(regra.items_base) > 0 and len(regra.items_add) > 0:
            base = ', '.join(regra.items_base)
            adiciona = ', '.join(regra.items_add)
            print(f"{base} => {adiciona} (confiança: {regra.confidence:.2f}, lift: {regra.lift:.2f})")
