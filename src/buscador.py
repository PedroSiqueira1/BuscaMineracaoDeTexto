import logging
import pandas as pd
import xml.etree.ElementTree as ET
from utils import read_config, similarity
from nltk.tokenize import RegexpTokenizer
import numpy as np


logger = logging.getLogger(__name__)


def buscador():

    logger.info("Searching queries.")


    try:

        logger.info("Reading the configuration file")
        config = read_config('./config/BUSCA.CFG')


        weight_files = config['MODELO']
        consultas_files = config['CONSULTAS']

        logger.info("Reading the vector model file")

        modelo = pd.read_csv('./results/' + weight_files[0], sep=';')
        modelo.set_index('Unnamed: 0', inplace=True)
        modelo.rename_axis("DocID", inplace=True)

        logger.info(f"Total of {modelo.shape[0]} weights for {modelo.shape[1]} words in vector model")


        logger.info("Reading the queries to be searched")

        consultas = pd.read_csv('./results/' + consultas_files[0], sep=';', dtype=str)

        logger.info(f"Total of queries read: {consultas.shape[0]}")

        tokenizer = RegexpTokenizer(r'[a-zA-Z]{2,}')

        query_tokens = [tokenizer.tokenize(word) for word in consultas['QueryText']]
        query_results = pd.DataFrame(consultas['QueryNumber'], columns=['QueryNumber'], dtype=str)


        dict = {'QueryNumber': [], 'Results':[]}
        for i in range(len(query_tokens)):
            document_matrix = modelo.loc[:,modelo.columns.isin(query_tokens[i])]
            query_vector = np.ones(len(document_matrix.columns))
            
            similar_documents = similarity(document_matrix, query_vector)
            similar_documents.sort_values(ascending=False,inplace=True)
            rank = similar_documents.rank(ascending=False)
            for j in range(len(modelo)):
                dict['QueryNumber'].append(query_results.iloc[i,0])
                dict['Results'].append([rank.iloc[j],similar_documents.index[j],similar_documents.iloc[j]])

        
        df = pd.DataFrame.from_dict(dict)

        query_documents = config['RESULTADOS']
        df.to_csv('./results/' + query_documents[0], sep=';', index=False)

        logger.info("Searched queries successfully.")

    except Exception as e:
        logger.error("An error occurred while searching queries: %s", str(e))
        raise
