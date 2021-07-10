import socket
import threading
from datetime import datetime


class ClientConnection:

    def __init__(self, clientSocket: socket.socket, clientAddress):
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.name = ""
        self.clientName = str(clientAddress[0]) + ':' + str(clientAddress[1])
        self.lobby = None
        self.playAgain = False
        self.localPool = {}
        self.onTurn = False

    def startHandler(self):
        pass

    def commitment(self):
        pass

    def connection(self):

        def joinLobby(name):
            for lobby in Lobby_list:
                if lobby.name == name:
                    # TODO confirm
                    self.lobby = lobby
                    self.lobby.addPlayer(self)

        def getLobbyList():
            lobbies = []
            for lobby in Lobby_list:
                lobbies.append(lobby.name)
            # TODO send lobbies

        def ping():
            pass
            # TODO send Null

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

        def sendServerPool():
            # TODO send Pool
            pass

        def OnTurn():
            # TODO send self.onTurn
            pass

        def sendTurn():
            # TODO Bliat
            pass

        # TODO get dict from client
        # {command...} openLobby joinLobby getLobbyList disconnect getServerPool leveLobby
        # OnTurn sendTurn
        data = {"command": "openLobby"}
        pass

    def send(self):
        pass

    def onTure(self):
        pass

    def showdown(self, midCards, Winner):
        pass

    def get_name(self):
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
        self.acPlayers = 0
        self.Vars = -0
        self.globalPool = {}
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
    clientClass.get_name()
    clientClass.startHandler()


def openLobby(name, money, smallBlind, bigBlind, playerNum, player0):
    lobby = Lobby(name)
    lobby.setParm(money, smallBlind, bigBlind, playerNum)
    lobby.addPlayer(player0)
    Lobby_list.append(lobby)
    return lobby


if __name__ == '__main__':
    Lobby_list = []
    HOST = ""
    PORT = 62435
    VERSION = "0.0"
    rMODES = ["C", "L", "G", "P"]  # C -> connect | L -> Lobby | G -> Gema | P -> Ping
    Update = False

