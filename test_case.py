import socket
import time
from RDT import RDTSocket
from multiprocessing import Process
from Header import RDTHeader
import signal

# connect proxy server 

# proxy_server_address = ('10.16.52.94', 12234)   # ProxyServerAddress
# fromSenderAddr = ('10.16.52.94', 12345)         # FromSender
# toReceiverAddr = ('10.16.52.94', 12346)         # ToSender
# fromReceiverAddr = ('10.16.52.94', 12347)       # FromReceiver
# toSenderAddr = ('10.16.52.94', 12348)           # ToReceiver

# resultAddr = ('10.16.52.94', 12230)

# #TODO change the adress to your address
# sender_address = ("10.16.56.14", 12344)         # Your sender address
# receiver_address = ("10.16.56.14", 12349)       # Your receiver address



# connect locally server

proxy_server_address = ('127.0.0.1', 12234)
fromSenderAddr = ('127.0.0.1', 12345)
toReceiverAddr = ('127.0.0.1', 12346)
fromReceiverAddr = ('127.0.0.1', 12347)
toSenderAddr = ('127.0.0.1', 12348)

sender_address = ("127.0.0.1", 12244)
receiver_address = ("127.0.0.1", 12249)
resultAddr = ("127.0.0.1", 12230)
num_test_case = 16

class TimeoutException(Exception):
    pass

def handler(signum, frame):
    raise TimeoutException


# signal.signal(signal.SIGALRM, handler)

def test_case():
    sender_sock = None
    reciever_sock = None

    # TODO: You could change the range of this loop to test specific case(s) in local test.

    for i in range(num_test_case):
        if sender_sock:
            del sender_sock
        if reciever_sock:
            del reciever_sock
        sender_sock = RDTSocket()   # You can change the initialize RDTSocket()
        reciever_sock = RDTSocket() # You can change the initialize RDTSocket()
        print(f"Start test case : {i}")

        try:
            result = RDT_start_test(sender_sock, reciever_sock, sender_address, receiver_address, i)
        except Exception as e:
            print(e)
        finally:

            client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_sock.connect(resultAddr)
           
            client_sock.sendall(f"{sender_address}-{receiver_address}:{i}".encode())

            response = client_sock.recv(1024)

            client_sock.close()

            print(f"proxy result for test case {i} {response.decode()}")
            
            if response.decode() == 'True' and result:
                print(f"test case {i} pass")
            else:
                print(f"test case {i} fail")


            #############################################################################
            #TODO you should close your socket, and release the resource, this code just a 
            # demo. you should make some changes based on your code implementation or you can 
            # close them in the other places.

            sender_sock.close()
            reciever_sock.close()

        #############################################################################
            time.sleep(5)

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(f"{sender_address}-{receiver_address}".encode(), proxy_server_address) 


            time.sleep(10)
    

def RDT_start_test(sender_sock, reciever_sock, sender_address, receiver_address, test_case):
    sender = Process(target=RDT_send, args=(sender_sock, sender_address, receiver_address, test_case))
    receiver = Process(target=RDT_receive, args=(reciever_sock, receiver_address, test_case))

    receiver.start()
    time.sleep(5)
    sender.start()

    # if test_case < 5:
    #     signal.alarm(20)
    # else:
    #     signal.alarm(120)

    sender.join()
    receiver.join()
    time.sleep(1)

    # signal.alarm(0)

    if test_case < 5:
        return True
    else:
        #TODO you may need to change the path, if you want.
        return test_file_integrity('original.txt', 'transmit.txt')
    
def RDT_send(sender_sock: RDTSocket, source_address, target_address, test_case):
    """
        You should refer to your own implementation to implement this code. the sender should specify the Source_address, Target_address, and test_case in the Header of all packets sent by the receiver.
        params: 
            target_address:    Target IP address and its port
            source_address:    Source IP address and its port
            test_case:         The rank of test case
    """
    data_blocks = []
    file_path = 'original.txt' # You can modify the path of file. Howerver, if you change this file, you need to modify the input for function test_file_integrity()

    sock = sender_sock  
    sock.proxy_server_addr = fromSenderAddr

    sock.bind(source_address)
    sock.connect(target_address)

    if test_case >= 5:
        #############################################################################
            # TODO: you need to send a files. Here you need to write the code according to your own implementation.

            raise NotImplementedError
        #############################################################################
        
    else:

        #############################################################################
            # TODO: you need to send a short message. May be you can use:
            # data = "Short Message test"
            # sock.send(data=data, test_case=test_case)

            raise NotImplementedError
        #############################################################################



def RDT_receive(reciever_sock: RDTSocket, source_address, test_case):
    """
        You should refer to your own implementation to implement this code. the receiver should specify the Source_address, Target_address, and test_case in the Header of all packets sent by the receiver.
        params: 
            source_address:    Source IP address and its port
            test_case:         The rank of test case
    """
    sock = reciever_sock
    sock.proxy_server_addr = fromReceiverAddr
    sock.bind(source_address)
    server_sock = sock.accept()



    if test_case >= 5:
        #############################################################################
            # TODO: you need to receive original.txt from sender. Here you need to write the code according to your own implementation.

            # you should Save all data to the file (transmit.txt), and stop this loop when the client close the connection. 
            # After that, you need to use the following function to verify the file that you received. When test_case >= 5, the test is passed only when test_file_integrity is verified and the proxy is verified.
            raise NotImplementedError
        #############################################################################
        
    else:

        #############################################################################
            # TODO: you need to receive a short message. May be you can use:
            # data = server_sock.recv() 

            raise NotImplementedError
        #############################################################################

        

def test_file_integrity(original_path, transmit_path):
    with open(original_path, 'rb') as file1, open(transmit_path, 'rb') as file2:
        while True:
            block1 = file1.read(4096)
            block2 = file2.read(4096)
            
            if block1 != block2:
                return False
            
            if not block1:
                break

    return True      
        
if __name__ == '__main__':
    test_case()