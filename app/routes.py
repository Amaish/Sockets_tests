import socket, select, string, sys
from forms import  chat_class, client, server


port = int(sys.argv[1])
server_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)


names=[]
print len(names)
name=""
def prompt(host,s) :
    if len(names)<1:
        global name
        name=raw_input("enter your name: ")
        host = socket.gethostbyname(socket.gethostname())
        sender=client()
        sender.create_socket()
        sender.connect_host(host,port,s)
        sender.send_message(s,name)
        names.append(name)
        print names
    else:
        sys.stdout.write("\n"+name+":->")
        sys.stdout.flush()
 
#main function
if __name__ == "__main__":
     
    if(len(sys.argv) < 2) :
        print 'Usage : python routes.py port'
        sys.exit()
     
    host = socket.gethostbyname(socket.gethostname())
    print host
    port = int(sys.argv[1])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    prompt(host,s) 
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start sending messages'
    prompt(host,s)
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    prompt(host,s)
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                s.send(msg)
                prompt(host,s)