import os

HOST = '0.0.0.0'
PORT = 8000
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123456789')
DB_NAME = os.getenv('DB_NAME', 'postgresdb')
DB_TYPE = os.getenv('DB_TYPE', 'postgresql+asyncpg')
