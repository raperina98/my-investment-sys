from _decimal import Decimal

import requests

def obter_cotacao_dolar():
    # URL da API para obter a cotação do dólar em relação ao Real
    url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'

    # Fazendo a requisição GET à API
    response = requests.get(url)

    # Verifica se a requisição foi bem sucedida (código 200)
    if response.status_code == 200:
        # Transforma a resposta em formato JSON para um dicionário Python
        dados = response.json()

        cotacao_dolar = Decimal(dados['USDBRL']['bid'])
        return cotacao_dolar
    else:
        print(f'Erro na requisição. Código de status: {response.status_code}')
        return None
