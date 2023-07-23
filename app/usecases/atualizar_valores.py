import datetime
from _decimal import Decimal

from peewee import fn

from app.modules.https.exchange_http import obter_cotacao_dolar
from app.models.investimentos import Investimentos
from app.models.movimentos import Movimentos, TipoEnum, DescricaoEnum

def escolher_investimento():
    corretora = input('Corretora: ')

    investimentos = Investimentos.select().where(fn.Lower(Investimentos.corretora).contains(corretora.lower())).order_by(Investimentos.corretora.asc()).execute()

    if len(investimentos) == 0:
        raise 'Corretora não encontrada'

    for i, investimento in enumerate(investimentos):
        print(i+1, investimento.corretora, investimento.tipo, investimento.detalhes, investimento.descricao, investimento.valor_atual)

    index_choise = int(input(": "))

    invest_choise = investimentos[index_choise-1];

    print('INVESTIMENTO ESCOLHIDO')
    print(invest_choise.tipo, invest_choise.detalhes, invest_choise.descricao, invest_choise.corretora)
    print(f'O valor atual é {invest_choise.valor_atual}')

    return invest_choise;


def get_current_value(invest_choise: Investimentos) -> Decimal:
    if invest_choise.tipo == 'ATIVO INTERNACIONAL':
        dolar = Decimal(input('Valor em dolar: ').replace(',', '.'))
        c_dolar = obter_cotacao_dolar()
        current_value = dolar * c_dolar
        print(f'O valor convertido para R$ é {current_value} | cotação: {c_dolar} | dolar {dolar}')
        return current_value
    else:
        return Decimal(input('Valor: ').replace(',', '.'))

def execute():
    invest_choise = escolher_investimento()

    update_choise = input('Deseja atualizar o valor? [Y/N]')

    if update_choise == 'Y':
        current_value = get_current_value(invest_choise)

        diferenca = current_value - invest_choise.valor_atual
        percentual = (current_value / invest_choise.valor_atual - 1) * 100

        print('diferença', diferenca, percentual)

        tipo = TipoEnum.ENTRADA if diferenca > 0 else TipoEnum.SAIDA


        input('Finalizar')

        Movimentos.create(
            valor=diferenca,
            valor_antigo=invest_choise.valor_atual,
            valor_novo=current_value,
            percentual=percentual,
            descricao=DescricaoEnum.RENDIMENTO,
            tipo=tipo,
            investimento=invest_choise
        )

        invest_choise.valor_atual = current_value,
        invest_choise.updated_at = datetime.datetime.now()

        invest_choise.save()

execute()