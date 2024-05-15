import socket
import time
from RDT import RDTSocket
from multiprocessing import Process
from Header import RDTHeader

proxy_server_address = ('10.16.52.94', 12234)   # ProxyServerAddress
fromSenderAddr = ('10.16.52.94', 12345)         # FromSender
toReceiverAddr = ('10.16.52.94', 12346)         # ToSender
fromReceiverAddr = ('10.16.52.94', 12347)       # FromReceiver
toSenderAddr = ('10.16.52.94', 12348)           # ToReceiver

sender_address = ("10.16.56.14", 12344)         # Your sender address
receiver_address = ("10.16.56.14", 12349)       # Your receiver address

num_test_case = 7

def test_case():
    sender_sock = None
    reciever_sock = None
    # TODO: You could change the range of this loop to test specific case(s).
    for i in range(num_test_case):
        if sender_sock:
            del sender_sock
        if reciever_sock:
            del reciever_sock
        sender_sock = RDTSocket()   # You can change the initialize RDTSocket()
        reciever_sock = RDTSocket() # You can change the initialize RDTSocket()
        print(f"Start test case : {i}")
        try:
            RDT_start_test(sender_sock, reciever_sock, sender_address, receiver_address, i)
        except Exception as e:
            print(e)
        finally:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(f"{sender_address}-{receiver_address}".encode(), proxy_server_address) #用于清理和关闭对应的proxy连接表
    

def RDT_start_test(sender_sock, reciever_sock, sender_address, receiver_address, test_case):
    sender = Process(target=RDT_send, args=(sender_sock, sender_address, receiver_address, test_case))
    receiver = Process(target=RDT_receive, args=(reciever_sock, receiver_address, test_case))

    receiver.start()
    time.sleep(5)
    sender.start()

    sender.join()
    receiver.join()
    time.sleep(5)


def RDT_send(sender_sock: RDTSocket, source_address, target_address, test_case):
    """
        You should refer to your own implementation to implement this code. the sender should specify the Source_address, Target_address, and test_case in the Header of all packets sent by the receiver.
        params: 
            target_address:    Target IP address and its port
            source_address:    Source IP address and its port
            test_case:         The rank of test case
    """
    data_blocks = []
    file_path = 'original.txt' # You can modify the path of file.
    sock = sender_sock  
    #############################################################################
    # TIPs: You should specify the Source_address, Target_address, and test_case 
    #       fields for all packets.
    #############################################################################
    #############################################################################
    # An example to assign proxy server destination
    sock.proxy_server_addr = ("10.16.52.94", 12345)
    #############################################################################
    sock.bind(source_address)
    sock.connect(target_address)
    time.sleep(1)
    if test_case > 3:
        try:
            with open(file_path, 'rb') as file:
                while True:
                    block = file.read(1024) 
                    if not block:
                        break
                    data_blocks.append(block.decode())  
            # all_data = b''.join(data_blocks)
            all_data = ''.join(data_blocks)
            # return all_data
        except IOError as e:
            print(f"An error occurred: {e}")
        # TODO: it should be modified to sock.send(data = all_data)
        sock.send(data=all_data, test_case=test_case)
    if test_case >= 1 and test_case <= 3:
        data = "Short Message test"
        sock.send(data=data, test_case=test_case)
    sock.close()


def RDT_receive(reciever_sock: RDTSocket, source_address, test_case):
    """
        You should refer to your own implementation to implement this code. the receiver should specify the Source_address, Target_address, and test_case in the Header of all packets sent by the receiver.
        params: 
            source_address:    Source IP address and its port
            test_case:         The rank of test case
    """
    sock = reciever_sock
    #############################################################################
    # Tips: You should specify the Source_address, Target_address, and test_case 
    #       fields for all packets.
    #############################################################################
    #############################################################################
    # An example to assign proxy server destination
    sock.proxy_server_addr = ("10.16.52.94", 12347)
    #############################################################################
    sock.bind(source_address)
    server_sock = sock.accept()
    if test_case >= 1 and test_case <= 3:
        data, _ = server_sock.recv()
    elif test_case > 3:
        while True:
            data, _ = server_sock.recv()
            #############################################################################
            # TODO: Save all data to the file, and stop this loop when the client
            #       close the connection.
            break
            #############################################################################
        #############################################################################
        # TODO: You could use the following function to verify the file that you received.
        #       e.g. The original file is original.txt. The file you received has been stored
        #               to transmit.txt
        if test_file_integrity('original.txt', 'transmit.txt'):
            print("These two files are same. Verified passed.")
        #############################################################################
        

def test_file_integrity(original_path, transmit_path):
    with open(original_path, 'rb') as file1, open(transmit_path, 'rb') as file2:
        while True:
            block1 = file1.read(4096)
            block2 = file2.read(4096)
            
            if block1 != block2:
                raise Exception("Contents is different")
            
            if not block1:
                break

    return True        
        
if __name__ == '__main__':
    test_case()