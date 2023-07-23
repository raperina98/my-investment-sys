from peewee import DecimalField, BooleanField, Model, DateField

from database.connection import db


class ViewBaterValoresMovimentacao(Model):
    investimento = DecimalField()
    movimento = DecimalField()
    all_right = BooleanField()

    class Meta:
        database = db
        db_table = 'bater_valores_movimentacao'
        primary_key = False


class ViewRelacaoMontanteTempo(Model):
    data_movimento = DateField()
    valor = DecimalField()

    class Meta:
        database = db
        table_name = 'relacao_montante_tempo'
        primary_key = False
