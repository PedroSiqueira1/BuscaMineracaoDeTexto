
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
- 2° Passo: Se quiser utilizar o Stemmer de Porter, altere nos arquivos **BUSCA.CFG** e **GLI.CFG** dentro da pasta **/config** a configuração de NOSTEMMER para STEMMER.

**BUSCA.CFG**
```
MODELO=modelo.csv
CONSULTAS=consultas.csv
RESULTADOS=RESULTADOS.csv
STEMMER=STEMMER <===
```

**GLI.CFG**
```
LEIA=cf74.xml
LEIA=cf75.xml
LEIA=cf76.xml
LEIA=cf77.xml
LEIA=cf78.xml
LEIA=cf79.xml
ESCREVA=lista.csv
STEMMER=STEMMER <===
```

- 3° Passo: Estando na raiz do projeto, rodar o arquivo main.py que se encontra na pasta src
```
python3 src/main.py
```

## Avaliação

Na pasta **/notebook** temos uma série de análises comparando a diferença dos resultados utilizando o Stemmer de Porter, e não utilizando. As seguintes métricas foram avaliadas:

1. Gráfico de 11 pontos de precisão e recall
2. F1
3. Precision@5
4. Precision@10
5. Histograma de R-Precision (comparativo)
6. MAP
7. MRR
8. Discounted Cumulative Gain (médio)
9. Normalized Discounted Cumulative Gain

Para ver apenas os resultados, acesse o arquivo **RELATORIO.MD** na pasta **/avalia**.

## Etapas do sistema

- Processar o arquivo de consultas para o padrão de palavras que utilizamos
- Criação das listas invertidas
- Criação do modelo vetorial a partir das listas
- Recuperar os documentos com base nas consultas