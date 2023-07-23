import os

DATABASE = {
    'engine': 'postgresql',
    'host':  os.environ.get('DB_HOST', 'localhost'),   
    'user': os.environ.get('DB_USER', 'admin'),  
    'password': os.environ.get('DB_PASS', 'admin'), 
    'name': os.environ.get('DB_NAME', 'db-invest-perina'),
    'port': os.environ.get('DB_PORT', 5432)
}
