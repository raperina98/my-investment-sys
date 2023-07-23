from typing import List

import matplotlib.pyplot as plt
from datetime import datetime


def create_line_graphq(datas, multi_valores: List, labels):
    print(multi_valores)
    # Converter as strings de data para objetos datetime
    datas_formatadas = [datetime.strptime(data, '%Y-%m-%d') for data in datas]

    # Criar o gráfico
    plt.figure(figsize=(10, 6))  # Tamanho do gráfico (opcional)

    # Plotar as linhas de investimentos
    for valores, label in zip(multi_valores, labels):
        if len(valores) == 2:
            valores.append(valores[-1])
        plt.plot(datas_formatadas, valores, label=label, marker='o')
        for x, y in zip(datas_formatadas, valores):
            print('entrou', x, y)
            plt.text(x, y, str(y), ha='right', va='bottom', fontsize=10, color='blue')

    print('saiu?')
    # Configurações do gráfico
    plt.xlabel('Datas')
    plt.ylabel('Valores dos Investimentos')
    plt.title('Desempenho dos Investimentos')
    plt.legend()  # Mostra a legenda com as labels das linhas
    plt.grid(True)  # Adiciona uma grade de fundo (opcional)

    # Configuração das datas no eixo X
    plt.xticks(rotation=45)  # Rotaciona os rótulos das datas para facilitar a leitura

    # Exibir o gráfico
    plt.tight_layout()  # Ajusta o layout para evitar cortes de rótulos
    plt.show()