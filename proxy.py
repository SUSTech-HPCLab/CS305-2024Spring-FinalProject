
import string
import socket
import random
import copy
import time
from Header import RDTHeader
import threading
import concurrent.futures

lock = threading.Lock()
buffer_lock = threading.Lock()
    
connection_pool = {}
test_buffer_pool = {}
case_test_status_pool = {}
num_test = 16

def randSleep(min, max):
    delay = random.randint(min, max) * 0.001
    time.sleep(delay)




    

    
def case_test(pkt, outSock: socket.socket):
    global connection_pool
    global test_buffer_pool
    global case_test_status_pool
    global num_test

    try:
        header = RDTHeader().from_bytes(pkt)
        addr = header.tgt
        test_case = header.test_case

        lock.acquire()

        if f"{header.src}-{header.tgt}" not in connection_pool.keys() and f"{header.tgt}-{header.src}" not in connection_pool.keys():
            connection_pool[f"{header.src}-{header.tgt}"] = []
            test_buffer_pool[f"{header.src}-{header.tgt}"] = []
        
            case_test_status_pool[f"{header.src}-{header.tgt}"] = []

            for i in range(0, num_test):
                case_test_status_pool[f"{header.src}-{header.tgt}"].append(False)


        if header.test_case != 20:
            connection_key = f"{header.src}-{header.tgt}" if f"{header.src}-{header.tgt}" in connection_pool.keys() else f"{header.tgt}-{header.src}"
            connection_pool[connection_key].append(header)
        else:

            outSock.sendto(pkt, addr)

        lock.release()
    
        

        
        if test_case == 0:
            if len(connection_pool[connection_key]) == 1:
                outSock.sendto(pkt, addr)
            else:
                outSock.sendto(pkt, addr)
                lock.acquire()
                case_test_status_pool[connection_key][test_case] = True

                lock.release()

        if test_case == 5:

            bottle_neck = 5
            if len(connection_pool[connection_key]) == 1:
                lock.acquire()
                case_test_status_pool[connection_key][test_case] = True
                lock.release()

            if len(test_buffer_pool[connection_key]) > bottle_neck:
                pass

            else:
                buffer_lock.acquire()
                test_buffer_pool[connection_key].append(header)
                buffer_lock.release()

                outSock.sendto(pkt, addr)
                randSleep(min=5, max=10) 

                buffer_lock.acquire()
                test_buffer_pool[connection_key].remove(header)
                buffer_lock.release()

           



    except Exception as e:
        print(e)
        lock.release()
        buffer_lock.release()
        
    finally:
        lock.release()
        buffer_lock.release()
    
    
def listener(ReceiveSock: socket.socket, outSock: socket.socket):
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        while True:
            try:
                print("Try to receive data...")
                pkt = ReceiveSock.recv(1024)

                executor.submit(case_test, pkt, outSock)
            except socket.error as e:
                print(e)
                lock.release()
                buffer_lock.release()
            





def clean_connection():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sock.bind(("127.0.0.1", 12234))

    while True:
        try:
            data  = server_sock.recv(1024)
            data = data.decode()
            lock.acquire()
            try:
                if data in connection_pool.keys():
                    del connection_pool[data]
            except Exception as e:
                print(e)
            try:
                if data in test_buffer_pool.keys():
                    del test_buffer_pool[data]
            except Exception as e:
                print(e)

            try:
                if data in case_test_status_pool.keys():
                    del case_test_status_pool[data]
            except Exception as e:
                print(e)

            lock.release()
            print(f"[PROXY] Delete connection :{data}")
        except Exception as e:
            lock.release()
            print(e)
        finally:
            pass
           

def result():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("127.0.0.1", 12230))

    server_sock.listen(5)
    while True:
        client_sock, client_addr = server_sock.accept()
        try:
            data = client_sock.recv(1024)
            key = data.decode().split(":")
            response = case_test_status_pool[key[0]][int(key[1])]
            client_sock.sendall(str(response).encode())
        except Exception as e:
            print(e)
        finally:
            client_sock.close()

        




if __name__ == '__main__':

    fromSenderAddr = ('127.0.0.1', 12345)
    toReceiverAddr = ('127.0.0.1', 12346)
    fromReceiverAddr = ('127.0.0.1', 12347)
    toSenderAddr = ('127.0.0.1', 12348)

    fromSenderSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fromSenderSock.bind(fromSenderAddr)
    fromReceiverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    fromReceiverSock.bind(fromReceiverAddr)

    outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print ("Listening...")
    threading.Thread(target=listener, daemon=True, args=(fromSenderSock, outSock)).start()
    threading.Thread(target=listener, daemon=True, args=(fromReceiverSock, outSock)).start()
    threading.Thread(target=clean_connection, daemon=True).start()
    threading.Thread(target=result, daemon=True).start()
    while True:
        pass
