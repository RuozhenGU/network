import socket
import sys


class Server:
    def __init__(self, req_code, address='', port=0):
        
        self.req_code = req_code

        self.port = port
        self.address = address

        self.stored_msg = ["NO MSG"]
        
        # set up TCP server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.address, self.port))
        self.server.listen(1)

        # set up UDP server, one time connection
        self.server_UDP = None

        self.n_port = self.return_free_port() # for TCP
        self.r_port = None # for UDP

        self.client_socket = None # assume only one client

    
    def return_free_port(self):
        """
            find random available TCP port, return to client
        """
        n_port = self.server.getsockname()[1]

        print("SERVER_PORT: %d\n" % n_port)

        with open("server.txt", "a") as f:
            f.write("SERVER_PORT: %d\n" % n_port)

        return n_port

    def connect_TCP_UDP(self):
                                  
        while True:

            self.client_socket, addr = self.server.accept()

            pwd = self.client_socket.recv(4096)

            # verify password
            if self.req_code != pwd:
                print("Invalid req_code")
                self.client_socket.sendall(str(0).encode())

                self.client_socket.close()
                sys.exit()
            else:

                # new UDP socket every time
                self.server_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                
                self.server_UDP.bind((self.address, self.port))

                self.r_port = self.server_UDP.getsockname()[1]

                # send r_port back to client for future UDP connect
                self.client_socket.sendall(str(self.r_port).encode())


                # TCP done, UDP start to transmit data
                message, client_address = self.server_UDP.recvfrom(4096)

                # handle Get request
                if message.decode('utf-8') == "GET":
                   
                    # then send each msg 
                    for i in range(1, len(self.stored_msg)):
                        self.server_UDP.sendto(self.stored_msg[i].encode(), client_address)
                    self.server_UDP.sendto(self.stored_msg[0].encode(), client_address)
                else:
                    # store it
                    self.stored_msg.append(message)

                # expect another message

                message, client_address = self.server_UDP.recvfrom(4096)

                if message.decode('utf-8') == 'TERMINATE':
                    self.server_UDP.close()
                    self.server.close()
                    break

                self.stored_msg.append(str(self.r_port) + ": " + message.decode('utf-8'))


if __name__ == "__main__":
    serverOnj = Server(req_code = sys.argv[1])
    
    serverOnj.connect_TCP_UDP()
   




  

