# COMP 332, Spring 2023
# Chat client
# Katelyn McCall

# Example usage:
# 
#   python3 udp_client.py <client host> <client port> <server host> <server port>
#

import socket
import sys
import datetime


class PingClient:

    def __init__(self, client_host, client_port, server_host, server_port):
        self.client_addr = (client_host, client_port)
        self.server_addr = (server_host, server_port)
        self.start()

    def start(self):

        # Initialize the client socket

        try: 
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(self.client_addr)
            sock.settimeout(1.0)
        except OSError as e:
            print ('Unable to connect to socket: ', e)
            if sock:
                sock.close()
            sys.exit(1)

        self.ping_n_times(sock, 10)
    
    # waits for a response and returns in
    def wait_for_response(self, sock):
        
        while True:
            try:
                msg, addr = sock.recvfrom(self.server_addr[1])
                return msg
            except Exception as e:
                return '%'
           

    def ping_msg(self, sock, msg, wait_for_response = False):
        sock.sendto(msg.encode('utf-8'), self.server_addr)
        if wait_for_response:
            return self.wait_for_response(sock)
        else:
            return
            

    def ping_n_times(self, sock, n):
        seq = 0
        while seq < n:

            t0 = datetime.datetime.now()

            # send msg
            msg = 'ping/' + str(seq) + '/' + str(t0)
            print('sending: ' + msg)

            # receive msg
            recv_msg = self.ping_msg(sock, msg, True)

            if not recv_msg == '%':

                RTT = datetime.datetime.now() - t0
                print('received: ' + recv_msg.decode('utf-8') + '\n' + 'RTT: ' + str(RTT) + '\n')
            
            else:
                print('TIMEOUT\n')


            seq = seq+1

def main():

    print (sys.argv, len(sys.argv))
    client_host = 'localhost'
    client_port = 50008

    server_host = 'localhost'
    server_port = 50007

    if len(sys.argv) > 1:
        chat_host = sys.argv[1]
        chat_port = int(sys.argv[2])
        server_host = sys.argv[3]
        server_port = int(sys.argv[4])

    ping_client = PingClient(client_host, client_port, server_host, server_port)

if __name__ == '__main__':
    main()