#!/usr/bin/python

import socket
import sys

class Client:

    def __init__(self, host, port, request_code):

        # create Ipv4, TCP socket
        self.clientTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # create Ipv4, UDP socket
        self.clientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.port = int(port)
        self.host_addr = host
        self.req_code = request_code.encode()

        # store message received from host
        self.message_pool = []

        # receive new port # from server
        self.n_port = self.connect_TCP()


    def connect_TCP(self):
        """
            attempt to establish TCP connections
            retrieve random available port from server
        """
        try:
            self.clientTCP.connect((self.host_addr, self.port))
            self.clientTCP.sendall(self.req_code)
        except:
            print("Quit, TCP cannot be established")
            sys.exit()
        
        new_port = self.clientTCP.recv(4096).decode('utf-8') # buffer size 4096
        
        if int(new_port) == 0:
            self.clientTCP.close()
            sys.exit()
        
        with open('client.txt', 'a') as f:
            f.write("r_port: %s\n" % new_port)
        
        self.clientTCP.close()

        return int(new_port)


    def send_UDP(self, text):
        """
            attempt to send message via UDP connections
        """
        try:
            self.clientUDP.sendto(text.encode(), (self.host_addr, self.n_port))
        except:
            self.clientUDP.sendto(text.encode(), (self.host_addr, self.n_port))
            print("Quit, unable to send via UDP connection")
            sys.exit()
    
    def receive_UDP(self):

        response, addr = self.clientUDP.recvfrom(4096)

        self.host_addr, _ = addr
        response = response.decode('utf-8')

        self.message_pool.append(response)

        return response

    
    def connect_UDP(self, text=None):

        self.send_UDP("GET")

        
        while True:
            _msg = self.receive_UDP().decode('utf-8')

            if _msg == "NO MSG":
                print(_msg)
            else:
                print(_msg.split(": ")[1])
            
            # write to a log file
            with open('client.txt', 'a') as f:
                f.write(_msg)
                f.write("\n")

            if (_msg == 'NO MSG'): 
                with open('client.txt', 'a') as f:
                    f.write("\n")
                break
        
        self.send_UDP(text)

        _ = raw_input('type something to terminate: \n')

        self.clientUDP.close()


        
if __name__ == "__main__":
    clientObj = Client(
                    host = sys.argv[1], 
                    port = sys.argv[2], 
                    request_code = sys.argv[3]
                    )
    
    clientObj.connect_UDP(sys.argv[4])
   
    
        




        

