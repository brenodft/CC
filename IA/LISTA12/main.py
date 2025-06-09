# -*- coding: utf-8 -*-

import os
import math
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer, Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, precision_score, balanced_accuracy_score

# Parâmetros principais do projeto
IMAGE_DIMENSIONS = (150, 150)  # Dimensão padrão para redimensionar as imagens para entrada da CNN
BATCH_SZ = 32                  # Número de imagens processadas por batch durante o treinamento
MAX_EPOCHS = 25                # Número máximo de épocas para o treinamento do modelo
BASE_DIR = "dataset"           # Diretório base onde estão os dados organizados

def preparar_dados():
    """
    Função para preparar os dados:
    - Garante que as pastas necessárias existem (train, test1, external_test).
    - Lê os nomes dos arquivos de imagens da pasta de treino.
    - Cria labels a partir do nome dos arquivos ('cat' ou 'dog').
    - Cria um DataFrame pandas para facilitar manipulação dos dados.
    - Divide os dados em treino (70%), validação (15%) e teste (15%) com stratificação para balancear as classes.
    """

    # Cria diretórios caso não existam, para evitar erros posteriores
    for subfolder in ['train', 'test1', 'external_test']:
        full_path = os.path.join(BASE_DIR, subfolder)
        if not os.path.isdir(full_path):
            os.makedirs(full_path)
            print(f"Diretório criado: {full_path}")

    print(">>> Iniciando preparação dos dados...")

    # Lista todos os arquivos jpg da pasta de treino
    filenames = [f for f in os.listdir(os.path.join(BASE_DIR, 'train')) if f.endswith('.jpg')]

    # Define os rótulos a partir do prefixo do nome do arquivo (cat/dog)
    labels = ['cat' if name.startswith('cat') else 'dog' for name in filenames]

    # Cria DataFrame para manipular dados mais facilmente
    df = pd.DataFrame({'filename': filenames, 'label': labels})

    # Divide os dados em treino (70%) e um conjunto temporário (30%)
    # A stratificação garante que a proporção de gatos e cães seja mantida em cada conjunto
    treino_df, temp_df = train_test_split(
        df,
        test_size=0.3,
        stratify=df['label'],
        random_state=42
    )

    # Divide o conjunto temporário igualmente em validação (15%) e teste (15%)
    valid_df, teste_df = train_test_split(
        temp_df,
        test_size=0.5,
        stratify=temp_df['label'],
        random_state=42
    )

    print(f"Quantidade - Treino: {len(treino_df)} | Validação: {len(valid_df)} | Teste: {len(teste_df)}\n")

    return treino_df, valid_df, teste_df

def gerar_generators(treino_df, valid_df, teste_df):
    """
    Configura geradores de dados para alimentar a CNN.
    Para o conjunto de treino, aplica técnicas de aumento de dados para melhorar generalização.
    Para validação e teste, apenas normaliza as imagens.
    """

    print(">>> Configurando geradores de imagens...")

    # Data augmentation para o conjunto de treino - aumenta a variedade das imagens gerando variações
    augmentacao_treino = ImageDataGenerator(
        rescale=1./255,           # Normaliza os pixels para valores entre 0 e 1
        rotation_range=40,        # Rotaciona imagens até 40 graus
        width_shift_range=0.2,    # Translada horizontalmente até 20%
        height_shift_range=0.2,   # Translada verticalmente até 20%
        shear_range=0.2,          # Aplica cisalhamento geométrico
        zoom_range=0.2,           # Aplica zoom aleatório
        horizontal_flip=True,     # Espelha horizontalmente aleatoriamente
        fill_mode='nearest'       # Preenche pixels vazios após transformações
    )

    # Apenas normalização para validação e teste, sem aumento
    sem_augmentacao = ImageDataGenerator(rescale=1./255)

    # Gerador de imagens para treino com aumento de dados
    treino_gen = augmentacao_treino.flow_from_dataframe(
        dataframe=treino_df,
        directory=os.path.join(BASE_DIR, 'train'),
        x_col='filename',
        y_col='label',
        target_size=IMAGE_DIMENSIONS,
        batch_size=BATCH_SZ,
        class_mode='binary'       # Classificação binária (gato ou cachorro)
    )

    # Geradores de validação e teste apenas com normalização
    valid_gen = sem_augmentacao.flow_from_dataframe(
        dataframe=valid_df,
        directory=os.path.join(BASE_DIR, 'train'),
        x_col='filename',
        y_col='label',
        target_size=IMAGE_DIMENSIONS,
        batch_size=BATCH_SZ,
        class_mode='binary'
    )
    teste_gen = sem_augmentacao.flow_from_dataframe(
        dataframe=teste_df,
        directory=os.path.join(BASE_DIR, 'train'),
        x_col='filename',
        y_col='label',
        target_size=IMAGE_DIMENSIONS,
        batch_size=BATCH_SZ,
        class_mode='binary',
        shuffle=False  # Para manter ordem durante avaliação
    )

    return treino_gen, valid_gen, teste_gen

