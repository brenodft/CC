import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle
from sklearn.ensemble import RandomForestClassifier
from skopt import BayesSearchCV
from skopt.space import Integer, Real, Categorical
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# * =======================================
# * Aluno: Breno Pires Santos
# * Matrícula: 808238
# * =======================================

# * =======================================
# * Configurações de execução
# * =======================================

executar_analise = False  # Define se a análise inicial será feita
mostrar_log = True  # Controla a exibição de logs

# * =======================================
# * Carregamento de arquivos
# * =======================================

dados_treino = pd.read_csv('titanic/train.csv')
dados_teste = pd.read_csv('titanic/test.csv')
respostas_oficiais = pd.read_csv('titanic/gender_submission.csv')

# Inserindo coluna alvo vazia para manter formato consistente
dados_teste.insert(0, 'Survived', np.nan)

# * =======================================
# * Análise exploratória (opcional)
# * =======================================

if executar_analise:
    print("Treino:", dados_treino.head())
    print("\nTeste:", dados_teste.head())
    print("\nGabarito:", respostas_oficiais.head())
    print("\nResumo estatístico:", dados_treino.describe())
    print("\nAusentes (treino):", dados_treino.isnull().sum())
    print("Distribuição 'Survived':", dados_treino['Survived'].value_counts(normalize=True))

# * =======================================
# * Tratamento de dados
# * =======================================

remover_colunas = ['PassengerId', 'Name', 'SibSp', 'Parch', 'Ticket', 'Cabin', 'Embarked']
if mostrar_log:
    print("\nColunas descartadas:", remover_colunas)

# Preenchendo ausências com média
for col in ['Age', 'Fare']:
    dados_treino[col].fillna(dados_treino[col].mean(), inplace=True)
    dados_teste[col].fillna(dados_teste[col].mean(), inplace=True)

# Codificação da variável categórica
le = LabelEncoder()
dados_treino['Sex'] = le.fit_transform(dados_treino['Sex'])
dados_teste['Sex'] = le.transform(dados_teste['Sex'])

# Criando features auxiliares
dados_treino['TamanhoFamilia'] = dados_treino['SibSp'] + dados_treino['Parch'] + 1
dados_treino['Sozinho'] = (dados_treino['TamanhoFamilia'] == 1).astype(int)
dados_teste['TamanhoFamilia'] = dados_teste['SibSp'] + dados_teste['Parch'] + 1
dados_teste['Sozinho'] = (dados_teste['TamanhoFamilia'] == 1).astype(int)

# Normalização de valores
normalizador = StandardScaler()
dados_treino[['Age', 'Fare', 'TamanhoFamilia']] = normalizador.fit_transform(dados_treino[['Age', 'Fare', 'TamanhoFamilia']])
dados_teste[['Age', 'Fare', 'TamanhoFamilia']] = normalizador.transform(dados_teste[['Age', 'Fare', 'TamanhoFamilia']])

# Remoção final de colunas
for df in [dados_treino, dados_teste]:
    df.drop(columns=remover_colunas, inplace=True)

# * =======================================
# * Salvando arquivos intermediários
# * =======================================

dados_treino.to_csv('titanic/preparado_treino.csv', index=False)
dados_teste.to_csv('titanic/preparado_teste.csv', index=False)

# * =======================================
# * Divisão de conjuntos
# * =======================================

entradas_treino = dados_treino.drop(columns=['Survived'])
rotulos_treino = dados_treino['Survived']
entradas_teste = dados_teste.drop(columns=['Survived'])
rotulos_teste = respostas_oficiais['Survived']

with open('titanic/conjuntos_treino_teste.pkl', 'wb') as arquivo:
    pickle.dump((entradas_treino, rotulos_treino, entradas_teste, rotulos_teste), arquivo)

# * =======================================
# * Ajuste de hiperparâmetros
# * =======================================

floresta = RandomForestClassifier(random_state=42)
espaco_rf = {
    'n_estimators': Integer(100, 1000),
    'max_depth': Integer(3, 30),
    'min_samples_split': Integer(2, 20),
    'min_samples_leaf': Integer(1, 20),
    'max_features': Categorical(['sqrt', 'log2', None]),
    'bootstrap': Categorical([True, False])
}
busca_rf = BayesSearchCV(
    estimator=floresta,
    search_spaces=espaco_rf,
    n_iter=50,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)
busca_rf.fit(entradas_treino, rotulos_treino)

melhores_param_rf = busca_rf.best_params_
melhor_modelo_rf = busca_rf.best_estimator_
if mostrar_log:
    print("\nRandom Forest ajustado:", melhores_param_rf)

# MLP
rede = MLPClassifier(max_iter=1000, random_state=42)
espaco_mlp = {
    'hidden_layer_sizes': Integer(5, 500),
    'activation': Categorical(['tanh', 'relu']),
    'solver': Categorical(['adam', 'sgd']),
    'alpha': Real(1e-5, 1e-1, prior='log-uniform'),
    'learning_rate_init': Real(1e-4, 1e-1, prior='log-uniform')
}
busca_mlp = BayesSearchCV(
    estimator=rede,
    search_spaces=espaco_mlp,
    n_iter=50,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    random_state=42
)
busca_mlp.fit(entradas_treino, rotulos_treino)

melhores_param_mlp = busca_mlp.best_params_
melhor_modelo_mlp = busca_mlp.best_estimator_
if mostrar_log:
    print("\nMLP ajustado:", melhores_param_mlp)

# * =======================================
# * Avaliação dos modelos treinados
# * =======================================

modelo_rf_final = RandomForestClassifier(**melhores_param_rf, random_state=42)
modelo_rf_final.fit(entradas_treino, rotulos_treino)

previsoes_rf = modelo_rf_final.predict(entradas_teste)
if mostrar_log:
    print("\nDesempenho Random Forest:")
    print("Acurácia:", accuracy_score(rotulos_teste, previsoes_rf))
    print(classification_report(rotulos_teste, previsoes_rf))
    print(confusion_matrix(rotulos_teste, previsoes_rf))
