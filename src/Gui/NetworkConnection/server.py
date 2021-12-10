import json
import socket
import threading
from PyQt5.QtCore import QObject, pyqtSignal
from .db_api import add_user, create_db
import os


class ServerError(Exception):
    pass


class Server(QObject):
    finished = pyqtSignal()

    def __init__(self, db_name, addr='', port=62000, buffer_size=1024, log=False):
        super().__init__()
        self.is_active = False
        self.buffer_size = buffer_size
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.state = True
        self.db_name = db_name
        if not os.path.exists(self.db_name):
            create_db(self.db_name)
        self.state = -1
        try:
            self.socket_server.bind((addr, port))
            self.socket_server.listen(10)
            if log:
                print('[SERVER]: Socket server started and listening at port {}:'.format(port))
        except socket.error as err:
            raise ServerError("Cannot create connection", err)

    def process_request(self, conn, addr):
        with conn:
            print(f'[SERVER]: Connected: {addr}')
            while True:
                msg = conn.recv(self.buffer_size).decode()
                if not msg:
                    break
                data = json.loads(msg)
                conn.sendall(('OK' + data["fio"]).encode('utf-8'))
                if "fio" in data and "public_key" in data:
                    add_user(self.db_name, data["fio"], data["public_key"])
                break

    def run(self):
        self.is_active = True
        while True:
            conn, addr = self.socket_server.accept()
            th = threading.Thread(target=self.process_request,
                                  args=(conn, addr))
            th.start()
            if not self.is_active:
                break
        self.finished.emit()
