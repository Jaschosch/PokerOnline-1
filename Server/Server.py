import socket
import threading
from datetime import datetime
from typing import List


class ClientConnection:

    def __init__(self, clientSocket: socket.socket, clientAddress):
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.name = ""
        self.clientName = str(clientAddress[0]) + ':' + str(clientAddress[1])
        self.lobby = None
        self.playAgain = False
        self.localPool = {
            'HandCards': []
        }
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
        self.PlayerList: List[ClientConnection] = []
        self.onTurn = -1
        self.acPlayers = 0
        self.Vars = -0
        self.globalPool = {
            'OpenedCards': [],
            'Pot': [],
            'Ingame': [],
            'AllIn': [],
            'check': 1,
            'stapel': list(range(52)),
            'Showdown': 0
        }
        x = 1
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

    def showdown(self, Ingame):

        Ingame = [Ingame, []]

        for _ in Ingame[0]:

            Ingame[1].append(0)

            x = [sorted(self.globalPool['OpenedCards'] + self.PlayerList[1].localPool['PlayerCards']), [], []]

            for __ in x[0]:

                x[1].append(__ % 13)

                x[2].append(int(__ / 13))

            z = []
            # Straight(-Flush)
            for __ in range(6, 0, -1):

                if x[1][__] - 1 == x[1][__ - 1]:

                    z.append(__)

                else:

                    z = []

                if len(z) == 5:

                    Ingame[1][Ingame[0].index(_)] = 400 + x[1][z[0]]

                    for ___ in range(5): z[___] = x[2][x[1].index(z[___])]

                    if z.count(0) == 5 or z.count(1) == 5 or z.count(2) == 5 or z.count(3) == 5:

                        Ingame[1][Ingame[0].index(_)] += 400

                    break

            z = []
            # Flush
            for __ in range(4):

                if x[2].count(__) >= 5 and Ingame[1][Ingame[0].index(_)] < 500:

                    Ingame[1][Ingame[0].index(_)] = 500

                    for ___ in x[0]:

                        if x[2][x[0].index(___)] == __:

                            z.append(___)

                    for ___ in range(len(z)):

                        Ingame[1][Ingame[0].index(_)] += 0.5 * x[1][x[0].index(z[___])] / (10 ** (len(z) - ___))
            # Quads
            for __ in range(4):

                if x[1].count(x[1][__]) >= 4 and Ingame[1][Ingame[0].index(_)] < 700:

                    Ingame[1][Ingame[0].index(_)] = 700 + x[1][__]

                    break
            # Trips(Full House)
            for __ in range(6, 1, -1):

                if x[1].count(sorted(x[1])[__]) == 3:

                    for ___ in range(5, -1, -1):

                        if x[1].count(sorted(x[1])[__]) >= 2 and sorted(x[1])[__] != sorted(x[1])[___] and Ingame[1][Ingame[0].index(_)] < 600:

                            Ingame[1][Ingame[0].index(_)] = 600 + sorted(x[1])[__] + sorted(x[1])[___] / 20

                    if Ingame[1][Ingame[0].index(_)] < 300:

                        Ingame[1][Ingame[0].index(_)] = 300 + sorted(x[1])[__]

                        a = sorted(x[1])

                        for __ in range(2): a.remove(sorted(x[1])[__])

                        for ___ in range(6):

                            Ingame[1][Ingame[0].index(_)] += 0.5 * a[___] / (10 ** (6 - ___))
            # (2) Pair
            for __ in range(6, 0, -1):

                if x[1].count(sorted(x[1])[__]) == 2:

                    for ___ in range(6, 0, -1):

                        if x[1].count(sorted(x[1])[___]) == 2 and sorted(x[1])[__] != sorted(x[1])[___] and Ingame[1][Ingame[0].index(_)] < 200:

                            Ingame[1][Ingame[0].index(_)] = 200 + sorted(x[1])[__] + sorted(x[1])[___] / 100

                            a = x[1]

                            for ____ in range(2):

                                a.remove(sorted(x[1])[__])

                                a.remove(sorted(x[1])[___])

                            for ____ in range(3):

                                Ingame[1][Ingame[0].index(_)] += 0.5 * sorted(x[1])[____] / (10 ** (3 - ____))

                            break

                    if Ingame[1][Ingame[0].index(_)] < 100:

                        Ingame[1][Ingame[0].index(_)] = 100 + x[1][__]

                        a = x[1]

                        for ___ in range(2): a.remove(sorted(x[1])[__])

                        for ___ in range(5): Ingame[1][Ingame[0].index(_)] += 0.5 * sorted(x[1])[___] / (10 ** (5 - ___))
            # High Card
            if not Ingame[1][Ingame[0].index(_)]:

                Ingame[1][Ingame[0].index(_)] = max(x[1])

                for __ in range(6):

                    Ingame[1][Ingame[0].index(_)] += 0.5 * sorted(x[1])[__] / (10 ** (6 - __))
        # Who Wins?
        for _ in range(len(Ingame[0])):

            if Ingame[1][0] < max(Ingame[1]):

                del Ingame[0][0]

                del Ingame[1][0]

            else:

                Ingame[0].append(Ingame[0][0])

                Ingame[1].append(Ingame[1][0])

                del Ingame[0][0]

                del Ingame[1][0]

        return Ingame

    def Handler(self):

        self.maxMoneyInRound += self.NextPlayer()

        for _ in self.globalPool['Ingame']:

            if self.globalPool['OpenedCards'][_] != self.maxMoneyInRound:

                break

            elif _ == self.globalPool['Ingame'][-1]:

                if self.globalPool['check'] == len(self.globalPool['Ingame']):

                    self.globalPool['check'] = 1

                if len(self.globalPool['OpenedCards']) == 5:

                    Ingame = self.globalPool['Ingame'] + self.globalPool['AllIn']

                    self.globalPool['Showdown'] = self.showdown(Ingame)

                elif len(self.globalPool['OpenedCards']) in range(3, 5):

                    self.globalPool['OpenedCards'].append(self.globalPool['stapel'][0])

                    del self.globalPool['stapel'][0]

                else:

                    for __ in range(3):

                        self.globalPool['OpenedCards'].append(self.globalPool['stapel'][0])

                        del self.globalPool['stapel'][0]


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

