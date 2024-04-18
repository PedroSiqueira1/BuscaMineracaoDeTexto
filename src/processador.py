import logging
import pandas as pd
import xml.etree.ElementTree as ET
from utils import read_config, clean_string, get_votes

# Configure logging
logging.basicConfig(filename='module_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read the configuration file
try:
    files = read_config('./config/PC.CFG')
except Exception as e:
    logging.error("Error reading configuration file: %s", str(e))
    raise

# Read the XML file
try:
    tree = ET.parse('./data/' + files['LEIA'][0])
    root = tree.getroot()
except Exception as e:
    logging.error("Error reading XML file: %s", str(e))
    raise

def generate_consultas():
    try:
        # Create a DataFrame to store the queries
        df_consultas = pd.DataFrame(columns=['QueryNumber', 'QueryText'])

        dict_list = []

        for query in root:
            # Get query number and query text
            query_number = query.find('QueryNumber').text
            query_text = query.find('QueryText').text

            # Clean query text
            query_text = clean_string(query_text)

            dict_list.append({'QueryNumber': query_number, 'QueryText': query_text})

        df_consultas = pd.DataFrame(dict_list)

        df_consultas.to_csv('./results/' + files['CONSULTAS'][0], index=False, sep=';')
        logging.info("Generated consultas successfully.")
        
        return df_consultas
    except Exception as e:
        logging.error("Error generating consultas: %s", str(e))
        raise

def generate_esperados():
    try:
        df_esperados = pd.DataFrame(columns=['QueryNumber', 'DocNumber', 'DocVotes'])

        dict_list = []

        for query in root:
            # Get query number and query text
            query_number = query.find('QueryNumber').text
            
            records = query.find('Records')

            for doc in records:
                doc_number = doc.text
                score = doc.attrib.get('score')
                doc_votes = get_votes(score)

                dict_list.append({'QueryNumber': query_number, 'DocNumber': doc_number, 'DocVotes': doc_votes})

        df_esperados = pd.DataFrame(dict_list)

        df_esperados.to_csv('./results/' + files['ESPERADOS'][0], index=False, sep=';')
        logging.info("Generated esperados successfully.")
        
        return df_esperados
    except Exception as e:
        logging.error("Error generating esperados: %s", str(e))
        raise

# Call the functions
try:
    generate_consultas()
    generate_esperados()
except Exception as e:
    logging.error("An error occurred: %s", str(e))
