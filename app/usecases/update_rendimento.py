from _decimal import Decimal
from peewee import fn
from app.modules.https.ibge_http import obter_dados_ipca
from app.models.movimentos import Movimentos, DescricaoEnum
from app.models.rendimentos import Rendimentos
from app.utils.next_step import next_step


def get_data():
    return Movimentos.select(
        fn.SUM(Movimentos.percentual),
        fn.SUM(Movimentos.valor)
    ) \
        .where(
        Movimentos.descricao == DescricaoEnum.RENDIMENTO,
        (Movimentos.data_movimento.month == 7) & (Movimentos.data_movimento.year == 2023)).tuples().get()


def update_rendimento():
    rendimento_percentual, rendimento_valor = get_data()

    inflacao_percentual = Decimal(obter_dados_ipca(2023, 6)['valor'])

    porcentual_sobre_cotacao = rendimento_percentual - inflacao_percentual

    print(
        f'''rendimento mensal: {rendimento_percentual}%\ncotacao: {inflacao_percentual}%\nporcentual sobre cotação: {porcentual_sobre_cotacao}%''')

    next_step()

    infla = inflacao_percentual * rendimento_valor;
    #
    Rendimentos.create(
        mes='Julho',
        rendimento_percentual=rendimento_percentual,
        rendimento_valor=rendimento_valor,
        inflacao_percentual=inflacao_percentual,
        inflacao_valor=infla,
        percentual_liquido=porcentual_sobre_cotacao,
        liquidez_final=rendimento_valor - infla,
    )
