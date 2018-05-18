import socket
import json
import logging
PORT = 6081
HOST = '127.0.0.1'
SOCKET = None
def create_socket():
    global SOCKET, HOST,ADDRESS
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ADDRESS = (HOST, PORT)
    return SOCKET;

def main():
    create_socket()
    heartbeat = {'id':'MSG_UBC_HEARTBEAT', 'module':'ubc'}
    SOCKET.sendto(json.dumps(heartbeat), ADDRESS)
    print 'message:' + json.dumps(heartbeat)
    message, address = SOCKET.recvfrom(1024)
    print 'message:'+ str(json.loads(message))

    get_imsi = {'id':'MSG_UBC_GET_IMSI', 'imsi':'460001234455439'}
    SOCKET.sendto(json.dumps(get_imsi), ADDRESS)
    print 'message:' + json.dumps(get_imsi)
    message, address = SOCKET.recvfrom(1024)
    print 'message:' + str(json.loads(message))

main()