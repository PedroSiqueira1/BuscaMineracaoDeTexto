import logging
import pandas as pd
import xml.etree.ElementTree as ET
from utils import read_config, clean_string, get_votes



def generate_consultas(root,files):

    logger = logging.getLogger(__name__)

    logger.info("Generating consultas.")

    try:
        # Create a DataFrame to store the queries
        df_consultas = pd.DataFrame(columns=['QueryNumber', 'QueryText'])

        dict_list = []

        queries_read = 0
        for query in root:
            queries_read+=1
            # Get query number and query text
            query_number = query.find('QueryNumber').text
            query_text = query.find('QueryText').text

            # Clean query text
            query_text = clean_string(query_text)

            dict_list.append({'QueryNumber': query_number, 'QueryText': query_text})
        logger.info(f"Total of queries read: {queries_read}")


        df_consultas = pd.DataFrame(dict_list)

        df_consultas.to_csv('./results/' + files['CONSULTAS'][0], index=False, sep=';')

        logger.info("Generated consultas successfully.")
        
        return df_consultas
    except Exception as e:
        logger.error("Error generating consultas: %s", str(e))
        raise

def generate_esperados(root,files):

    logger = logging.getLogger(__name__)

    logger.info("Generating expected results.")

    try:

        df_esperados = pd.DataFrame(columns=['QueryNumber', 'DocNumber', 'DocVotes'])

        dict_list = []
        docs_read = 0

        for query in root:
            # Get query number and query text
            query_number = query.find('QueryNumber').text
            
            records = query.find('Records')

            for doc in records:
                docs_read+=1
                doc_number = doc.text
                score = doc.attrib.get('score')
                doc_votes = get_votes(score)

                dict_list.append({'QueryNumber': query_number, 'DocNumber': doc_number, 'DocVotes': doc_votes})

        logger.info(f"Total of docs read: {docs_read}")

        df_esperados = pd.DataFrame(dict_list)

        df_esperados.to_csv('./results/' + files['ESPERADOS'][0], index=False, sep=';')
        logger.info("Generated expected results successfully.")
        
        return df_esperados
    except Exception as e:
        logger.error("Error generating esperados: %s", str(e))
        raise

def processador():

    logger = logging.getLogger(__name__)


    # Read the configuration file

    logger.info("Reading the configuration file")

    try:
        files = read_config('./config/PC.CFG')
    except Exception as e:
        logging.error("Error reading configuration file: %s", str(e))
        raise

    # Read the XML file

    logger.info("Reading the score data from queries")

    try:
        tree = ET.parse('./data/' + files['LEIA'][0])
        root = tree.getroot()
    except Exception as e:
        logger.error("Error reading XML file: %s", str(e))
        raise

    generate_consultas(root,files)
    generate_esperados(root,files)
