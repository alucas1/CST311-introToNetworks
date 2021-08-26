# Run Program Using Python3 as Python2 will cause the Packet Loss not to work
import time
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)

# To set waiting time of one second for reponse from server
clientSocket.settimeout(1)

# Declare server's socket address
serverName = '10.0.0.1'
serverPort = 12000

# Initialize variable to store amount of successful packets
packetsReceived = 0
pingAmount = 10

#Exponential weighted moving average variables
alpha = 0.125
beta = 0.25
estimatedRTT = 0
averageRTT = 0

# Ping ten times
for i in range(pingAmount):  
    message = 'Ping ' + str(i+1) # creates message to send to server
    # try except to catch when ping goes missing
    try:
        # Start timer for packet
        startTime = time.time()
        
        # Send Packet to server and print a message that it was sent
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        print("Sent: " + message)

        # Receive Successful Packet from server and print that the packet was received
        # And Increment Counter For a Successful Packet Received
        data, server = clientSocket.recvfrom(1024)
        print("Recieved: " + data.decode())
        packetsReceived += 1

        # Stop timer and Calculate the RTT using the EndTime - StartTime. Multiply by 1000 to
        # convert it to ms.
        endTime = time.time()
        rtt = (endTime - startTime) * 1000
        
        # On first packet, store value of minimum RTT, max RTT, average RTT, and begin calculations
        # for estimated and devRTT.
        if i == 0:
            minRTT = rtt
            maxRTT = rtt
            averageRTT = rtt
            estimatedRTT = rtt
            devRTT = rtt / 2
        
        # All other successful packets, add to the averageRTT value and continue computing the estimatedRTT
        # and devRTT using the given formulas.   
        else:
            averageRTT += rtt
            estimatedRTT = (1 - 0.125) * estimatedRTT + (0.125 * rtt)
            devRTT = (1 - 0.25) * devRTT + 0.25 * abs(rtt - estimatedRTT)

        # If statement to see, if current RTT is less than the value stored in minRTT
        if minRTT > rtt:
            minRTT = rtt

        # If statement to see, if current RTT is greater than the value stored in maxRTT
        if maxRTT < rtt:
            maxRTT = rtt
        
        # Print start and end time values using scientific notation, and print the current sample RTT
        print('Start time: ' + str(format(startTime, 'e')))
        print('Return Time: ' + str(format(endTime, 'e')))
        print (data.decode() + " RTT: " + str(rtt) + ' ms\n')
    
    # Upon failing to receive packet, a message will be printed out to the console that Request has Timed Out
    except timeout:
        print('No Message Received')
        print(message + ' Request Timed Out\n')    

# Calculate timeout interval using estimated and devRTT, and calculate the amount of missing packets
timeoutInterval = estimatedRTT + (4 * devRTT)
packetsMissed = pingAmount - packetsReceived

# Print out all totals to the console.
print('Min RTT:\t' + str(minRTT) + ' ms')
print('Max RTT:\t' + str(maxRTT) + ' ms')
# current value of averageRTT is divided by total number of packets to get true average of RTT
print('Avg RTT:\t' + str(averageRTT / packetsReceived) + ' ms') 
print('Packets Dropped:' + str(packetsMissed) + ' Packets Lost')
# calculate the percentage of missed packets
print('Packet Loss:\t' + str((packetsMissed / pingAmount) * 100) + '%')
print('Estimated RTT:\t' + str(estimatedRTT) + ' ms') 
print('Dev RTT:\t' + str(devRTT) + ' ms')
print('Timeout Interval:' + str(timeoutInterval) + ' ms')