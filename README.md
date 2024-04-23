
# Busca e Mineração De Texto

## Descrição

Este é o repositório da matéria de Busca e Mineração de Texto (COS738), onde foi implementado um sistema de recuperação de informação utilizando Python e a biblioteca de linguagem natural NLTK.

## Requisitos

- Python

### Bibliotecas (Requirements.txt)
- Pandas
- NLTK
- Numpy
- Unidecode


## Como rodar o projeto

- 1° Passo: Clonar o github do projeto
- 2° Passo: Estando na raiz do projeto, rodar o arquivo main.py que se encontra na pasta src
```
python3 src/main.py
```

## Etapas do sistema

- Processar o arquivo de consultas para o padrão de palavras que utilizamos
- Criação das listas invertidas
- Criação do modelo vetorial a partir das listas
- Recuperar os documentos com base nas consultas