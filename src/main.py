import subprocess

print("Installing dependencies")

# Define the command
command = ["pip", "install", "-r", "./requirements.txt"]

# Run the command
try:
    subprocess.check_call(command)
    print("Dependencies installed successfully!")
except subprocess.CalledProcessError as e:
    print("Error: Failed to install dependencies:", e)


import processador 
import gerador_de_lista_invertida
import indexador
import buscador
import time 

import logging
logging.root.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

start = time.time()
processador.processador()
end = time.time()
logger.info(f"Time to process queries: {end-start}")

start = time.time()
gerador_de_lista_invertida.generate_inverted_list()
end = time.time()
logger.info(f"Time to generate inverted list: {end-start}")

start = time.time()
indexador.indexador()
end = time.time()
logger.info(f"Time to create vector model: {end-start}")

start = time.time()
buscador.buscador()
end = time.time()
logger.info(f"Time to query: {end-start}")

