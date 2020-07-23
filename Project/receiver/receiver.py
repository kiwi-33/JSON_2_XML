import os, requests

from flask import Flask, request
from cryptography.fernet import Fernet

api = Flask(__name__)

STORAGE_DIRECTORY = "receiver/received_files"

if not os.path.exists(STORAGE_DIRECTORY):
    os.makedirs(STORAGE_DIRECTORY)


@api.route("/", methods=["POST"])
def receiver():
    """Accepts and stores encrypted data, before decrypting and storing 
    in XML format."""
    with open('receiver/secret', 'wb') as secret:
        secret.write(request.data)
    filename = request.headers.get("FILENAME")

    symkey = read_sym_key()
    cipher = Fernet(symkey)
    encoded = open('receiver/secret', 'rb')
    encoded = encoded.read()
    token = cipher.decrypt(encoded)
    with open('receiver/received_files/' + filename + ".xml", "wb") as xml:
        xml.write(token)
    return "Data received"

@api.route("/sym", methods=["POST"])
def receive_key():
    """Accepts and stores symmetric key for decryption"""
    with open('receiver/sym', "wb") as public_key:
        public_key.write(request.data)
    return "Key received"

def read_sym_key():
    f = open('receiver/sym', 'r')
    key = f.read()
    f.close()
    return key

if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=8001)