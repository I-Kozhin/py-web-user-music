import socket

ip_address = socket.gethostbyname(socket.gethostname())

HOST = '0.0.0.0'
PORT = 8000
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_USER = 'user'
DB_PASSWORD = '123456789'
DB_NAME = 'postgresdb'
DB_TYPE = 'postgresql'
# HOST_OUT = '192.168.85.33'
HOST_OUT = ip_address
