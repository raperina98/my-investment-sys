from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os

from app.models.investimentos import Investimentos

# Defina o ID da planilha onde você deseja adicionar a nova aba (página)
SPREADSHEET_ID = '1-XuoBB-B_i2Qkgq4DpUWynL3gRNFQBG7c9-l6sbIVKU'

# Defina o nome da nova aba que você quer criar
NEW_SHEET_NAME = 'NovaAba'

# Escopo de acesso necessário (leitura e escrita)
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authorize_google_sheets():
    # Cria o fluxo de autorização OAuth2
    flow = InstalledAppFlow.from_client_secrets_file(
        'credenciais.json', SCOPES
    )

    # Realiza a autorização do usuário e obtém as credenciais
    return flow.run_local_server(port=0)


def insert_data(service, spreadsheet_id, sheet_name, data):
    sheet_range = f'{sheet_name}!A1:Z' + str(len(data))

    value_input_option = 'RAW'

    value_range_body = {
        'values': data
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=sheet_range,
        valueInputOption=value_input_option, body=value_range_body
    ).execute()


def format_table(service,spreadsheet_id, sheet_id, last_column_index):
    # Defina a fórmula personalizada para aplicar a cor em linhas pares
    even_row_formula = "=MOD(ROW(); 2) = 0"

    # Defina a fórmula personalizada para aplicar a cor em linhas ímpares
    odd_row_formula = "=MOD(ROW(); 2) = 1"

    # Defina a cor para linhas pares (vermelho claro)
    even_row_color = {"red": 1.0, "green": 0.9, "blue": 0.9}

    # Defina a cor para linhas ímpares (azul claro)
    odd_row_color = {"red": 0.9, "green": 0.9, "blue": 1.0}

    # Congele a primeira linha (cabeçalho)
    requests = [
            # Congelar a primeira linha
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheet_id,
                        "gridProperties": {
                            "frozenRowCount": 1
                        }
                    },
                    "fields": "gridProperties.frozenRowCount"
                }
            },
            # Deixar a primeira linha em negrito
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": last_column_index
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {
                                "bold": True
                            }
                        }
                    },
                    "fields": "userEnteredFormat.textFormat.bold"
                }
            },
            # Aplicar formatação condicional para cores alternadas
            {
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [
                            {
                                "sheetId": sheet_id,
                                "startRowIndex": 1,
                                "endRowIndex": 1000,  # Substitua pelo número máximo de linhas que você deseja aplicar a formatação
                                "startColumnIndex": 0,
                                "endColumnIndex": last_column_index
                            }
                        ],
                        "booleanRule": {
                            "condition": {
                                "type": "CUSTOM_FORMULA",
                                "values": [
                                    {"userEnteredValue": even_row_formula}
                                ]
                            },
                            "format": {
                                "backgroundColor": even_row_color
                            }
                        }
                    },
                    "index": 0
                }
            }
        ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id, body={'requests': requests}
    ).execute()


def get_sheet_id(service, spreadsheet_id, sheet_name):
    # Obtém a lista de planilhas do arquivo
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])

    for sheet in sheets:
        if sheet['properties']['title'] == sheet_name:
            return sheet['properties']['sheetId']

    return None


# Função para obter os dados da consulta e formatá-los no formato desejado
def obter_dados_formatados():
    colunas = [field for field in Investimentos._meta.fields]
    # Realizando a consulta e obtendo os resultados
    resultados = (Investimentos
                  .select()
                  .order_by(Investimentos.corretora)
                  .tuples())

    # Criando a lista com os resultados formatados
    data = [colunas]
    for pessoa in resultados:
        data.append(list(map(str, pessoa)))

    return data

if __name__ == '__main__':
    data = obter_dados_formatados()
    print(data)

    credentials = authorize_google_sheets()
    service = build('sheets', 'v4', credentials=credentials)




    SHEET_NAME = 'teste'

    SHEET_ID = get_sheet_id(service, SPREADSHEET_ID, SHEET_NAME)

    format_table(service, SPREADSHEET_ID, SHEET_ID, len(data[0]))

    insert_data(service, SPREADSHEET_ID, SHEET_NAME, data)

