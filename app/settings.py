import socket

HOST = '0.0.0.0'
PORT = 8000
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_USER = 'user'
DB_PASSWORD = '123456789'
DB_NAME = 'postgresdb'
DB_TYPE = 'postgresql'


# Определение внешнего IP-адреса сервера
def get_server_ip():
    try:
        # Создаем сокет для получения внешнего IP-адреса
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))  # Подключаемся к внешнему серверу (в данном случае используем Google DNS)
        server_ip = sock.getsockname()[0]  # Получаем IP-адрес сервера
        sock.close()
        return server_ip
    except socket.error:
        return "0.0.0.0"  # В случае ошибки возвращаем 0.0.0.0


HOST_OUT = get_server_ip()
