import json
import socket
import threading
from PyQt5.QtCore import QObject, pyqtSignal
from .db_api import add_user, create_db, get_valid_election, get_users, find_by_fio, add_user_voice
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import importlib
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
from base64 import b64decode
import os


class ServerError(Exception):
    pass


class Server(QObject):
    finished = pyqtSignal()

    def __init__(self, db_name, passphrase, addr='', port=62000, buffer_size=1024, log=False):
        super().__init__()
        self.is_active = False
        self.buffer_size = buffer_size
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.state = True
        self.db_name = db_name
        self.passphrase = passphrase
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
                command = json.loads(msg)
                if command[0] == "ADD":
                    data = command[1]
                    print(data["public_key"])
                    public_key = data["public_key"].encode()
                    add_user(self.db_name, table="voters", fio=data["fio"], public_key=public_key)
                elif command[0] == "UPDATE":
                    voters = get_users(self.db_name, "current_voters")
                    voters = [voter["fio"] for voter in voters]
                    question = get_valid_election(self.db_name)
                    print(question)
                    pk = ""
                    with open("./server_public_key", "rb") as f:
                        pk = RSA.import_key(f.read()).export_key("PEM")
                    print(pk)
                    message = json.dumps({"voters": voters, "question": question, "public_key": pk.decode()})
                    conn.sendall(message.encode('utf-8'))
                elif command[0] == "VOTE":
                    data = command[1]
                    print(data)
                    fio = data["fio"]
                    question = data["question"]
                    voice, sign = self.decipher(data)
                    users = find_by_fio(self.db_name, "current_voters", fio)
                    print(users)
                    user = users[0]
                    user_public_key = RSA.import_key(user["public_key"])
                    print(f'voice: {voice}, sign: {sign}')
                    print(f'user_public_key: {user_public_key.export_key("PEM")}')
                    pkcs1_15.new(user_public_key).verify(SHA256.new(str(voice).encode()), sign)
                    add_user_voice(db_name=self.db_name, table="voices", fio=fio, question=question, voice=voice.lower())
                elif command[0] == "BYE":
                    break
                else:
                    print(f'command {command[0]} doesn\'t support')

    def decipher(self, encrypted_vote):
        sign = b64decode(encrypted_vote["sign"].encode())
        encrypted_bytes = b64decode(encrypted_vote["encrypted_bytes"].encode())
        encrypted_session_key = b64decode(encrypted_vote["encrypted_session_key"].encode())
        iv = b64decode(encrypted_vote["iv"].encode())
        print(f'sign {sign}')
        private_key = 0
        with open("./server_private_key", "rb") as f:
            private_key = RSA.import_key(f.read(), passphrase=self.passphrase)
        rsa_cipher = PKCS1_OAEP.new(private_key)
        session_key = rsa_cipher.decrypt(encrypted_session_key)
        aes = AES.new(session_key, AES.MODE_CBC, iv)
        print(f'iv: {aes.iv}')
        print(f'session_key: {session_key}')
        decrypted_text = unpad(aes.decrypt(encrypted_bytes), AES.block_size).decode()
        print(decrypted_text)
        return decrypted_text, sign

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
