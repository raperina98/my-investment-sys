from peewee import Model, DecimalField, CharField, DateField, DateTimeField, UUIDField, ForeignKeyField
from datetime import datetime
from database.connection import db
import uuid
from .investimentos import Investimentos
from ..utils.custom_enum import CustomEnum


class TipoEnum(CustomEnum):
    ENTRADA = 'ENTRADA'
    SAIDA = 'SAIDA'

class DescricaoEnum(CustomEnum):
    APORTE = 'APORTE'
    RENDIMENTO = 'RENDIMENTO'
    SAQUE = 'SAQUE'

class Movimentos(Model):
    # Campos de controle
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    investimento = ForeignKeyField(Investimentos, backref='movimentos')

    # Campos
    valor = DecimalField(max_digits=10, decimal_places=2)
    valor_antigo = DecimalField(max_digits=10, decimal_places=2)
    valor_novo = DecimalField(max_digits=10, decimal_places=2)
    percentual = DecimalField(max_digits=10, decimal_places=5)

    tipo = CharField(choices=TipoEnum)
    descricao = CharField(choices=DescricaoEnum, null=True)
    data_movimento = DateField(null=True, default=datetime.now)

    def consultar_investimentos_por_tipo(tipo_investimento):
        query = f"SELECT * FROM consultar_investimentos('{tipo_investimento}')"
        return Movimentos.raw(query)

    class Meta:
        database = db
        table_name = 'movimentos'
