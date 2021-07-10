import socket
import threading
from datetime import datetime
from typing import List
import pickle
import random as rand


class ClientConnection:

    def __init__(self, clientSocket: socket.socket, clientAddress):
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        self.name = ""
        self.clientName = str(clientAddress[0]) + ':' + str(clientAddress[1])
        self.lobby = None
        self.playAgain = False
        self.localPool = {'Cards': [-1, -1],
                          'Money': ...}
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
        self.SBlind = 10
        self.BBlind = 20
        self.playerNum = None
        self.BotNum = None
        self.PlayerList: List[ClientConnection] = []
        self.onTurn = -1
        self.acPlayers = 0
        self.globalPool = {
            'OpenedCards': [],
            'Pot': [],
            'Ingame': [],
            'AllIn': [],
            'check': 1,
            'stapel': list(range(52)),
            'Showdown': 0,
            'Raise': self.BBlind,
            'Players': ...,
            'Blinds': [0, 1],
            'Turn': 0
        }
        x = 1
        self.maxMoneyInRound = 0

    def HandOutCards(self): pass

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

    def endRound(self, Showdown):

        a = 0

        for _ in range(len(self.globalPool['Pot'])):

            a += self.globalPool['Pot'][_]

            self.globalPool['Pot'] = 0

        for _ in range(len(Showdown)):

            self.PlayerList[Showdown[_]].localPool['Money'] += int(a / (len(Showdown) - _))

            Showdown -= int(a / (len(Showdown) - _))

        self.globalPool['Blinds'][0] = (self.globalPool['Blinds'][0] + 1) % self.globalPool['Players']

        self.globalPool['Blinds'][1] = (self.globalPool['Blinds'][1] + 1) % self.globalPool['Players']

        self.globalPool['Turn'] = (self.globalPool['Blinds'][1] + 1) % self.globalPool['Players']

        self.globalPool['Raise'] = self.BBlind

        self.globalPool = {
            'OpenedCards': [],
            'Pot': [],
            'Ingame': list(range(self.acPlayers)),
            'AllIn': [],
            'check': 1,
            'stapel': list(range(52)),
            'Showdown': 0,
            'Raise': self.BBlind
        }

        self.HandOutCards()

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

            x = [sorted(self.globalPool['OpenedCards'] + self.PlayerList[1].localPool['Cards']), [], []]

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
    TIME_FORMAT = '%Y.%m.%d -> %H:%M:%S'
    Lobby_list = []
    HOST = ""
    PORT = 62435
    VERSION = "0.0"
    rMODES = ["C", "L", "G", "P"]  # C -> connect | L -> Lobby | G -> Gema | P -> Ping
    Update = False

