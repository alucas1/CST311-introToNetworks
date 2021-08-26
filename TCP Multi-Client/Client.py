# Team: Cryptids
# Authors: Bryan Aguiar, Gabriel De Leon, Emerald Kunkle, Alberto Lucas
# Date: June 08, 2021
# Name: TCPClient
# Description: This program showcases a simple TCP connection between a server and two
# clients. The server accepts a predefined amount of connections (in this case, 2). The
# server then waits for a single message from each client. After each message is sent, 
# the server determines which client sent the message first. The order of messages is 
# sent to each client and the TCP connections are subsequently closed.

import socket
import time

# Setup client and connect to server
serverName = "10.0.0.1"
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Receive initial connection message from server
serverMsg = clientSocket.recv(1024)
print("From Server: " + serverMsg.decode())

# Send message to server
clientMsg = input("Enter message to send to server: ")
clientSocket.send(clientMsg.encode())

# Receive second message from server (message order)
serverMsg = clientSocket.recv(1024)
print("From Server: " + serverMsg.decode())

# End connection
clientSocket.close()
