import socket
import os
import time
from multiprocessing import Process
from RDT import RDTSocket as RDTSocket
from  Header import RDTHeader

Speed_RDT = 0
Speed_UDP = 0

source_address = ('127.0.0.1', 12334)
target_address = ('127.0.0.1', 12335)


def UDP_send(ip, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (ip, port)
    try:
        for i in range(0, 100):
            sock.sendto(str(float(time.time() * 1000)).encode(), server_address)
        # sock.sendto(str(float(time.time() * 1000)).encode(), server_address)
        sock.sendto('end'.encode(), server_address)
    except IOError as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()

def UDP_receive(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    spend_time = 0
    time_list = []
    try:
        while True:
            data, addr = sock.recvfrom(200)
            # spend_time = float(time.time() * 1000) - float(data.decode())
            # print(spend_time)
            if data == b'end':
                break
            else:
                spend_time = float(time.time() * 1000) - float(data.decode())
                time_list.append(spend_time)
        time_list.sort()
        print(f"{time_list[49]}")
    except IOError as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()

    print(f"UDP lantency : {spend_time} ms")

def UDP_start_test(port=12349):
    sender = Process(target=UDP_send, args=("localhost", port))
    receiver = Process(target=UDP_receive, args=("localhost", port))

    receiver.start()
    time.sleep(5)

    sender.start()

    sender.join()
    receiver.join()  
    


def RDT_start_test(): 
    sender = Process(target=RDT_send, args=(source_address, target_address))
    receiver = Process(target=RDT_receive, args=(target_address,))

    receiver.start()
    time.sleep(5)
    sender.start()

    sender.join()
    receiver.join()
    


def RDT_send(source_address, target_address):
    """
        You need to send the system's timestamp and use it to calculate the lantency of a communication. The following code is 
        a reference code that you can modify due to differences in implementation. 

        Note that the lantency is calculated between the time the sender calls the function send() to send data and the time the receiver calls the function recv().
        params: 
            target_address:    Target IP address and its port
            source_address:    Source IP address and its port
    """
    #############################################################################
    # HINT: Since the lantency test could be finished locally. So you could
    #       assign the ProxyServerAddress as your true target address directly.
    #       you can change this code base on your implementation.
    #############################################################################
    source_address = ('127.0.0.1', 22334)
    target_address = ('127.0.0.1', 22335)

    sock = RDTSocket()
    sock.bind(source_address)
    sock.connect(target_address)
    sock.send(data=str(float(time.time() * 1000)))
    
    sock.close()

def RDT_receive(source_address):
    """
        You need to send the system's timestamp and use it to calculate the lantency of a communication. The following code is 
        a reference code that you can modify due to differences in implementation. 

        Note that the lantency is calculated between the time the sender calls the function send() to send data and the time the receiver calls the function recv().
        params: 
            source_address:    Source IP address and its port
    """
    #############################################################################
    # HINT: Since the lantency test could be finished locally. So you could
    #       assign the ProxyServerAddress as your true target address directly.
    #       you can change this code base on your implementation.
    #############################################################################
    source_address = ('127.0.0.1',22335)
    sock = RDTSocket() 
    sock.bind(source_address)
    server_sock = sock.accept()
    data = server_sock.recv()
    spend_time = float(time.time() * 1000) - float(data.PAYLOAD)
    print(f"RDT lantency : {spend_time} ms")



        

def test_latency():
    # UDP
    try:
        UDP_start_test()
    except Exception as e:
        print(e)

    # Yours
    try:
        RDT_start_test()
    except Exception as e:
        print(e)




if __name__ == '__main__':
    test_latency()
    
