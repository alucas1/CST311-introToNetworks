# Team: Cryptids
# Authors: Bryan Aguiar, Gabriel De Leon, Emerald Kunkle, Alberto Lucas
# Date: June 08, 2021
# Name: TCPClient
# Description: This program is the client portion of the tcp chat server.
# The program builds on the main project which requires one server and two
# clients to communicate. The client creates two threads: one to listen to for responses
# and the second thread to write messages out to the server for the other client. The
# client ends when one of the user types 'Bye'.

import socket
import threading
import time

# Client setup and connect to server
serverName = 'localhost'
serverPort = 12000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serverName,serverPort))

# List to store threads 
threads = []
# Flag to check if current connection is active.
active_connection = True
# Current Command to End Chat Server and UserName Request Command
RequestUserName = 'USER'
ShutDown = 'Bye'

# Request a Username from the client.
userName = input("Enter your user name: ")

# readMessage Function - Controls all read aspects of the socket connection. The function
# is only executed once upon successful connection
def readMessage():
    global active_connection

    # Loops through reading, decoding and printing messages until 'Bye' message is received.
    # Once active_connection flag is flipped, the loop will end and the thread will join.
    while active_connection:
        # Receive message from server and decode into variable message
        message = client.recv(1024).decode()

        # On first connection, the server will send a 'USER' message. The client is then
        # required to send the stored user name back to the server.
        if message == RequestUserName:
            client.send(userName.encode())

        # Elif statement to check if last three characters in string contain 'Bye'. If found to be
        # true the client then flips the flag, prints the message, sends the 'Bye' message back to the
        # server and requests the client for an enter input to terminate the write_thread.
        elif message[-3:] == ShutDown:
            active_connection = False
            print(message)
            client.send(ShutDown.encode())
            print("Hit enter to close program")
            break

        # If none of the previous condtions are true, the message is then printed on the client side.
        else:
            print(message)

# sendMessage Function - Sends messages to the server. Similar to readMessage function. The function loops
# until active_connection flag is triggered.
def sendMessage():
    global active_connection

    # Loops through sending messages to server upon input, otherwise waits for input from client.
    while active_connection:
        message = '{}: {}'.format(userName, input(''))
        client.send(message.encode())

# Create threads for both receive and write using the appropriate function as the target and append them
# to our threads list.        
receive_thread = threading.Thread(target=readMessage)
threads.append(receive_thread)
write_thread = threading.Thread(target=sendMessage)
threads.append(write_thread)

# Using the threads list. Iterate to start each thread. 
for thread in threads:
    thread.start()

# Using the threads list. Wait for each thread to fall out of their function and rejoin the main thread.
for thread in threads:
    thread.join()

# Client is closed upon successful joining of threads.
client.close()
