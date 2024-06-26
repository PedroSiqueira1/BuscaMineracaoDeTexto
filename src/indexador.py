import pandas as pd
from collections import Counter
import numpy as np
import re
from utils import read_config
import logging


logger = logging.getLogger(__name__)

def indexador():


    try:
        # Regex to transform base, only pick words with 2 or more letters, and only words made by letters
        regex = r'^[a-zA-Z]{2,}$'

        logger.info("Reading the configuration file")

        config = read_config('./config/INDEX.CFG')

        read_files = config['LEIA']
        write_files = config['ESCREVA']

        logger.info("Reading inverted list")
        list_of_words = pd.read_csv('./results/' + read_files[0], sep=';')

        logger.info(f"Total of words read: {list_of_words.shape[0]}")

        logger.info("Creating vector model.")

        max_freq_term = {}
        nis = {}
        freq_words = {}
        weights = {}

        for index, row in list_of_words.iterrows():
            word = row['WORDS']

            if re.search(regex, str(word)) == None:
                continue
            docs = eval(row['RECORDS'])
            doc_appearences= Counter(docs)

            # Number of documents containing word
            nis[word] = len(doc_appearences.keys())

            freq_words[word] = doc_appearences
            for doc in doc_appearences.keys():
                if doc in max_freq_term.keys():
                    max_freq_term[doc] = max(max_freq_term[doc], doc_appearences[doc])
                else:
                    max_freq_term[doc] = doc_appearences[doc]
            
        # Total number of documents in the system
        N = len(max_freq_term.keys())

        for word in nis.keys():
            for doc in max_freq_term.keys():
                # Normalized frequency of word in doc
                fij = freq_words[word].get(doc,0)/max_freq_term[doc]

                # Inverse document frequency
                idf = np.log(N/nis[word])

                weight = fij * idf

                if word in weights.keys():
                    weights[word][doc] = weight
                else:
                    weights[word] = {doc: weight}

        # Create data frame
        weights_df = pd.DataFrame(columns=list(weights.keys()), index=list(max_freq_term.keys()))

        # Add data
        for word in weights.keys():
            weights_df[word] = list(weights[word].values())

        # Save as csv
        weights_df.to_csv('./results/' + write_files[0], sep=';')

        logger.info("Generated vector model.")

    
    except Exception as e:
        logger.error("An error occurred while generating index: %s", str(e))
        raise
