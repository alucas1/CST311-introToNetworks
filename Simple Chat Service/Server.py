# Team: Cryptids
# Authors: Bryan Aguiar, Gabriel De Leon, Emerald Kunkle, Alberto Lucas
# Date: June 08, 2021
# Name: TCPServer
# Description: This program is the server portion of the tcp chat server.
# The program builds on the main project which requires one server and two
# clients to communicate. The server creates two threads: one for each client 
# connection. During this process the usernames and connections are stored into lists
# by the server. The server terminates upon successful reception of the 'Bye' shutdown command

import socket
import threading

# Data for Server
serverName = 'localhost'
serverPort = 12000

# Server start-up
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((serverName, serverPort))
server.listen()

# Lists to store users and their chosen names
clients = []
userNames = []

# Threads list to store threads created by server, and flag to trigger when server has received
# 'Bye' message to shut down.
threads = []
server_flag = True

# Data to set up max amount of clients so server is not continuously waiting for more than 2 clients
# to connect. Also current shutdown command for server and command for UserName Request.
RequestUserName = 'USER'
MaxConnections = 2
ShutDown = 'Bye'

# sendMessage Function - Broadcast Messages to Other Clients using the clients list
# message - Contains an undecoded message from one of the clients to send out to both clients.
def sendMessage(message):
    for client in clients:
        client.send(message)

# readMessage Function - Receives message from client and loops while the server flag is true
# Upon receiving a 'bye' message the server will begin it's shutdown sequence.  
# client - contains the client connection
def readMessage(client):
    global server_flag

    # Loops through while server_flag is true. Receiving messages and sending them to sendMessage for clients
    # to receive. Only breaks when a 'bye' message is sent
    while server_flag:
            message = client.recv(1024)

            # Decodes message and compares the last 3 characters to see if 'Bye' command was sent. Flips the server
            # flag and the function is exited 
            if message[-3:].decode() == ShutDown:
                sendMessage(message)
                server_flag = False

            # If message is not the shutdown command, then server calls the sendMessage function to send message to clients
            else:
                sendMessage(message)

# receiveConnections Function - Accepts connection from up to MaxConnections of Client. The server also requests  for the clients
# user names by sending a 'USER' message. The client is informed of successful connection and a thread is created for the client
# connection and added to the threads list.
def receiveConnections():
    # Index through loop up to a Maximum of MaxConnections, in this case 2 clients.
    for index in range(MaxConnections):
        # Accepts and stores client and prints out connection to terminal
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request user name from client and append both client data and userName to respective lists
        client.send(RequestUserName.encode())
        userName = client.recv(1024).decode()
        userNames.append(userName)
        clients.append(client)

        # Let client know of successful connection and username.
        print("Username is {}".format(userName))
        sendMessage("{} joined!".format(userName).encode())
        client.send('Connected to server!'.encode())
        
        # Create thread using the readMessage as the target function and append thread to thread list
        thread = threading.Thread(target=readMessage, args=(client, ))
        threads.append(thread)
    
    # Iterate to thread of threads to start each individual thread.
    for thread in threads:
        thread.start()

    # Wait for each thread to terminate and join with main thread
    for thread in threads:
        thread.join()

    # Closes All clients once all threads are joined
    for client in clients:
        client.close()

    # Close server
    server.close()
    
# Main thread starts here by calling the receiveConnection function and falls out and terminates once finished
receiveConnections()




