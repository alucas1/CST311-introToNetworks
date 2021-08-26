# Team: Cryptids
# Authors: Bryan Aguiar, Gabriel De Leon, Emerald Kunkle, Alberto Lucas
# Date: June 08, 2021
# Name: TCPServer
# Description: This program showcases a simple TCP connection between a server and two
# clients. The server accepts a predefined amount of connections (in this case, 2). The
# server then waits for a single message from each client. After each message is sent, 
# the server determines which client sent the message first. The order of messages is 
# sent to each client and the TCP connections are subsequently closed.

# Lab Question: Explain why you need multithreading to solve this problem. 
# Answer: Multithreading is required for the server to maintain multiple TCP 
# connections with multiple clients. Each thread in the server is able to maintain 
# a TCP connection with a remote client while working in parallel with other threads;
# the server is able to "work" individually with each client in parallel (such as 
# listening to and sending messages between the server and different clients). Without 
# multithreading, the server would only be able to work on one part of the program 
# with one individual client at a time.

import socket
import threading
import time

# THREAD SETUP #
mutexLock = threading.Lock()            
maxConnections = 2     
connectedClientNames = list()                 
threads = list()                        
msgHistory = list()                     # message history stored in 3-tuple list: (msgCount, clientName, message)
readyToDC = [False] * maxConnections    # Keeps track of which threads are ready to disconnect
msgCount = 0                            # Keeps track of message count

# SERVER SETUP #
serverPort = 12000
serverName = "10.0.0.1"
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Thread execution function - Controls the flow of messages between the clients 
# and the server. Executed each time a new thread(new connection) is created. 
# connectionSocket - Socket of connected client
# clientName       - Name of connected client
def thread_function(connectionSocket, clientName):  
    global msgCount
    global msgHistory

    # Connection message sent to client
    serverMsg = "Client " + clientName + " connected."
    connectionSocket.send(serverMsg.encode())

    # Receive message from client
    clientMsg = connectionSocket.recv(1024)
    clientMsg = clientMsg.decode()
        
    # Update message count and message
    mutexLock.acquire()
    msgCount += 1
    msgHistory.append((msgCount, clientName, clientMsg))  
    print("Client " + clientName + " sent message " + str(msgCount) + ": " + clientMsg)
    mutexLock.release()

    # Update readyToDC list - signal that this thread is ready to end connection
    mutexLock.acquire()
    for index, signal in enumerate(readyToDC):
        if signal == False:
            readyToDC[index] = True
            break
    mutexLock.release()

    # Waits until msg from other client is received    
    while any(signal == False for signal in readyToDC):
        time.sleep(1) 
    
    # Sends message to client - Informs client the order of the received messages
    clientMsg = msgHistory[0][1] + ": " +  msgHistory[0][2] + " received before " + msgHistory[1][1] + ": " +  msgHistory[1][2] 
    connectionSocket.send(clientMsg.encode())

    connectionSocket.close()

# Start server - Listen to connections
serverSocket.bind((serverName, serverPort))
serverSocket.listen(1)
print("The server is waiting to receive " + str(maxConnections) + " connections...\n")

# SERVER MAIN LOOP #
# Accepts connections and manages threads
while True:
    # Accept new connection (up to maxConnections) and create a thread for it
    for index in range(maxConnections):
        connectionSocket, addr = serverSocket.accept()
        clientName = chr(88 + index) # Assigns clientName starting at ASCII 'X'
        connectedClientNames.append(clientName)
        print("Accepted connection " + str(index + 1) + ", calling it client " + clientName)
        newThread = threading.Thread(target=thread_function, args=(connectionSocket, clientName,))
        threads.append(newThread)
    print()

    # Start threads
    for index, thread in enumerate(threads):
        thread.start()

    # Server message - announces server is ready to receive messages from clients
    announcement = "Waiting to receive messages from "
    for index, clientName in enumerate(connectedClientNames):
        if maxConnections == 1 or index == maxConnections - 1:
            announcement += "client " + connectedClientNames[index] + "..."
        else:
            announcement += "client " + connectedClientNames[index] + " and "
    print(announcement + "\n")

    # Wait for threads to signal that they are ready to disconnect
    while any(signal == False for signal in readyToDC):
        time.sleep(1)

    # Wait for threads to terminate  
    print("\nWaiting a bit for clients to close their connections")
    for thread in threads:
        thread.join()
    
    # Cleanup for new connections
    threads.clear()
    msgHistory.clear()
    connectedClientNames.clear()
    readyToDC = [False] * maxConnections
    msgCount = 0  
    print("Done\n")
    break # If this is removed, the server will accept 2 new connections and loop over