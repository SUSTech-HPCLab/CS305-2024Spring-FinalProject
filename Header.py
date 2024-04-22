import json

class RDTHeader():
    def __init__(self, SYN: int = 0, FIN: int = 0, ACK: int = 0, SEQ: int = 0, SEQACK: int = 0, LEN: int = 0, CHECKSUM: int = 0, PAYLOAD = None, RWND: int = 0)  -> None:
        self.SYN = SYN                      # 1 bytes
        self.FIN = FIN                      # 1 bytes
        self.ACK = ACK                      # 1 bytes
        self.SEQ = SEQ                      # 4 bytes
        self.SEQACK = SEQACK                # 4 bytes
        self.LEN = LEN                      # 4 bytes
        self.CHECKSUM = CHECKSUM            # 2 bytes
        self.PAYLOAD = PAYLOAD              # Data LEN bytes
        # self.CWND = CWND                  # Congestion window size 4 bytes
        self.RWND = RWND                    # Notification window size 4 bytes
        
        self.test_case = None               # Notify the mid-SERVER which test case will be tesed
        self.Source_address = (None, None)  # Souce ip and port
        self.Target_address = (None, None)  # Target ip and port