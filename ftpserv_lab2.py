import os
import sys
import pyftpdlib

from hashlib import md5

from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed

# Обработчик запросов 
class MyHandler(FTPHandler):

    # Клиент подключается
    def on_connect(self):
        print("%s:%s connected" % (self.remote_ip, self.remote_port))
        
    # Клиент отключается
    def on_disconnect(self):
        print("%s:%s disconnected" % (self.remote_ip, self.remote_port))
        
    # Клиент загружает файл
    def on_file_sent(self, file):
        try:
            with open(path, 'rb') as file:
                response = ftp.storbinary('STOR ' + path, file, 1024)
                print(response)
                file.close()
        except:
            print("Internal exception: " + str(sys.exc_info()[0]))
            
    # Клиент скачивает файл
    def on_file_received(self, file):
        try:
            response = ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
            print(response)
        except:
            print("Internal exception: " + str(sys.exc_info()[0]))
            
    # Клиент удаляет файл
    def on_incomplete_file_received(self, file):
        os.remove(file)
        
# Менеджер пользователей 
class DummyMD5Authorizer(DummyAuthorizer):

    # Авторизация пользователя
    def validate_authentication(self, username, password, handler):
        hash = md5(password.encode('latin1')).hexdigest()
        try:
            if username != 'anonymous' and self.user_table[username]['pwd'] != hash:
                raise KeyError
            print("AuthenticationSuccess")
        except KeyError:
            raise AuthenticationFailed
        
# Инициализация сервера 
def main():
    authorizer = DummyMD5Authorizer()
    authorizer.add_user('user', md5('12345'.encode('latin1')).hexdigest(), 'root', perm='elradfmwMT')
    authorizer.add_user('anonymous', md5(''.encode('latin1')).hexdigest(), 'root', perm='elr')

    handler = MyHandler
    handler.authorizer = authorizer

    server = FTPServer(('0.0.0.0', 2121), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
