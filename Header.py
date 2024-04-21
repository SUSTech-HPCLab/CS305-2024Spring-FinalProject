import json

class TCPHeader():
    def __init__(self, SYN: int = 0, FIN: int = 0, ACK: int = 0, SEQ: int = 0, SEQACK: int = 0, LEN: int = 0, CHECKSUM: int = 0, PAYLOAD = None, CWND: int = 0, AWND: int = 0)  -> None:
        self.SYN = SYN                  # 1 bytes
        self.FIN = FIN                  # 1 bytes
        self.ACK = ACK                  # 1 bytes
        self.SEQ = SEQ                  # 4 bytes
        self.SEQACK = SEQACK            # 4 bytes
        self.LEN = LEN                  # 4 bytes
        self.CHECKSUM = CHECKSUM        # 2 bytes
        self.PAYLOAD = PAYLOAD          # Data LEN bytes
        # self.CWND = CWND                # Congestion window size 4 bytes
        self.AWND = AWND                # Notification window size 4 bytes
        
    def to_bytes(self):
        json_data =  {
            "SYN": self.SYN.to_bytes(1, 'big').hex(),
            "FIN": self.FIN.to_bytes(1, 'big').hex(),
            "ACK": self.ACK.to_bytes(1, 'big').hex(),
            "SEQ": self.SEQ.to_bytes(4, 'big').hex(),  
            "SEQACK": self.SEQACK.to_bytes(4, 'big').hex(),
            "LEN": self.LEN.to_bytes(4, 'big').hex(),
            # "CWND": self.CWND.to_bytes(4, 'big').hex(),
            "AWND": self.AWND.to_bytes(4, 'big').hex(),
            "CHECKSUM": self.CHECKSUM.to_bytes(2, 'big').hex(),
            "PAYLOAD": self.PAYLOAD if isinstance(self.PAYLOAD, str) else self.PAYLOAD.hex() if self.PAYLOAD else None
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
        self.CHECKSUM = int.from_bytes(bytes.fromhex(data["CHECKSUM"]), 'big')
        self.AWND = int.from_bytes(bytes.fromhex(data["AWND"]), 'big')
        # self.CWND = int.from_bytes(bytes.fromhex(data["CWND"]), 'big')
        
        self.PAYLOAD = data['PAYLOAD']

        return self

    def __str__(self) -> str:
        """
        Overwrite the toString function of this class
        """
        return f'SYN: {self.SYN}, FIN: {self.FIN}, ACK: {self.ACK}, SEQ: {self.SEQ}, SEQACK: {self.SEQACK}, LEN: {self.LEN}, CHECKSUM: {self.CHECKSUM}, PAYLOAD: {self.PAYLOAD}'
