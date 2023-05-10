from socketserver import StreamRequestHandler
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad
import importlib
from base64 import b64decode
import os
import json
from db_api import *
from enum import Enum

class Commands(Enum):
    ADD = "ADD"
    UPDATE = "UPDATE"
    VOTE = "VOTE"
    BYE = "BYE"


class MyHandler(StreamRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024)
        print(f"[CLIENT]: Send: {self.data}")
        if not self.data:
            return
        command = json.loads(self.data)
        if command[0] == Commands.ADD:
            data = command[1]
            print(data["public_key"])
            public_key = data["public_key"].encode()
            add_user(self.db_name, table="voters", fio=data["fio"], public_key=public_key)
        elif command[0] == Commands.UPDATE:
            voters = get_users(self.db_name, "voters")
            voters = [voter["fio"] for voter in voters]
            question = get_valid_election(self.db_name)
            print(question)
            pk = ""
            with open("./server_public_key", "rb") as f:
                pk = RSA.import_key(f.read()).export_key("PEM")
            print(pk)
            message = json.dumps({"voters": voters, "question": question, "public_key": pk.decode()})
            self.request.sendall(message.encode('utf-8'))
        elif command[0] == Commands.VOTE:
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
        elif command[0] == Commands.BYE:
            return
        else:
            print(f'command {command[0]} doesn\'t support')