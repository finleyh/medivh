#!/usr/bin/python
import socket
import math
import os

UDP_IP = ""
UDP_PORT = 53

shared_secret = os.environ.get('MEDIVH_SHARED_KEY','aweakkey').encode('utf-8')

def encrypt(data, key=shared_secret):
    padding = math.ceil(len(data)/len(shared_secret))
    if padding > 1:
        key = key*padding
    return bytes(a^b for a,b in zip(data,key))


def process_request(data):
    print(f'Raw data is {data}')
    decrypted = encrypt(data,shared_secret)
    print(f'Decrypted {decrypted}')
    if b'done' in decrypted:
        return encrypt(b'OK',shared_secret)
    else:
        return b''


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as listener:
        listener.bind((UDP_IP,UDP_PORT))

        while True:
            data, addr = listener.recvfrom(40960)
            if not data:
                break
            else:
                response = process_request(data)
                listener.sendto(response,addr)


if __name__=="__main__":
    main()