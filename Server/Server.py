import socket
import threading
from datetime import datetime
import pickle


class ClientConnection:

    def __init__(self, clientSocket: socket.socket, clientAddress):
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.name = ""
        self.clientName = str(clientAddress[0]) + ':' + str(clientAddress[1])
        self.lobby = None
        self.playAgain = False
        self.localPool = {}
        self.onTurn_val = False
        self.online = False

    def startHandler(self):
        try:
            self.get_name()
            while self.online:
                self.connection()
        except Exception as e:
            print(f"{'=' * 100}\n@ClientConnection name : {self.name}, {self.clientName} : ERROR at "
                  f"{datetime.now().strftime(TIME_FORMAT)}"
                  f"\n \n \t {e} \n{'=' * 100}")
            del self

    def commitment(self, val):
        pass

    def connection(self):

        def joinLobby(name):
            x = True
            for lobby in Lobby_list:
                if lobby.name == name:
                    self.lobby = lobby
                    self.lobby.addPlayer(self)
                    self.send("confirm")
                    x = False
            if x:
                self.send("not")

        def getLobbyList():
            lobbies = []
            for lobby in Lobby_list:
                lobbies.append(lobby.name)
            self.send(lobbies)

        def ping():
            self.send("pong")

        def disconnect():
            for lobby in Lobby_list:
                if self in lobby.PlayerList:
                    lobby.delPlayer(self)
            self.clientSocket.close()
            del self

        def leveLobby():
            for lobby in Lobby_list:
                if self in lobby.PlayerList:
                    lobby.delPlayer(self)
            self.send("don")

        def sendServerPool():
            self.send(self.localPool)

        def OnTurn():
            self.send(self.onTurn_val)

        def sendInvalid():
            self.send("ERROR Invalid key")

        # {command...}

        _openLobby = 17841
        _joinLobby = 5114
        _getLobbyList = 1338
        _disconnect = 2116
        _getServerPool = 8167
        _leveLobby = 2641
        _OnTurn = 1651
        _commitment = 1646
        _ping = 0

        # data = {"command": 0, "val": None}

        try:
            data = pickle.loads(self.clientSocket.recv(1024))
            if data["command"] == _ping:
                ping()
            if data["command"] == _commitment:
                self.commitment(data["val"])
            if data["command"] == _openLobby:
                self.lobby = openLobby(data["val"]["name"], data["val"]["money"], data["val"]["smallBlind"],
                                       data["val"]["bigBlind"], data["val"]["playerNum"], self)
                self.send(True)
            if data["command"] == _joinLobby:
                joinLobby(data["val"])
            if data["command"] == _getLobbyList:
                getLobbyList()
            if data["command"] == _disconnect:
                disconnect()
            if data["command"] == _getServerPool:
                sendServerPool()
            if data["command"] == _leveLobby:
                leveLobby()
            if data["command"] == _OnTurn:
                OnTurn()
            else:
                sendInvalid()
        except Exception as e:
            print(f"{'='*100}\n@ClientConnection name : {self.name}, {self.clientName} : ERROR at "
                  f"{datetime.now().strftime(TIME_FORMAT)}"
                  f"\n \n \t {e} \n{'='*100}")
            del self
        pass

    def send(self, data):
        try:
            self.clientSocket.send(bytes(str(pickle.dumps(data), "utf-8")))
        except Exception as e:
            print(f"{'='*100}\n@ClientConnection name : {self.name}, {self.clientName} : ERROR at "
                  f"{datetime.now().strftime(TIME_FORMAT)}"
                  f"\n \n \t {e} \n{'='*100}")

    def onTure(self, turn):
        self.onTurn_val = turn

    def showdown(self, midCards, Winner):
        pass

    def get_name(self):
        self.name = eval(str(self.clientSocket.recv(1024), "utf-8"))["N"]
        self.online = True
        print(f"@ClientConnection name : {self.name}, {self.clientName}")


class Lobby:

    def __init__(self, name):
        self.name = name
        self.money = None
        self.smallBlind = None
        self.bigBlind = None
        self.playerNum = None
        self.BotNum = None
        self.PlayerList = []
        self.onTurn = -1
        self.acPlayers = 0
        self.Vars = -0
        self.globalPool = {
            'OpenedCards': [],
            'Pot': []
        }
        self.maxMoneyInRound = 0

    def setParm(self, money, smallBlind, bigBlind, playerNum):
        self.money, self.smallBlind, self.bigBlind, self.playerNum = money, smallBlind, bigBlind, playerNum

    def addPlayer(self, player: ClientConnection):
        self.PlayerList.append(player)
        self.acPlayers += 1

    def delPlayer(self, player: ClientConnection):
        self.PlayerList.remove(player)
        self.acPlayers -= 1

    def startGame(self):
        pass

    def endGame(self):
        pass

    def openNextCard(self):
        pass

    def setCards(self):
        pass

    def NextPlayer(self):
        pass

    def showdown(self):
        pass

    def Handler(self):

        self.maxMoneyInRound += self.NextPlayer()

        for _ in Ingame:

            if self.globalPool['OpenedCards'][_] != self.maxMoneyInRound:

                break

            elif _ == Ingame[-1]:

                if check == len(Ingame):
                    check = 1

                if len(self.globalPool['OpenedCards']) == 5:

                    Ingame = Ingame + AllIn

                    Showdown = showdown(Ingame)

                elif len(self.globalPool['OpenedCards']) in range(3, 5):

                    self.globalPool['OpenedCards'].append(stapel[0])

                    del stapel[0]

                else:

                    for __ in range(3):
                        self.globalPool['OpenedCards'].append(stapel[0])

                        del stapel[0]


def openServer() -> socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(0)
    print(f"@SERVER :: online {datetime.now().strftime(TIME_FORMAT)}")


def versionControl():
    pass


def validation(clientSocket, clientAddress):
    key = clientSocket.recv(16)
    if key == b'gtzfh667zuioukj8':
        clientSocket.send(bytes(str(clientAddress[0]) + ':' + str(clientAddress[1]), 'utf-8'))
        return True
    return False


def connections_handler(server: socket.socket):
    clientSocket, clientAddress = server.accept()
    if validation(clientSocket, clientAddress):
        threading.Thread(target=clientConnection, args=(clientSocket, clientAddress)).start()


def openLobby(name, money, smallBlind, bigBlind, playerNum, player0):
    lobby = Lobby(name)
    lobby.setParm(money, smallBlind, bigBlind, playerNum)
    lobby.addPlayer(player0)
    Lobby_list.append(lobby)
    return lobby


def clientConnection(clientSocket, clientAddress):
    clientClass = ClientConnection(clientSocket, clientAddress)
    clientClass.startHandler()


if __name__ == '__main__':
    TIME_FORMAT = '%Y.%m.%d -> %H:%M:%S'
    Lobby_list = []
    HOST = ""
    PORT = 62435
    VERSION = "0.0"
    Update = False
