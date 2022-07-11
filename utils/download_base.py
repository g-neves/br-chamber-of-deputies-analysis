import os 
import requests 
import json

def download_base():
    # Creates the directory where the 
    # data will be stored
    if not 'data' in os.listdir():
        os.mkdir('data')


    BASE_URL = 'https://dadosabertos.camara.leg.br/arquivos/votacoesVotos/json/votacoesVotos-{}.json'
    data_content = os.listdir('./data')

    # Iterates over all years to download the data
    for year in range(2001, 2022+1):
        if f'votacoesVotos-{year}.json' not in data_content:
            r = requests.get(BASE_URL.format(year))

            with open(f'data/votacoesVotos-{year}.json', 'w') as f:
                f.write(r.content.decode())
                print(f"year {year} data saved.")    
