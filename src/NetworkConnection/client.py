import json
import socket


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host='192.168.0.7', port=62000, timeout=None, buffer_size=1024):
        self.host = host
        # self.host = '192.168.1.4'
        self.port = port
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.action = None
        host = self.find_server()
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

    def vote(self, encrypted_vote):
        print(encrypted_vote)
        command = ("VOTE", encrypted_vote)
        self._send(json.dumps(command).encode('utf-8'))

    def bye(self):
        command = ("BYE",)
        self._send(json.dumps(command).encode('utf-8'))

    def find_server(self):
        print("find")
        server_addr = ""
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as sock:
            for i in range(9, 1, -1):
                address = f"192.168.0.{i}"
                # address = "127.0.0.1"
                print(f"looking for address: {address}")
                try:

                    sock.connect((address, self.port))
                    print(f"after connect")
                    command = ("HELLO",)
                    sock.sendall(json.dumps(command).encode())
                    print(f"after sendall")
                    response = sock.recv(self.buffer_size)
                    print(f"after recv")
                    code = json.loads(response.decode())
                    if code != "HELLO":
                        print(f"Address {address} is server but not responds correctly")
                        continue
                    print(f"Address {address} is server")
                    server_addr = address
                except socket.error:
                    print(f"Address {address} is not active")
        return server_addr
