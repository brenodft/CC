#!/bin/bash

echo "==========================================="
echo "       Dogs vs Cats - Organizando Dataset"
echo "==========================================="
echo
echo "Este script ajuda a preparar o dataset Dogs vs Cats automaticamente."
echo
echo "PASSO 1: Faça o download manual do arquivo 'dogs-vs-cats.zip' no Kaggle:"
echo
echo "https://www.kaggle.com/c/dogs-vs-cats/data"
echo
echo "PASSO 2: Copie o arquivo 'dogs-vs-cats.zip' para a pasta do projeto."
echo
read -p "Pressione ENTER quando o arquivo estiver no diretório para continuar..."

ZIP_FILE="dogs-vs-cats.zip"
DATA_DIR="dataset"

# Criar diretório dataset/ caso não exista
if [ ! -d "$DATA_DIR" ]; then
    mkdir "$DATA_DIR"
    echo "Diretório '$DATA_DIR/' criado com sucesso."
fi

# Mover o zip para dataset/ se estiver no diretório atual
if [ -f "$ZIP_FILE" ]; then
    mv "$ZIP_FILE" "$DATA_DIR/"
    echo "Arquivo '$ZIP_FILE' movido para '$DATA_DIR/'."
fi

# Verificar se o arquivo zip está na pasta dataset/
if [ ! -f "$DATA_DIR/$ZIP_FILE" ]; then
    echo "ERRO: '$ZIP_FILE' não encontrado dentro de '$DATA_DIR/'."
    echo "Por favor, refaça os PASSOS 1 e 2."
    exit 1
fi

cd "$DATA_DIR" || exit

echo
echo "Agora vamos extrair o arquivo principal dogs-vs-cats.zip."
read -p "Aperte ENTER para iniciar a extração..."

# Descompactar o arquivo principal se train.zip ou test1.zip não existirem
if [ ! -f "train.zip" ] || [ ! -f "test1.zip" ]; then
    echo "Extraindo conteúdo de dogs-vs-cats.zip..."
    unzip -q -o dogs-vs-cats.zip
else
    echo "Os arquivos train.zip e test1.zip já estão presentes. Pulando extração."
fi

echo
echo "Agora vamos extrair o arquivo train.zip."
read -p "Pressione ENTER para continuar..."

# Extrair train.zip diretamente para a pasta train/
if [ -f "train.zip" ]; then
    mkdir -p train
    echo "Extraindo train.zip para a pasta train/ sem subpastas adicionais..."
    unzip -q -j train.zip -d train
    echo "Extração do train.zip concluída."
else
    echo "ERRO: train.zip não foi encontrado após a extração."
    exit 1
fi

echo
echo "Vamos extrair agora o arquivo test1.zip."
read -p "Pressione ENTER para continuar..."

# Extrair test1.zip diretamente para a pasta test1/
if [ -f "test1.zip" ]; then
    mkdir -p test1
    echo "Extraindo test1.zip para a pasta test1/ sem subpastas extras..."
    unzip -q -j test1.zip -d test1
    echo "Extração do test1.zip concluída."
else
    echo "ERRO: test1.zip não foi encontrado após a extração."
    exit 1
fi

# Perguntar sobre remoção dos arquivos zip
echo
read -p "Deseja apagar os arquivos ZIP para liberar espaço? (s/n): " resposta
if [[ "$resposta" =~ ^[Ss]$ ]]; then
    echo "Removendo arquivos ZIP..."
    rm -f dogs-vs-cats.zip train.zip test1.zip
    echo "Arquivos ZIP excluídos."
else
    echo "Arquivos ZIP mantidos no disco."
fi

echo
echo "Dataset pronto! As imagens de treino estão em '$DATA_DIR/train/' e as de teste em '$DATA_DIR/test1/'."
