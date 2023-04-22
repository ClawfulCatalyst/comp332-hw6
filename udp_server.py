# COMP 332, Spring 2023
# Chat client
# Katelyn McCall

# Example usage:
# 
#   python3 udp_sever.py <server host> <server port> <client host> <client port>
#

import socket
import sys
import random


class PingServer:

    def __init__ (self, server_host, server_port, client_host, client_port):
        self.server_addr = (server_host, server_port)
        self.client_addr = (client_host, client_port)
        self.start()
    
    def start(self):

        # Initialize the server socket
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(self.server_addr)
        except OSError as e:
            print ('unable to open server socket')
            if sock:
                sock.close()
            sys.exit(1)
        
        self.recv_ping(sock)

    def ping_msg(self, sock, msg):
        r = random.randint(1,10)

        # 30% of packets are dropped
        if r <= 7:
            sock.sendto(msg.encode('utf-8'),self.client_addr)
    
    def wait_for_msg(self, sock):
        while True:
            try:
                msg, addr = sock.recvfrom(self.server_addr[1])
                return msg
            except Exception as e:
                print('Error receiving: ', e)
                return '%'

    def recv_ping(self, sock):
        while True:
            
            # receive msg

            recv_msg = self.wait_for_msg(sock)
            
            # send msg back

            if not recv_msg == '%':
                recv_msg = recv_msg.decode('utf-8')
                print(recv_msg)
                spl = recv_msg.split('/')
                msg = 'ping/' + '/' + spl[1]
                self.ping_msg(sock, msg)

def main():

    print (sys.argv, len(sys.argv))
    server_host = 'localhost'
    server_port = 50007
    client_host = 'localhost'
    client_port = 50008

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])
        client_host = sys.argv[3]
        client_port = int(sys.argv[4])

    ping_server = PingServer(server_host, server_port, client_host, client_port)

if __name__ == '__main__':
    main()