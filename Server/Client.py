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
    _getServerPool = 8147
    _getLocalPool = 8167
    _leveLobby = 2641
    _OnTurn = 1651
    _commitment = 1646
    _ping = 0
    HOST = '127.0.0.1'
    PORT = 62435
    TIME_FORMAT = '%Y.%m.%d -> %H:%M:%S'
    VERSION = "0.0"
    Update = False

    def __init__(self, name: str, connect: (str, int)):
        self.name = name
        self.connect = connect
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientName = None
        pass

    def first_connection(self):
        self.connection.connect(self.connect)
        self.connection.send(b'gtzfh667zuioukj8')
        self.clientName = str(self.connection.recv(512), "utf-8")
        print(self.clientName)
        x = {"N": self.name}
        self.connection.send(pickle.dumps(x))
        ping = self.ping()
        print(f"@Client connected with Server at : {self.connection.getsockname()} \n"
              f"\t@{self.name} -> ping {ping}ms")

    def open_lobby(self, val) -> bool:  # money, smallBlind, bigBlind, playerNum
        print("openLobby")
        self.send(Client._openLobby, val)
        return self.get_data()

    def join_lobby(self, lobbyId: str):
        self.send(Client._joinLobby, lobbyId)
        return self.get_data()

    def on_turn(self) -> bool:
        self.send(Client._OnTurn, None)
        return self.get_data()

    def get_lobbyList(self) -> List[str]:
        self.send(Client._getLobbyList, None)
        return self.get_data()

    def ping(self) -> float:
        t1 = time.time()
        self.send(0, None)
        return time.time() - t1

    def send_turn(self, commitment: int):  # 0 = hold -1 = fold -2 = allin}
        self.send(Client._commitment, commitment)

    def leve_lobby(self):
        self.send(Client._leveLobby, None)
        return self.get_data()

    def disconnect(self):
        self.send(Client._disconnect, None)

    def get_server_pool(self) -> dict:
        self.send(Client._getServerPool, None)
        return self.get_data()

    def get_local_pool(self) -> dict:
        self.send(Client._getLocalPool, None)
        return self.get_data()

    def send(self, command, val):
        x = {"command": command,
             "val": val}
        try:
            self.connection.send(pickle.dumps(x))
        except Exception as e:
            print(f"{'=' * 100}\n@ClientConnection name : {self.name}, {self.clientName} : ERROR at "
                  f"{datetime.now().strftime(TIME_FORMAT)}"
                  f"\n \n \t {e} \n{'=' * 100}")

    def get_data(self):
        return pickle.loads(self.connection.recv(1024))

    def test_client_server(self):
        pass


if __name__ == '__main__':
    c = Client("Markin", ("0.0.0.0", 62435))
    c.first_connection()
    time.sleep(2)
    print(c.open_lobby({"name": "test", "money": "10K", "smallBlind": "2.5t", "playerNum": 10}))
    print(c.open_lobby({"name": "test1", "money": "10K", "smallBlind": "2.5t", "playerNum": 10}))
    print(c.open_lobby({"name": "test2", "money": "10K", "smallBlind": "2.5t", "playerNum": 10}))
    print(c.open_lobby({"name": "test3", "money": "10K", "smallBlind": "2.5t", "playerNum": 10}))
    print(c.open_lobby({"name": "te5s4t", "money": "10K", "smallBlind": "2.5t", "playerNum": 10}))
    print(c.open_lobby({"name": "tes5235t", "money": "10K", "smallBlind": "2.5t", "playerNum": 10}))
    print(c.open_lobby({"name": "tes123t", "money": "10K", "smallBlind": "2.5t", "playerNum": 10}))
    print(c.open_lobby({"name": "tes132t", "money": "10K", "smallBlind": "2.5t", "playerNum": 10}))

    print("getLobbyList-> ", c.get_lobbyList())
    print("joinLobby-> ", c.join_lobby("dasda"))
    print("leveLobby-> ", c.leve_lobby())
    print("joinLobby-> ", c.join_lobby("tes132t"))
    print("leveLobby-> ", c.leve_lobby())
    print("joinLobby-> ", c.join_lobby("te5s4t"))
    print("getLobbyList-> ", c.get_lobbyList())
    print("OnTurn-> ", c.on_turn())
    print("getLocalPool-> ", c.get_local_pool())
    print("getServerPool-> ", c.get_server_pool())

    while True:
        pass
