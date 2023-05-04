import threading
from handler import MyHandler
from socketserver import TCPServer




class MultiThreadTCPServer(TCPServer):


    # def decipher(self, encrypted_vote):
    #     sign = b64decode(encrypted_vote["sign"].encode())
    #     encrypted_bytes = b64decode(encrypted_vote["encrypted_bytes"].encode())
    #     encrypted_session_key = b64decode(encrypted_vote["encrypted_session_key"].encode())
    #     iv = b64decode(encrypted_vote["iv"].encode())
    #     print(f'sign {sign}')
    #     private_key = 0
    #     with open("./server_private_key", "rb") as f:
    #         private_key = RSA.import_key(f.read(), passphrase=self.passphrase)
    #     rsa_cipher = PKCS1_OAEP.new(private_key)
    #     session_key = rsa_cipher.decrypt(encrypted_session_key)
    #     aes = AES.new(session_key, AES.MODE_CBC, iv)
    #     print(f'iv: {aes.iv}')
    #     print(f'session_key: {session_key}')
    #     decrypted_text = unpad(aes.decrypt(encrypted_bytes), AES.block_size).decode()
    #     print(decrypted_text)
    #     return decrypted_text, sign


    def run(self):
        self.is_active = True
        while True:
            conn, addr = self.get_request()
            th = threading.Thread(target=self.process_request,
                                  args=(conn, addr))
            th.start()
            if not self.is_active:
                break


host = "localhost"
port = 10000
addr = (host, port)



if __name__ == "__main__":
    myserver = MultiThreadTCPServer(addr, MyHandler)
    myserver.run()