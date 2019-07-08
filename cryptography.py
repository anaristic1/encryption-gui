from Crypto.Cipher import AES, Salsa20
from Crypto.Random import get_random_bytes
from database import insert
from base64 import b64decode


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
        enc_data = open_binary(cipher_path)
        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        data = cipher.decrypt(enc_data)
        path = cipher_path.split(".")[0]+"."+filetype
        write_binary(path,data)
    except Exception:
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
        enc_data = open_binary(cipher_path)
        cipher = Salsa20.new(key, nonce)
        data = cipher.decrypt(enc_data)
        path = cipher_path.split(".")[0]+"."+filetype
        write_binary(path,data)
    except Exception:
        print("Incorrect decryption")


# if __name__ == '__main__':
    # encrypt_aes(b"\xech4l\x1f6\x81f}{\x01'\xf1\xea\xf7\x9f", "C:/Users/Ana/Desktop/Git.pdf")
    # decrypt_aes("7Gg0bB82gWZ9ewEn8er3nw==",b'U\xed|\xf9D\x01\xea\x1f\xa08\rP\x00f5g',"C:/Users/Ana/Desktop/Git.enc","pdf")
    # key = b64decode("beV7e/05MCQcohtT312qGA==")
    # print(key)

    # pic = open_binary("C:/Users/Ana/Desktop/image.jpg")
    # write_binary("C:/Users/Ana/Desktop/image1.jpg",pic)


    # encrypt_salsa20(get_random_bytes(32), "C:/Users/Ana/Desktop/info.txt")
    # decrypt_salsa20("AUKWKWiAHhEbeFqtzGApfHSg1zT3lRLMqM//0OrKOKA=", b'\xda\xf8\xd62hX\xbb-',"C:/Users/Ana/Desktop/info.enc","txt")