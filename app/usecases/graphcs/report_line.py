from typing import List
from app.models.investimentos import Investimentos
from app.models.movimentos import Movimentos
from app.models.views import ViewRelacaoMontanteTempo
from app.modules.graphcs.graphcs import create_line_graphq


def get_values(data: List):
    array = [m.valor for m in data];
    array.insert(0, 0.00)
    return array


def grafico_de_historico_montante():
    movimentos = ViewRelacaoMontanteTempo().select().execute()
    tipos_unicos = Investimentos.select(Investimentos.tipo).distinct().execute()

    tipos_unicos = [str(t.tipo) for t in tipos_unicos]

    valores = [m.valor for m in movimentos]
    data_movimento = [str(m.data_movimento) for m in movimentos]

    valores.insert(0, 0.00)
    data_movimento.insert(0, '2023-07-10')

    all_valores = [valores]

    for tipo in tipos_unicos:
        all_valores.append(get_values(Movimentos.consultar_investimentos_por_tipo(tipo)))

    tipos_unicos.insert(0, 'Geral')

    create_line_graphq(data_movimento, all_valores, tipos_unicos)