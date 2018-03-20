"""def add():
    print "this is for addition"
    return 1+2

b=add()
print b"""

from forms import client, server
import socket

Client = client()
host = ''
port=8888
s=Client.create_socket()
Client.connect_host(host,port,s)
message=raw_input("enter a message:\n")
Client.send_message(s,message)