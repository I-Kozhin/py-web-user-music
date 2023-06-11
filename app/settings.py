import socket


def get_server_ip():
    # Получаем имя хоста
    hostname = socket.gethostname()
    # Получаем IP-адрес по имени хоста
    ip_address = socket.gethostbyname(hostname)
    return ip_address


server_ip = get_server_ip()

HOST = '0.0.0.0'
PORT = 8000
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_USER = 'user'
DB_PASSWORD = '123456789'
DB_NAME = 'postgresdb'
DB_TYPE = 'postgresql'
# HOST_OUT = '192.168.85.33'
HOST_OUT = server_ip
