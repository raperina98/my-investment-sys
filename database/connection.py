from peewee import PostgresqlDatabase
from config.db_config import DATABASE

db = PostgresqlDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port'],  
)
