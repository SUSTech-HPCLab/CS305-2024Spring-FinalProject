import json

class RDTHeader():
    def __init__(self, SYN: int = 0, FIN: int = 0, ACK: int = 0, SEQ: int = 0, SEQACK: int = 0, LEN: int = 0, CHECKSUM: int = 0, PAYLOAD = None, RWND: int = 0)  -> None:
        self.SYN = SYN                      # SYN flag, 1 byte
        self.FIN = FIN                      # FIN flag, 1 byte
        self.ACK = ACK                      # ACK flag, 1 byte
        self.SEQ = SEQ                      # Sequence number, 4 bytes
        self.SEQACK = SEQACK                # ACK sequence number, 4 bytes
        self.LEN = LEN                      # Length of the payload, 4 bytes
        self.RWND = RWND                    # Receiver window size, 4 bytes
        self.CHECKSUM = CHECKSUM            # Checksum, 2 bytes
        self.PAYLOAD = PAYLOAD              # Payload
        
        self.test_case = None               # Test case identifier, 1 byte
        self.Source_address = (None, None)  # Source IP and port, 6 bytes
        self.Target_address = (None, None)  # Target IP and port, 6 bytes

    def to_bytes(self):
        json_data =  {
            "SYN": self.SYN.to_bytes(1, 'big').hex(),
            "FIN": self.FIN.to_bytes(1, 'big').hex(),
            "ACK": self.ACK.to_bytes(1, 'big').hex(),
            "SEQ": self.SEQ.to_bytes(4, 'big').hex(),  
            "SEQACK": self.SEQACK.to_bytes(4, 'big').hex(),
            "LEN": self.LEN.to_bytes(4, 'big').hex(),
            # "CWND": self.CWND.to_bytes(4, 'big').hex(),
            "RWND": self.RWND.to_bytes(4, 'big').hex(),
            "CHECKSUM": self.CHECKSUM.to_bytes(2, 'big').hex(),
            "PAYLOAD": self.PAYLOAD if isinstance(self.PAYLOAD, str) else self.PAYLOAD.hex() if self.PAYLOAD else None,
            "test_case": self.test_case.to_bytes(1, 'big').hex(),
            "Source_address": f"{self.Source_address[0]}:{self.Source_address[1]}",
            "Target_address": f"{self.Target_address[0]}:{self.Target_address[1]}"
        }
        return json.dumps(json_data).encode()
    

    def from_bytes(self, data):
        data = json.loads(data)
        self.SYN = int.from_bytes(bytes.fromhex(data["SYN"]), 'big')
        self.FIN = int.from_bytes(bytes.fromhex(data["FIN"]), 'big')
        self.ACK = int.from_bytes(bytes.fromhex(data["ACK"]), 'big')
        self.SEQ = int.from_bytes(bytes.fromhex(data["SEQ"]), 'big') if data["SEQ"] else None
        self.SEQACK = int.from_bytes(bytes.fromhex(data["SEQACK"]), 'big') if data["SEQACK"] else None
        self.LEN = int.from_bytes(bytes.fromhex(data["LEN"]), 'big')
        self.RWND = int.from_bytes(bytes.fromhex(data["RWND"]), 'big')
        self.CHECKSUM = int.from_bytes(bytes.fromhex(data["CHECKSUM"]), 'big')
        # self.CWND = int.from_bytes(bytes.fromhex(data["CWND"]), 'big')
        self.PAYLOAD = data['PAYLOAD']
        self.test_case = int.from_bytes(bytes.fromhex(data["test_case"]), 'big')
        source = data["Source_address"].split(':')
        target = data["Target_address"].split(':')
        self.source_address = (source[0], int(source[1]))
        self.target_address = (target[0], int(target[1]))

        return self


