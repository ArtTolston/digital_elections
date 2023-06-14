import json
import socket
import ipaddress


class ClientError(Exception):
    pass


class Client:
    def __init__(self, port=62000, timeout=None, buffer_size=1024):
        self.port = port
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.action = None
        self.host = self.find_server()
        print("here")
        try:
            self.connection = socket.create_connection((self.host, self.port), timeout)
            print("here2")
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

    def check_user(self, fio):
        command = ("CHECK", {"fio": fio})
        print(json.dumps(command))
        self._send(json.dumps(command).encode('utf-8'))
        response = self._read().decode()
        print(response)
        return response

    def update_info(self):
        command = ("UPDATE",)
        self._send(json.dumps(command).encode('utf-8'))
        response = self._read().decode()
        print(response)
        return json.loads(response)

    def vote(self, encrypted_vote):
        print(encrypted_vote)
        command = ("VOTE", encrypted_vote)
        self._send(json.dumps(command).encode('utf-8'))

    def bye(self):
        command = ("BYE",)
        self._send(json.dumps(command).encode('utf-8'))

    def find_server(self):
        print("find")
        print(socket.INADDR_BROADCAST)
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        s.sendto("HELLO SERVER".encode("utf-8"), (str(socket.INADDR_BROADCAST), self.port))
        # s.bind(("" ,self.port))
        while True:
            data, addr = s.recvfrom(self.buffer_size)
            if data.decode() == "ITS YOUR SERVER":
                server_addr = str(addr[0])
                return server_addr

