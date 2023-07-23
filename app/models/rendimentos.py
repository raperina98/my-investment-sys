from peewee import Model, CharField, DateTimeField, UUIDField, DateField, DecimalField, ForeignKeyField
from datetime import datetime

from app.models.movimentos import Movimentos
from database.connection import db
import uuid

class Rendimentos(Model):
    # Campos de controle
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    # Campos
    mes = CharField()

    rendimento_percentual = DecimalField(max_digits=10, decimal_places=5)
    rendimento_valor = DecimalField(max_digits=10, decimal_places=2)

    inflacao_percentual = DecimalField(max_digits=10, decimal_places=5)
    inflacao_valor = DecimalField(max_digits=10, decimal_places=2)

    percentual_liquido = DecimalField(max_digits=10, decimal_places=5)
    liquidez_final = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = 'rendimentos'
        database = db