def criar_modelo_cnn():
    """
    Cria a arquitetura da rede neural convolucional (CNN).
    Utiliza 3 blocos Conv2D + MaxPooling para extrair características das imagens.
    Após isso, as camadas Flatten e Dense realizam a classificação final.
    O Dropout é utilizado para reduzir overfitting.
    """

    print(">>> Construindo o modelo CNN...")

    model = Sequential()

    # Camada de entrada, especificando o formato da imagem
    model.add(InputLayer(input_shape=(IMAGE_DIMENSIONS[0], IMAGE_DIMENSIONS[1], 3)))

    # Primeiro bloco convolucional + pooling
    model.add(Conv2D(32, (3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    # Segundo bloco convolucional + pooling com mais filtros
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    # Terceiro bloco convolucional + pooling com ainda mais filtros
    model.add(Conv2D(128, (3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    # Achata os mapas de características para vetor 1D
    model.add(Flatten())

    # Camada densa totalmente conectada para aprendizado de representações complexas
    model.add(Dense(512, activation='relu'))

    # Dropout de 50% para reduzir overfitting (desliga neurônios aleatoriamente)
    model.add(Dropout(0.5))

    # Camada de saída com ativação sigmoid para classificação binária
    model.add(Dense(1, activation='sigmoid'))

    # Compila o modelo com otimizador Adam e função de perda binária
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    return model

def plotar_graficos(hist):
    """
    Gera gráficos que mostram a evolução da acurácia e do loss durante o treinamento,
    tanto para o conjunto de treino quanto para o de validação.
    """

    print(">>> Gerando gráficos de treinamento...")

    plt.figure(figsize=(14, 6))

    # Gráfico da acurácia por época
    plt.subplot(1, 2, 1)
    plt.plot(hist.history['accuracy'], marker='o', label='Treino')
    plt.plot(hist.history['val_accuracy'], marker='s', label='Validação')
    plt.title('Acurácia ao Longo das Épocas')
    plt.xlabel('Épocas')
    plt.ylabel('Acurácia')
    plt.legend()
    plt.grid(True)

    # Gráfico do loss por época
    plt.subplot(1, 2, 2)
    plt.plot(hist.history['loss'], marker='o', label='Treino')
    plt.plot(hist.history['val_loss'], marker='s', label='Validação')
    plt.title('Loss ao Longo das Épocas')
    plt.xlabel('Épocas')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('metricas_treinamento.png')
    plt.show()

def main():
    # 1. Preparar os dados e separar em treino, validação e teste
    treino_df, valid_df, teste_df = preparar_dados()

    # 2. Criar os geradores de dados para alimentar o modelo
    treino_gen, valid_gen, teste_gen = gerar_generators(treino_df, valid_df, teste_df)

    # 3. Construir a rede neural convolucional
    modelo = criar_modelo_cnn()
    modelo.summary()  # Imprime resumo da arquitetura da rede

    print(">>> Iniciando treinamento...")

    # Callbacks para evitar overfitting e salvar o melhor modelo
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    checkpoint = ModelCheckpoint('melhor_modelo.keras', monitor='val_accuracy', save_best_only=True)

    # Calcula o número de passos por época para treino e validação
    steps_train = math.ceil(len(treino_df) / BATCH_SZ)
    steps_val = math.ceil(len(valid_df) / BATCH_SZ)

    # 4. Treinamento do modelo
    historico = modelo.fit(
        treino_gen,
        steps_per_epoch=steps_train,
        validation_data=valid_gen,
        validation_steps=steps_val,
        epochs=MAX_EPOCHS,
        callbacks=[early_stop, checkpoint]
    )

    # 5. Plotar gráficos de desempenho do treinamento
    plotar_graficos(historico)

    print(">>> Avaliando modelo no conjunto de teste...")

    # Avaliação final no conjunto de teste
    perda, acuracia = modelo.evaluate(teste_gen)

    # Predição das classes no conjunto de teste (limiar 0.5)
    predicoes = (modelo.predict(teste_gen) > 0.5).astype(int).flatten()

    # Métricas adicionais para avaliação
    acc_balanceada = balanced_accuracy_score(teste_gen.classes, predicoes)
    prec_global = precision_score(teste_gen.classes, predicoes)

    print(f"\nAcurácia no conjunto de teste: {acuracia:.2%}")
    print(f"Precisão geral: {prec_global:.2%}")
    print(f"Acurácia balanceada: {acc_balanceada:.2%}\n")

    # Relatório detalhado com precisão, recall e f1-score por classe
    print("Relatório de classificação detalhado:")
    print(classification_report(teste_gen.classes, predicoes, target_names=['gatos', 'cães']))

    # Salva o modelo final treinado para uso futuro
    modelo.save('modelo_final_dogs_vs_cats.keras')
    print("\nModelo salvo em 'modelo_final_dogs_vs_cats.keras'")

if __name__ == '__main__':
    main()
