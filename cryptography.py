from Crypto.Cipher import AES, Salsa20, DES3
from Crypto.Random import get_random_bytes
from database import insert
from base64 import b64decode
import time

def open_binary(path):
    with open(path, 'rb') as f:
        data = f.read()
    return data


def write_binary(path, data):
    with open(path,'wb') as f:
        f.write(data)


def encrypt_aes(key, path):
    data = open_binary(path)
    cipher = AES.new(key, AES.MODE_CFB)
    cipher_bytes = cipher.encrypt(data)
    iv = cipher.iv
    cipher_path = path.split(".")[0]+".enc"
    write_binary(cipher_path, data=cipher_bytes)
    insert(cipher_path,"AES", path.split(".")[1], key, iv)


def decrypt_aes(key,iv,cipher_path, filetype):
    try:
        key = b64decode(key)
        iv = b64decode(iv)
        enc_data = open_binary(cipher_path)
        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        data = cipher.decrypt(enc_data)
        path = cipher_path.split(".")[0]+"."+filetype
        write_binary(path,data)
    except Exception as e:
        print("Incorrect decryption")


#32byte key
def encrypt_salsa20(key, path):
    data = open_binary(path)
    cipher = Salsa20.new(key)
    nonce = cipher.nonce
    cipher_bytes = cipher.encrypt(data)
    cipher_path = path.split(".")[0] + ".enc"
    write_binary(cipher_path, data=cipher_bytes)
    insert(cipher_path,"Salsa20", path.split(".")[1], key, nonce)


def decrypt_salsa20(key,nonce,cipher_path, filetype):
    try:
        key = b64decode(key)
        nonce = b64decode(nonce)
        enc_data = open_binary(cipher_path)
        cipher = Salsa20.new(key, nonce)
        data = cipher.decrypt(enc_data)
        path = cipher_path.split(".")[0]+"."+filetype
        write_binary(path,data)
    except Exception:
        print("Incorrect decryption")


def encrypt_3des(path):
    data = open_binary(path)
    while True:
        try:
            key = DES3.adjust_key_parity(get_random_bytes(24))
            break
        except ValueError:
            pass
    cipher = DES3.new(key,DES3.MODE_CFB)
    cipher_bytes = cipher.encrypt(data)
    iv = cipher.iv
    cipher_path = path.split(".")[0] + ".enc"
    write_binary(cipher_path, data=cipher_bytes)
    insert(cipher_path, "3DES", path.split(".")[1], key, iv)


def decrypt_3des(key,iv,cipher_path, filetype):
    try:
        key = b64decode(key)
        iv = b64decode(iv)
        enc_data = open_binary(cipher_path)
        cipher = DES3.new(key, DES3.MODE_CFB, iv=iv)
        data = cipher.decrypt(enc_data)
        path = cipher_path.split(".")[0] + "." + filetype
        write_binary(path, data)
    except Exception:
        print("Incorrect decryption")


if __name__ == '__main__':

    start_time = time.time()
    encrypt_aes(b"\xech4l\x1f6\x81f}{\x01'\xf1\xea\xf7\x9f", "C:/Users/Ana/Desktop/Git.pdf")
    elapsed_time = time.time() - start_time
    print(elapsed_time)

    start_time = time.time()
    decrypt_aes("7Gg0bB82gWZ9ewEn8er3nw==", "QNCVyBQg+f16YfTtzQny1Q==", "C:/Users/Ana/Desktop/Git.enc","pdf")
    elapsed_time = time.time() - start_time
    print(elapsed_time)

    start_time = time.time()
    encrypt_3des("C:/Users/Ana/Desktop/Git.pdf")
    elapsed_time = time.time() - start_time
    print(elapsed_time)

    start_time = time.time()
    decrypt_3des("XjIfRhNMO1QIwgKrulJdCzvZbmJRC0A7", "VZ03NWOEKH0=", "C:/Users/Ana/Desktop/Git.enc","pdf")
    elapsed_time = time.time() - start_time
    print(elapsed_time)

    start_time = time.time()
    encrypt_salsa20(get_random_bytes(32), "C:/Users/Ana/Desktop/Git.pdf")
    elapsed_time = time.time() - start_time
    print(elapsed_time)

    start_time = time.time()
    decrypt_salsa20("ia+yb8f3d2KHA4+59vja8Wkq0kcOLqdK2SHxINRDZrs=", "gXKFVUOSGEg=",
                    "C:/Users/Ana/Desktop/Git.enc", "pdf")
    elapsed_time = time.time() - start_time
    print(elapsed_time)
