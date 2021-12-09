import json
import socket
import threading


class ServerError(Exception):
    pass


class Server:
    def __init__(self, addr='127.0.0.1', port=62000, buffer_size=1024, log=False):
        self.buffer_size = buffer_size
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.state = True
        try:
            self.socket_server.bind((addr, port))
            self.socket_server.listen()
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
                # PAYLOAD CODE HERE ###########################################
                data = json.loads(msg)
                conn.sendall(('OK' + data["fio"]).encode('utf-8'))
                ###############################################################
                break

    def run(self):
        while True:
            conn, addr = self.socket_server.accept()
            th = threading.Thread(target=self.process_request,
                                  args=(conn, addr))
            th.start()
            if not self.state:
                return 0
