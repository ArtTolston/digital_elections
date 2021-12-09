import json
import socket


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host='127.0.0.1', port=62000, timeout=None, buffer_size=1024):
        self.host = host
        # self.host = '192.168.1.4'
        self.port = port
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.action = None
        try:
            self.connection = socket.create_connection((self.host, self.port), timeout)
        except socket.error as err:
            raise ClientError("[Client]: Cannot create connection", err)

    def _send(self, data):
        try:
            self.connection.sendall(data)
        except socket.error as err:
            raise ClientError("Error sending data to server", err)

    def _read(self):
        try:
            data = self.connection.recv(self.buffer_size)
        except socket.error as err:
            raise ClientError("Error reading data from socket", err)
        return data

    def setAction(self, button):
        self.action = button

    def add_user(self, fio, pub_key):
        data = {"fio": fio, "key": pub_key}
        self._send(json.dumps(data).encode('utf-8'))
        response = self._read().decode()
        if not response.startswith('OK'):
            print('Incorrect response!')
        print(response)
        # return response

    def update_info(self):


    # def run(self):
    #     while True:
    #         match self.action:
    #             case "add_user":
    #                 self.add_user(fio, pub_key)
    #             case _:
    #                 raise ClientError("Incorrect request from client")
