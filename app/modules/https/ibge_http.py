import requests

def obter_dados_ipca(ano, mes):
    # URL da API do IBGE para o IPCA
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.16121/dados?formato=json&dataInicial=01/{mes:02d}/{ano}&dataFinal=30/{mes:02d}/{ano}'

    # Fazendo a requisição GET à API do IBGE
    response = requests.get(url)

    # Verifica se a requisição foi bem sucedida (código 200)
    if response.status_code == 200:
        # Transforma a resposta em formato JSON para um dicionário Python
        dados = response.json()
        return dados[0]
    else:
        print(f'Erro na requisição. Código de status: {response.status_code}')
        return None
