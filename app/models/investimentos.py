from peewee import Model, CharField, DecimalField, DateTimeField, UUIDField, DateField
from datetime import datetime
from database.connection import db
import uuid


class Investimentos(Model):
    # Campos de controle
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    # Details
    tipo=CharField()
    detalhes = CharField()
    descricao = CharField()
    corretora = CharField()
    data_inicial = DateField(null=True, default=datetime.now)
    data_vencimento = DateField(null=True)
    aporte_inicial = DecimalField(max_digits=10, decimal_places=2)
    valor_atual = DecimalField(max_digits=10, decimal_places=2)
    objetivo = CharField()


    class Meta:
        database = db
        table_name = 'investimentos'  # Defina o nome da tabela no banco de dados
