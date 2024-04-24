# CS305-2024Spring-FinalProject: Reliable Data Transfer using UDP

This project focuses on the development of a reliable data transfer (RDT) protocol using UDP as the unreliable protocol. Specifically, this project requires you to use UDP as the transport layer protocol and implement an RDT protocol at the application layer. The primary objective is to design and implement a protocol that can address the challenges and limitations of RDT in an unreliable network environment. By leveraging UDP and exploring various mechanisms for reliable transmission, the project aims to create a robust and efficient communication protocol. The protocol will be designed to mitigate issues such as packet loss, latency, data corruption, and congestion, which commonly impact network communication.

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
You should construct your RDT header as the template RDTHeader class, and it should contain the following data fields:

|test_case|Source_address|Target_address|SYN|FIN|ACK|SEQ|SEQACK|LEN|RWND|CHECKSUM|OPTIONAL|PAYLOAD|
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|1 bytes|6 bytes|6 bytes|1 byte|1 byte|1 byte|4 bytes|4 bytes|4 bytes|4 bytes|2 bytes|8 bytes|LEN bytes|
|Indicate the test case will be used, ranged in 0~10|IP address and port of sender|IP address and port of receiver|SYN in TCP|FIN in TCP|ACK in TCP|SEQ in TCP|ACK number in TCP|Length of PYALOAD|Size of Receiving window|Chcksum in other protocol|Reserved space for adding any additional fields you deem necessary|Data|

We provided the template code of RDTSocket in *`RDT.py`* and template code of RDT packet Header in *`Header.py`*. Based on our `Header.py` file, you could also add some other attributes up to **8 bytes** as optional. 

