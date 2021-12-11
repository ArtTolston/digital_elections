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

    def add_user(self, fio, pub_key):
        command = ("ADD", {"fio": fio, "public_key": pub_key})
        print(json.dumps(command))
        self._send(json.dumps(command).encode('utf-8'))

    def update_info(self):
        command = ("UPDATE",)
        self._send(json.dumps(command).encode('utf-8'))
        response = self._read().decode()
        print(response)
        return json.loads(response)

    def vote(self, var):
        command = ("VOTE", var)
        self._send(json.dumps(command).encode('utf-8'))

    def bye(self):
        command = ("BYE",)
        self._send(json.dumps(command).encode('utf-8'))
