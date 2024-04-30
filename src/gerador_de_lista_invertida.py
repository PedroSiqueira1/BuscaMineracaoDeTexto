import logging
import pandas as pd
import xml.etree.ElementTree as ET
from utils import read_config, coalesce
from nltk.stem.porter import PorterStemmer

logger = logging.getLogger(__name__)


def generate_inverted_list():
    try:
        logger.info("Generating inverted list")

        # Lendo a configuração do arquivo

        logger.info("Reading the configuration file")

        cfg = read_config('./config/GLI.CFG')
        read_files = cfg['LEIA']
        use_stemmer = cfg['STEMMER'][0]

        if use_stemmer == "STEMMER":
            stemmer = PorterStemmer()
            logger.info("Using stemmer to generate inverted list")
        generator_list = {}
        
        
        for file in read_files:
            logger.info(f"Reading papers from file {file}")

            # Lendo o arquivo XML
            tree = ET.parse('./data/' + file)
            root = tree.getroot()

            papers_read = 0

            if use_stemmer == "STEMMER":
                for record in root:
                    papers_read+=1
                    record_num = record.find('RECORDNUM').text
                    record_text = coalesce(record.find('ABSTRACT'), record.find('EXTRACT'))
                    for word in record_text.split():
                        word = stemmer.stem(word).upper()
                        if word in generator_list:
                            generator_list[word].append(record_num)
                        else:
                            generator_list[word] = [record_num]
            else:
                for record in root:
                    papers_read+=1
                    record_num = record.find('RECORDNUM').text
                    record_text = coalesce(record.find('ABSTRACT'), record.find('EXTRACT'))
                    for word in record_text.split():
                        if word in generator_list:
                            generator_list[word].append(record_num)
                        else:
                            generator_list[word] = [record_num]
            logger.info(f"Total of papers read: {papers_read}")


        generator_list_df = pd.DataFrame({'WORDS': generator_list.keys(), 'RECORDS': generator_list.values()})

        # Escrevendo o resultado no arquivo de saída
        write_path = cfg['ESCREVA'][0]
        generator_list_df.to_csv('./results/' + write_path, index=False, sep=';')

        logger.info("Inverted list generated successfully.")
        return generator_list_df
    except Exception as e:
        logger.error("An error occurred while generating inverted list: %s", str(e))
        raise