Each field functions similarly to those in the TCP protocol, and you can find detailed information about them through the following [link](https://datatracker.ietf.org/doc/html/rfc9293).

*Please note that during data transmission, all above data should be encoded to corresponding lenght bytes and added together following the order in the table above. You are not supposed to use the first **3** fields (test_case, Source_address, Target_address) to calculate the `CHECKSUM`, `Source_address` and `Target_address` should be formatted by stream.*



### 1.2 Reliable Data Transfer
For a reliable connection, the following steps are to be executed consecutively:

#### 1 Accept and establish a connection
You are supposed to implement the function `bind(), accept(), and connect()`. The function `bind()` could bind the current RDT socket to a specific address. Function *accept()* and *connect()* are used to establish connection between client and server. You are supposed to implement the 3-way-handshake in these two function. 

**Function *`accept()`* needs to support multithreading and be able to establish multiple socket connections. Messages from different sockets should be isolated from each other, requiring you to multiplex the data received at the underlying UDP.**

For example:
```python
# As a Server
target_addr = ("123.4.5.6", 12345)
socket = RDTSocket(...)
socket.bind(target_addr)
server_socket = socket.accept()
```
```python
# As a Client
target_addr = ("123.4.5.7", 12345)
socket = RDTSocket(...)
socket.bind(target_addr)
socket.connet()
```

#### 2 Packet verification
To ensure reliable data transmission, you are supposed to implement data validation functionality. Specifically, you need to calculate a 16-bit checksum for all fields in the packet except for **`test_case, Source_address, and Target_address`**, and then fill in the `CHECKSUM` field. This ensures that the receiver can perform validation checks upon receiving the data. *You could implement related feature in both **`send() & recv()`** or define a new function and call it if need.*

#### 3 Retransmitting
Generally, in an unreliable network environment, the connection might occur packets lost, corrupted or delyaed. Hence it is necessary to retransmit these error packets when above error happened. Specifically, when some packets that have been sent do not receive a response with `ACK=1`, which means that they have not been received successfully, it is necessary to resend those packets. You can implement this feature using any strategy you think suitable. For example, maintain a list of sent data, remove an item from the list when it receives the correct response, and resend the data if no response is received within a set duration.



#### 4 Retransmission request
Sometimes, during the reception of a large amount of data, the receiver may experience timeouts for certain packets that are not delivered, and if the sender does not resend these packets, the receiver needs to send a request to the sender to specify retransmission. This feature should be implemented in both **`recv() & send()`**.

#### 5 Data segmentation 
Sometimes, we need to transmit large amounts of data that cannot be sent all at once. In such cases, you are supposed to implement a basic data chunking and sorting method that can divide a large dataset into multiple small CHUNKs that can be transmitted directly. Additionally, it should ensure that the receiver can reassemble these data chunks into the original large dataset upon receipt. This feature shoule be implemented in **`send()`** For example,
```python
target_addr = ("123.4.5.6", 12345)
socket = TCPSocket(...)
socket.bind(target_addr)
with open('test.txt', 'r') as f:
    data = f.read()
    socket.send(data=data)
socket.close()
```

In the testing section, we have **a strict limit on the size of each chunk**, and you need to stick to that limit.

#### 6 Pipeline manner
Sequential transmission need to wait for confirmation of the previous packet, which is inefficient. In such cases, data transmission needs to be done in a PIPELINE manner. You can transmit multiple packets simultaneously without waiting for confirmation of previous packet. The number of unacknowledged packets is limited by the **RWND**.



#### 7 Congestion control & Flow control

In this part, you can refer to the congestion and flow control mechanisms within the TCP protocol.
#### 8 Close connection
You are supposed to implement the 4-way handshake to close a reliable connection in **`close()`** function.

# 2 Testing & Grading
## Environment
Each function must be independently implemented by you, using only the standard libraries provided with Python; no external libraries are permitted. We will test your implementation in an environment running **Python 3.9.0**. Note that the use of the **socket library** is restricted solely to functions related to the **UDP** protocol.
 

## 2.1 Test system
When testing your RDTSocket, you should make our porxy server as your target server. And make sure that your **real target server address & port** has been stored in *Target_address* and the ip adress and port of your host have been stored in *Source_address*.

<p align="center">
  <img src="./img/proxy.png" width="70%"/>
</p>

A complete test system example is structured as shown in the figure above, where the proxy server will be deployed on our server. You are required to use your RDTSocket implementation for Sender and Receiver during testing. All interactive data must pass through our proxy server for forwarding. Our proxy server will simulate the unreliable network environment (lost, occupt, delay, etc.) based on the **test_case** field set in the headers of the data you transmit.

To facilitate smoother testing, please adhere to the following guidelines by using the IP address and port of our official proxy server when conducting tests.

## 2.2 Guidelines
When the network environment is like the example figure above. Due to the header size totaling **42 bytes**, we have set the maximum data size that can be received at one time in the proxy server to **298 bytes.** Any excess beyond this size will be discarded. Therefore, please ensure that the size of each packet you send does not exceed 256 bytes, which means, the length of *PAYLOAD* should not be larger than **256** bytes.
1. Please ensure that your Sender correctly saves the real destination address `("123.4.5.3", 12345)` and local address `("123.4.5.2", 12345)` in the header when sending data. The socket should be configured to send data to the address `("123.4.5.1", 12345)` during data transmission.
2. Our proxy server will parse the first **13 bytes** of your data upon receipt to extract the *test_case, Source_address, and Target_address*. It will then simulate an unreliable network based on the *test_case* you set before forwarding your data to your receiver.
3. Please ensure that your Receiver correctly saves the real Sender address `("123.4.5.2", 12345)` and local address `("123.4.5.3", 12345)` in the header when sending data. The socket should be configured to send data to the address `("123.4.5.2", 12345)` during data transmission and keep listening to the local address `("123.4.5.3", 12345)`.

<!-- ```python
target_addr = ("123.4.5.6", 12345)
socket = RDTSocket()
socket.connect(target_addr)
``` -->


## 2.3 Testing
You should implement an RDTSocket based on the requirements. 
We will use a proxy SERVER to test your protocol. When using your RDTSocket to build server and client to communicate with each other, all data sent will pass through our proxy server. Therefore, construct your data packages carefully based on our RDTHeader template. Please note that our proxy SERVER assumes that the data will be delayed/lost/corrupted based on different test case.

The total score is 100 points, plus a bonus of 20 points.

**How to test your RDTSocket?**

You can test it through our deployed proxy server. Therefore, you need to include a test_case field in your packet header with values ranging from 0 to 10 (tentative) (no need to calculate it into the `CHECKSUM`). When test_case is 0, it represents a reliable network environment without any packet loss or corruption operations. When test_case ranges from 1 to 10, it will test various functions of RDTSocket. When sending test data for testing, the packet header should include sender's IP and port, receiver's IP and port, as well as test_case, to complete data forwarding and network simulation operations.
The IP address and test port of the testing server will be released later.

## 2.4 Grading
1. Establish (3-way handshakes) & close (4-way handshakes) connection. (5 pts)
2. Demultiplexing directs the data received from UDP to different sockets. (5 pts)
3. Calculation and verification of the CHECKSUM correctly. (5 pts)
4. Complete data segmentation. (5 pts)
5. Your RDTSocket could be used as a client to send multiple short messages to the server built by your RDTSocket. (10 pts)
6. Your RDTSocket could be used as a server to receive a large file from the a server built by your RDTSocket. The file should be separated into multiple CHUNKs and will be sent in a disordered sequence, with some packets being lost. Your RDTSocket should receive and buffer all this data and recover it to the original file based on the sequence number of each packet. If the RDTSocket detects lost packets, it should send a request to the CLIENT and require a re-send. (10 pts)
7. Your RDTSocket could be used as a client to send a large file to the server built by our RDTSocket. This file should be separated into multiple CHUNKs and sent in a PIPELINE way. During testing, we will delay the reception of data to simulate congestion situations. **Please ensure your RDTSocket could maintain the sizes of the congestion control window and flow control window** to control the sending and receiving speed of data, and stop sending data when the server is congested. Resume sending data only when notified by the server that it can receive data again. Sending more than 30% of data beyond the buffer will be considered a failure to complete the flow control function. (20 pts)

6. We will prepare different test cases for testing the performance of your RDTSocket. (total 25 pts)

7. You need to submit a report in which you explain how each function is implemented. The performance analysis of RDT is included. （15 pts）

**Bonus**: To be decided. Any mechanism that improves the RDT transfer rate is permitted. If you have any ideas, please confirm with the instructors or SAs before you start. (20 bonus pts)

<!-- ## 2.2 Presentation (30 pts)
For the final presentation:
1. Add a debug mode to the RDTSocket to print out information about the transmission process.
2. Introduce how you implemented congestion control, flow control, and the pipeline.
3. Explain how you tested and evaluated the performance of your implementation.

You will need to create a video of about 5-8 minutes containing the contents described above. -->

# 3 Notes

- Do not use any existing function that performs the work of RDT for you.
- Data sent during testing will be similar to a long test.
- Provided code:

    1. *Header.py*: provides the data structure of the RDT packet header.
    2. *RDT.py*: provides the template and necessary interface of your RDT Socket.

- Suggested steps:

    1. Assume a reliable link and infinite buffer, complete basic connection management.
    2. Assume the link becomes unreliable, try to fix the issues of loss, corruption, and delay.
    3. Add congestion control and flow control mechanisms.
    4. Attempt to fulfill the bonus requirement by creating a pipeline sending mode for your RDTSocket.

# Contact
If you have any questions about this project, please start a new issue.