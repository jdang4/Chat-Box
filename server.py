#!/usr/bin/python3.6

import socket 
import select 
import sys 
from thread import *
import signal
  
"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print "Missing arguments. Needs IP address and Port Number"
    exit() 
  
# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 
  
# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 
  
""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_address, Port)) 
  
""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100) 
  
list_of_clients = [] 

# if detects a signal interrupt (ctrl + C) this method will terminate the program gracefully
def exitGracefully(sigNum, frame) :
    print "\nTermination signal has been detected!"
    for client in list_of_clients :
        #print client
        client.close()
    sys.exit(0)

# creating a thread for each client (allows server to have multiple of clients)    
def clientthread(conn, addr): 
  
    # sends a message to the client whose user object is conn 
    conn.send("Welcome to the Chatroom!\n")
    conn.send("An agent will be right with you\n") 
  
    while True: 
        try: 
            message = conn.recv(2048) 
            if message: 
  
                print "<" + addr[0] + "> " + message 
  
                # Calls broadcast function to send message to all 
                message_to_send = "<" + addr[0] + "> " + message 
                broadcast(message_to_send, conn) 
  
            else: 
                """message may have no content if the connection 
                is broken, in this case we remove the connection"""
                remove(conn) 
  
        except: 
            continue
  
"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients != connection: 
            try: 
                clients.send(message) 
            
            except: 
                clients.close() 
  
                # if the link is broken, we remove the client 
                remove(clients) 
  
"""The following function simply removes the object 
from the list that was created at the beginning of  
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
signal.signal(signal.SIGINT, exitGracefully)

while True: 
  
    conn, addr = server.accept() 

    list_of_clients.append(conn) 
  
    # prints the address of the user that just connected 
    print addr[0] + " connected"
  
    # creates and individual thread for every user that connects 
    start_new_thread(clientthread,(conn,addr))     

# at this point the server will close   
conn.close() 
server.close() 