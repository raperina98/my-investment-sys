from app.models.views import ViewBaterValoresMovimentacao


def verify_movment_value():
    resultado = ViewBaterValoresMovimentacao.select().first()
    print("================================================================")
    print("Investimento:", resultado.investimento, end=" | ")
    print("Movimento:", resultado.movimento, end=" | ")
    print("All Right:", resultado.all_right)
    print("================================================================")