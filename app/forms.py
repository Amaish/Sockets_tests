import socket
import sys
from thread import *


class config:
    def __init__(self, host=None, port=None, s=None):
        self.host = host
        self.port = port
        self.s = s


class client(config):
    def create_socket(self):  # Create a socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
        print 'Socket Created'
        return s

    def connect_host(self, host, port, s):  # Connect to remote server
        self.host = host
        self.port = port
        self.s = s
        try:
            remote_ip = socket.gethostbyname(host)
        except socket.gaierror:
            # could not resolve
            print 'Hostname could not be resolved. Exiting'
            sys.exit()
        # Connect to remote server
        s.connect((remote_ip, port))
        print 'Socket Connected to ' + host + ' on ip ' + remote_ip

    def send_message(self, s, message):  # Send some data
        self.s = s
        self.message = message
        try:
            # Set the whole string
            s.sendall(message)
        except socket.error:
            # Send failed
            print 'Send failed'
            sys.exit()
        print 'Message sent successfully'

    def receive_message(self, s):  # Receive a reply
        self.s = s
        # Now receive data
        reply = s.recv(4096)

        print reply


class server(config):
    def create_socket(self):  # Create a socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print 'Failed to create socket'
            sys.exit()
        print 'Socket Created'
        return s

    def bind_socket(self, host, port):
        self.host = host
        self.port = port
        try:
            s.bind((host, port))
        except socket.error, msg:
            print 'Bind failed. Error Code : ' + \
                str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        print 'Socket bind complete'

    def sckt_listen(self):
        s.listen(10)
        print 'Socket now listening'

    #Function for handling connections. This will be used to create threads
    def clientthread(self,conn):
        #Sending message to connected client
        conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
        
        #infinite loop so that function do not terminate and thread do not end.
        while True:
            
            #Receiving from client
            data = conn.recv(1024)
            reply = 'OK...' + data
            if not data: 
                break
        
            conn.sendall(reply)
        
        #came out of loop
        conn.close()


    def sckt_accept(self):
        #now keep talking with the client
        while 1:
            #wait to accept a connection - blocking call
            conn, addr = s.accept()
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            
            #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            start_new_thread(self.clientthread ,(conn,))
        
        s.close()


server = server()
s = server.create_socket()
host = ''
port = 5000
server.bind_socket(host, port)
server.sckt_listen()
server.sckt_accept()
