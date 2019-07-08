from Crypto.Cipher import AES
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
    insert(cipher_path, path.split(".")[1], key, iv)


def decrypt_aes(key,iv,cipher_path, filetype):
    try:
        key = b64decode(key)
        enc_data = open_binary(cipher_path)
        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        data = cipher.decrypt(enc_data)
        path = cipher_path.split(".")[0]+"."+filetype
        write_binary("C:/Users/Ana/Desktop/image.jpg",data)
    except Exception:
        print("Incorrect decryption")


if __name__ == '__main__':
    # encrypt_aes(b"\xech4l\x1f6\x81f}{\x01'\xf1\xea\xf7\x9f", "C:/Users/Ana/Desktop/image.jpg")

    decrypt_aes("7Gg0bB82gWZ9ewEn8er3nw==", b'[<\x88w\x0b\x1a\x9ew\x83^\xea\xa4\xd5\x8f\xaf=',"C:/Users/Ana/Desktop/image.enc","jpg")
    # key = b64decode("beV7e/05MCQcohtT312qGA==")
    # print(key)

    # pic = open_binary("C:/Users/Ana/Desktop/image.jpg")
    # write_binary("C:/Users/Ana/Desktop/image1.jpg",pic)