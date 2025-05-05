import pandas as pd
from apyori import apriori

# Dados
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

# Preparar transações com presença e ausência
transacoes = []
for _, row in df.iterrows():
    transacao = []
    for col in colunas:
        estado = 'leva' if row[col] == 'Sim' else 'não leva'
        transacao.append(f'{col}_{estado}')
    transacoes.append(transacao)

# Aplicar Apriori
regras = apriori(transacoes, min_support=0.3, min_confidence=0.6)
resultados = list(regras)

# Impressão das regras em linguagem natural
print("Regras de associação em linguagem natural:\n")
for item in resultados:
    for regra in item.ordered_statistics:
        if regra.items_base and regra.items_add:
            base = ', '.join(regra.items_base)
            adiciona = ', '.join(regra.items_add)

            # Transformar em frases mais humanas
            def frase(item):
                nome, estado = item.split('_')
                return f"quem {estado} {nome.lower()}"

            frases_base = [frase(i) for i in regra.items_base]
            frases_add = [frase(i) for i in regra.items_add]

            print(f"{' e '.join(frases_base)} => {' e '.join(frases_add)} "
                  f"(confiança: {regra.confidence:.2f}, lift: {regra.lift:.2f})")
