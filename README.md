# CS305-2024Spring-FinalProject: Reliable Data Transfer using UDP

This project focuses on the development of a reliable data transfer (RDT) protocol using UDP as the underlying protocol. The primary objective is to design and implement a protocol that can address the challenges and limitations of TCP in an unstable network environment. By leveraging UDP and exploring various mechanisms for reliable transmission, the project aims to create a robust and efficient communication protocol. The protocol will be designed to mitigate issues such as packet loss, latency, data corruption, and congestion, which commonly impact network communication. Through this project, we seek to enhance the existing methods of data transfer and contribute to the field of reliable communication protocols.

A comprehensive report documenting the implementation process, insights, and improvements made is expected. Additional research beyond the provided instructions is encouraged to contribute to the project's success.

## 1 Requirements

### 1.1 Message Format
<!-- To achieve reliable transmission based on UDP, it is necessary to design appropriate protocol fields within the application layer, which sits above the UDP protocol layer. These protocol fields should be incorporated within the UDP packets to facilitate the implementation of reliable transmission mechanisms.

```
+-------------------------+
|   UDP Datagram           |
+-------------------------+
|   UDP Header             |
+-------------------------+
|   Custom Header          |
+-------------------------+
|   UDP Payload            |
+-------------------------+
``` -->

The organization of the packet header can play a crucial role in facilitating reliable transmission. Based on the diagram provided, the packet header can be structured as follows.    
You should construct your RDT header as the template RDTHeader class, and it should contain at least the following data fields:

|SYN|FIN|ACK|SEQ|SEQACK|LEN|AWND|CHECKSUM|PAYLOAD|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|1 byte|1 byte|1 byte|4 bytes|4 bytes|4 bytes|4 bytes|2 bytes|LEN bytes|

### 1.2 Reliable Data Transfer
For a stable connection, the following steps are to be executed consecutively:

1. Accept and establish a connection
2. Maintain the connection, keep listening, and replying
3. Implement congestion control and flow control based on CWND and AWND fields.
4. Manage the TCP pipeline
5. Close the connection and release the resources.

The factors that cause the channel to be unreliable are:

- Delay
- Loss
- Corruption

# 2 Testing & Grading
You should implement an RDTSocket based on the requirements. We will use our RDT SERVER to test your protocol. Therefore, construct your data packages carefully based on our RDTHeader template. Please note that our RDT SERVER assumes that 10% of all incoming packets will be lost. For packets that are not lost, there is a 10% chance of corruption or a 10% chance of a delay of 1 to 5 seconds.

The total score is 100 points, plus a bonus of 20 points.

**How to test your RDTSocket?**

You can test it through our deployed relay server. Therefore, you need to include a test_case field in your data header with values ranging from 0 to 10 (tentative) (no need to calculate it into the CHECKSUM). When test_case is 0, it represents a normal network environment without any packet loss or corruption operations. When test_case ranges from 1 to 10, it will test various functions of RDTSocket. When sending test data for testing, the data header should include sender's IP and port, receiver's IP and port, as well as test_case, to complete data forwarding and network simulation operations.
The IP address and test port of the testing server will be released later.

## 2.1 Grading
1. Establish (3-way handshakes) & close (4-way handshakes) connection with the RDT SERVER. (5 pts)
2. Use your RDTSocket as a client to send multiple short messages to the RDT SERVER. (10 pts)
3. Use your RDTSocket as a server to receive short messages from the RDT SERVER. (10 pts)
4. Use your RDTSocket as a server to receive a large file from the RDT SERVER. The file will be separated into multiple CHUNKs and will be sent in a disordered sequence, with some packets being lost. Your RDTSocket should receive and buffer all this data and recover it to the original file based on the sequence number of each packet. If the RDTSocket detects lost packets, it should send a request to the SERVER and require a re-send. (10 pts)
5. Use your RDTSocket as a client to send a large file to the RDT SERVER. This file should be separated into multiple CHUNKs and sent in a PIPELINE way. During testing, we will delay the reception of data to simulate congestion situations. Please ensure to maintain the sizes of the congestion control window and flow control window to stop sending data when the server is congested. Resume sending data only when notified by the server that it can receive data again. Sending more than 30% of data beyond the buffer will be considered a failure to complete the flow control function. (15 pts)

6. We will prepare 10 different test case for testing the performance of your RDTSocket. (5 pts per case, total 50 pts)

**Bonus**: Implement congestion and flow control system in more than 1 manner will awarded up to 20 pts as bonus.

## 2.2 Presentation (30 pts)
For the final presentation:
1. Add a debug mode to the RDTSocket to print out information about the transmission process.
2. Introduce how you implemented congestion control, flow control, and the pipeline.
3. Explain how you tested and evaluated the performance of your implementation.

You will need to create a video of about 5-8 minutes containing the contents described above.

# 3 Notes

- Do not use any existing function that performs the work of RDT for you.
- Data sent during testing will be similar to a long test.
- Provided code:

    1. *Header.py*: provides the data structure of the RDT protocol header.
    2. *RDT.py*: provides the template and necessary interface of your RDT Socket.

- Suggested steps:

    1. Assume a reliable link and infinite buffer, complete basic connection management.
    2. Assume the link becomes unreliable, try to fix the issues of loss, corruption, and delay.
    3. Add congestion control and flow control mechanisms.
    4. Attempt to fulfill the bonus requirement by creating a pipeline sending mode for your RDTSocket.