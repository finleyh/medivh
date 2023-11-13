#!/usr/bin/python
import socket
import math
import os

UDP_IP = "127.0.0.1"
UDP_PORT = 53

shared_secret = os.environ.get('MEDIVH_SHARED_KEY','aweakkey').encode('utf-8')

def encrypt(data, key=shared_secret):
    padding = math.ceil(len(data)/len(shared_secret))
    if padding > 1:
        key = key*padding
    return bytes(a^b for a,b in zip(data,key))


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mydata = input("your message:")
    mybytes = mydata.encode('utf-8')

    client.sendto(encrypt(mybytes), (UDP_IP,UDP_PORT))

    try:
        data, server = client.recvfrom(1024)
        print(f'{data} from {server}')
    except socket.timeout:
        print('NO RESPONSE FROM SERVER')

if __name__=="__main__":
    main()