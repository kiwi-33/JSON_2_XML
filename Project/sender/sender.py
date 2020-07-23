import os, requests, json

from flask import Flask, request, abort, send_from_directory
from json2xml import json2xml
from json2xml.utils import readfromjson
from cryptography.fernet import Fernet

UPLOAD_DIRECTORY = "sender/api_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Flask(__name__)

@api.route("/files/<filename>", methods=["POST"])
def load_file(filename):
    """Accepts json payload.  Stores this before converting to XML and encrypting
    using symmetric key.  Sends encrypted data to storage server."""
    path = UPLOAD_DIRECTORY + '/' + filename + '.json'
    if "/" in filename:
        abort(400, "no subdirectories allowed")

    if request.is_json:
        content = request.get_json()

        with open(path, 'w') as outfile:
            json.dump(content, outfile)
        
        data = readfromjson(path)
        with open("sender/message.xml", "w") as f:
            f.write(json2xml.Json2xml(data).to_xml())
        
        f = open('sender/message.xml', 'r')
        message = f.read()
        message = message.encode('utf-8')
        f.close()

        symkey = read_sym_key()
        print(symkey)
        cipher = Fernet(symkey)
        encrypted = cipher.encrypt(message)
        requests.post('http://' + os.environ['ADDRESS'] + ':' + os.environ["PORT"], data=encrypted, headers = {"FILENAME": filename})
        return 'Data posted to storage server', 201
    else:
        return 'Error accepting data, format must be JSON.', 400

def gen_sym_key():
    """Generates symmetric key and sends to storage server."""
    sym = Fernet.generate_key()
    with open('sender/sym', 'wb') as symkey:
        symkey.write(sym)
    requests.post('http://' + os.environ['ADDRESS'] + ':' + os.environ["PORT"] + '/sym', data=sym)

def read_sym_key():
    f = open('sender/sym', 'r')
    key = f.read()
    f.close()
    return key

if __name__ == "__main__":
    gen_sym_key()
    api.run(debug=True, host="0.0.0.0", port=8000)
