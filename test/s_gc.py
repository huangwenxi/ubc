import socket
import json
import logging
import random
PORT = 6080
HOST = '127.0.0.1'
SOCKET = None
def create_socket():
    global SOCKET, HOST,ADDRESS
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ADDRESS = (HOST, PORT)
    return SOCKET;

def main():
    create_socket()

    heartbeat = {'id':'NTC_HEARTBEAT','info':[70,2,1,1,1,1,1,1,1,1]}
    queryimsi = {'id':'NTC_QUERY_IMSI', 'imsi':['460001234455439']}
    insertimsi = {'id':'NTC_INSERT_IMSI', 'imsilist':['460001234455438']}

    while True:
        queryimsi['imsi'] = []
        insertimsi['imsilist'] = []
        for i in range(0, 10):
            queryimsi['imsi'].append('46000' + str(random.randint(1000000000, 9999999999)))
            insertimsi['imsilist'].append('46000' + str(random.randint(1000000000, 9999999999)))

        code = input("""Please select the operation
        usage:1 -> send heartbeat to server.
              2 -> send query imsi
              3 -> send insert imsi
        """)
        if code is 1:
            packet = heartbeat
        elif code is 2:
            packet = queryimsi
        elif code is 3:
            packet = insertimsi

        SOCKET.sendto(json.dumps(packet), ADDRESS)
        print 'send message:' + json.dumps(packet)

        message, address = SOCKET.recvfrom(1024)
        print 'receive message:'+ str(json.loads(message))


main()