import configparser
from unidecode import unidecode


def read_config(file:str) -> dict:
    data = {}
    with open(file, 'r') as cfg_file:
        for line in cfg_file:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=')

                if key in data.keys():
                    data[key].append(value)
                else:
                    data[key] = [value]

    return data


def clean_string(text:str) -> str:
    return unidecode(text.replace(';', '').upper())

def get_votes(string:str) -> int:
    
    votes = string.strip()
    count = 0
    for vote in votes:
        count += int(vote)
    return count

def coalesce(*args):
    for arg in args:
        if arg is not None:
            return unidecode(arg.text).upper()
    return '' 