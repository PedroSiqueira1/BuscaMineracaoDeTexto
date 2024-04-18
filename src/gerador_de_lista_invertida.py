import logging
import pandas as pd
import xml.etree.ElementTree as ET
from utils import read_config, coalesce

# Configurando o logging
logging.basicConfig(filename='generate_inverted_list.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_inverted_list():
    try:
        # Lendo a configuração do arquivo
        cfg = read_config('./config/GLI.CFG')
        read_files = cfg['LEIA']

        generator_list = {}

        for file in read_files:
            # Lendo o arquivo XML
            tree = ET.parse('./data/' + file)
            root = tree.getroot()

            for record in root:
                record_num = record.find('RECORDNUM').text
                record_text = coalesce(record.find('ABSTRACT'), record.find('EXTRACT'))

                for word in record_text.split():
                    if word in generator_list:
                        generator_list[word].append(record_num)
                    else:
                        generator_list[word] = [record_num]

        generator_list_df = pd.DataFrame({'WORDS': generator_list.keys(), 'RECORDS': generator_list.values()})

        # Escrevendo o resultado no arquivo de saída
        write_path = cfg['ESCREVA'][0]
        generator_list_df.to_csv('./results/' + write_path, index=False, sep=';')

        logging.info("Inverted list generated successfully.")
        return generator_list_df
    except Exception as e:
        logging.error("An error occurred while generating inverted list: %s", str(e))
        raise

try:
    generate_inverted_list()
except Exception as e:
    logging.error("An error occurred: %s", str(e))