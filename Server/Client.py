import socket
from typing import List
import pickle
import time
from datetime import datetime

TIME_FORMAT = '%Y.%m.%d -> %H:%M:%S'


def decode2(data):
    return data


def encode1(data):
    return data


class Client:
    _openLobby = 17841
    _joinLobby = 5114
    _getLobbyList = 1338
    _disconnect = 2116
    _getServerPool = 8167
    _leveLobby = 2641
    _OnTurn = 1651
    _commitment = 1646
    _ping = 0
    HOST = '127.0.0.1'
    PORT = 62435
    TIME_FORMAT = '%Y.%m.%d -> %H:%M:%S'
    VERSION = "0.0"
    Update = False

    def __init__(self, name: str, connect: (int, str)):
        self.name = name
        self.connect = connect
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientName = None
        pass

    def firstConnection(self):
        self.connection.connect((Client.HOST, Client.PORT))
        self.connection.send(b'gtzfh667zuioukj8')
        self.clientName = str(self.connection.recv(512), "utf-8")
        x = {"N": self.name}
        self.connection.send(pickle.dumps(x))
        self.ping()

    def openLobby(self, val) -> bool: # money, smallBlind, bigBlind, playerNum
        self.send(Client._openLobby, val)
        return self.getData()

    def joinLobby(self, lobbyId: str):
        self.send(Client._joinLobby, lobbyId)
        return self.getData()

    def OnTurn(self) -> bool:
        self.send(Client._OnTurn, None)
        return self.getData()

    def getLobbyList(self) -> List[str]:
        self.send(Client._getLobbyList, None)
        return self.getData()

    def ping(self) -> float:
        t1 = time.time()
        self.send(0, None)
        return time.time() - t1

    def sendTurn(self, commitment: int):  # 0 = hold -1 = fold -2 = allin}
        self.send(Client._commitment, commitment)

    def leveLobby(self):
        self.send(Client._leveLobby, None)
        return self.getData()

    def disconnect(self):
        self.send(Client._disconnect, None)

    def getServerPool(self) -> dict:
        self.send(Client._getServerPool, None)
        print(self.getData())
        return {
            "OpenCards": [45, 60],
            "OpenCardsType": ...,
            "moneyPool": ...,
            "winner": ...,
            "ifWinner": False,
            "onwCards": [...],
            "name": self.name,
            "pl": [1200, 120, ]
        }
        pass

    def send(self, command, val):
        x = {"command": command,
             "val": val}
        try:
            self.connection.send(bytes(str(pickle.dumps(x), "utf-8")))
        except Exception as e:
            print(f"{'=' * 100}\n@ClientConnection name : {self.name}, {self.clientName} : ERROR at "
                  f"{datetime.now().strftime(TIME_FORMAT)}"
                  f"\n \n \t {e} \n{'=' * 100}")

    def getData(self):
        return pickle.loads(self.connection.recv(1024))
