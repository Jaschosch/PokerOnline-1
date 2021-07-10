import socket
import threading
import time
from datetime import datetime


class ClientConnection:

    def __init__(self, clientSocket, clientAddress):
        self.clientSocket = clientSocket
        self. clientAddress = clientAddress
        self.name = ""
        self.clientName = str(clientAddress[0]) + ':' + str(clientAddress[1])
        self.game = None
        self.lobby = None
        self.localPool = {}

    def commitment(self):
        pass

    def connection(self):
        pass

    def send(self):
        pass

    def handler(self):
        pass


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
        self.acPlayers = -1
        self.Vars = -0
        self.globalPool = {}
        self.maxMoneyInRound = 0

    def setParm(self, money, smallBlind, bigBlind, playerNum):
        self.money, self.smallBlind, self.bigBlind, self.playerNum = money, smallBlind, bigBlind, playerNum

    def addPlayer(self, player: ClientConnection):
        self.PlayerList.append(player)

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
        #
        #
        #
        self.maxMoneyInRound += self.NextPlayer()
        #
        #
        #
        #
        #
        #
        #
        pass


def openServer() -> socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(0)
    print(f"@SERVER :: online {datetime.now().strftime('%Y.%m.%d -> %H:%M:%S')}")


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


def clientConnection(clientSocket, clientAddress):
    clientClass = ClientConnection(clientSocket, clientAddress)
    pass


if __name__ == '__main__':
    HOST = ""
    PORT = 62435
    VERSION = "0.0"
    rMODES = ["C", "L", "G", "P"]  # C -> connect | L -> Lobby | G -> Gema | P -> Ping
    Update = False

