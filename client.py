#!/usr/bin/python3.6

import socket 
import select 
import sys
import signal 
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

if len(sys.argv) != 3: 
    print "Missing arguments. Needs IP address and Port Number"
    sys.exit(1)

IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2])

if (Port < 0 or Port > 65535) :
        print "Overflow Error!!!"
        print "PROGRAM TERMINATING!!!"
        sys.exit(1)

try :
    server.connect((IP_address, Port)) 

except socket.error :
    print "Failed to connect to server"
    print "PROGRAM TERMINATING!!!"
    s.close()
    sys.exit(1)

# if detects a signal interrupt (ctrl + C) this method will terminate the program gracefully
def exitGracefully(sigNum, frame) :
    print "\nTermination signal has been detected!"
    sys.exit(0)

signal.signal(signal.SIGINT, exitGracefully)

while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 
  
    """ There are two possible input situations. Either the 
    user wants to give  manual input to send to other people, 
    or the server is sending a message  to be printed on the 
    screen. Select returns from sockets_list, the stream that 
    is reader for input. So for example, if the server wants 
    to send a message, then the if condition will hold true 
    below.If the user wants to send a message, the else 
    condition will evaluate as true"""
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for socks in read_sockets: 
        if socks == server: 
            message = socks.recv(2048) 
            print message

        else: 
            message = sys.stdin.readline()
            print '\n' 
            server.send(message) 
            sys.stdout.write("<You>") 
            sys.stdout.write(message) 
            sys.stdout.flush()
            print '\n'

server.close() 