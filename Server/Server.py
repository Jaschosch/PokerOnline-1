import socket
import threading
from datetime import datetime
from typing import List
import pickle
import random as rand


class ClientConnection:

    def __init__(self, client_socket: socket.socket, client_address):
        self.clientSocket = client_socket
        self.clientAddress = client_address
        self.name = ""
        self.clientName = str(client_address[0]) + ':' + str(client_address[1])
        self.lobby = None
        self.playAgain = False
        self.localPool = {'Cards': [-1, -1],
                          'Money': ...}
        self.onTurn_val = False
        self.online = False
        self.get_name()
        self.connect()

    def commitment(self, val):
        pass

    def connect(self):

        # {command...}
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

        # data = {"command": 0, "val": None}
        while self.online:
            try:
                data = pickle.loads(self.clientSocket.recv(1024))
                print(data)
                if data["command"] == _ping:
                    self.send("pong")
                elif data["command"] == _commitment:
                    self.commitment(data["val"])
                elif data["command"] == _openLobby:
                    self.lobby = open_lobby(data["val"]["name"], data["val"]["money"], data["val"]["smallBlind"],
                                            data["val"]["playerNum"], self)
                    self.send(True)
                elif data["command"] == _joinLobby:
                    name = data["val"]
                    x = True
                    for lobby in Lobby_list:
                        if lobby.name == name:
                            self.lobby = lobby
                            self.lobby.add_player(self)
                            self.send("confirm")
                            x = False
                    if x:
                        self.send("not")
                elif data["command"] == _getLobbyList:
                    lobbies = []
                    for lobby in Lobby_list:
                        lobbies.append(lobby.lobby_infos())
                    self.send(lobbies)
                elif data["command"] == _disconnect:
                    for lobby in Lobby_list:
                        if self in lobby.PlayerList:
                            lobby.del_player(self)
                    self.clientSocket.close()
                elif data["command"] == _getLocalPool:
                    self.send(self.localPool)
                elif data["command"] == _getServerPool:
                    if self.lobby:
                        self.send(self.lobby.globalPool)
                elif data["command"] == _leveLobby:
                    for lobby in Lobby_list:
                        if self in lobby.PlayerList:
                            lobby.del_player(self)
                    self.lobby = None
                    self.send("don")
                elif data["command"] == _OnTurn:
                    self.send(self.onTurn_val)
                else:
                    self.send("ERROR Invalid key")
            except Exception as e:
                print(f"{'=' * 100}\n@ClientConnection name : {self.name}, {self.clientName} : ERROR at RECV "
                      f"{datetime.now().strftime(TIME_FORMAT)}"
                      f"\n \n \t {e} \n{'=' * 100}")
                self.online = False

    def send(self, data):
        try:
            self.clientSocket.send(pickle.dumps(data))
        except Exception as e:
            print(f"{'=' * 100}\n@ClientConnection name : {self.name}, {self.clientName} : ERROR at SEND "
                  f"{datetime.now().strftime(TIME_FORMAT)}"
                  f"\n \n \t {e} \n{'=' * 100}")

    def on_ture(self, turn):
        self.onTurn_val = turn

    def showdown(self):
        pass

    def get_name(self):
        self.name = pickle.loads(self.clientSocket.recv(1024))["N"]
        self.online = True
        print(f"@ClientConnection name : {self.name}, {self.clientName}")


class Lobby:

    def __init__(self, name):
        self.name = name
        self.money = None
        self.small_blind = 10
        self.big_blind = self.small_blind * 2
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
            'Raise': self.big_blind,
            'Players': ...,
            'Blinds': [0, 1],
            'Turn': 0
        }
        self.maxMoneyInRound = 0

    def lobby_infos(self):
        return 'EYYOOOOOOOOOOOOOOOOOO'

    def hand_out_cards(self):
        pass

    def set_parm(self, money, small_blind, player_num):
        self.money, self.small_blind, self.big_blind, self.playerNum = money, small_blind, 2 * small_blind, player_num

    def add_player(self, player: ClientConnection):
        self.PlayerList.append(player)
        self.acPlayers += 1

    def del_player(self, player: ClientConnection):
        self.PlayerList.remove(player)
        self.acPlayers -= 1

    def start_game(self):
        pass

    def end_game(self):
        pass

    def end_round(self):
        pass

    def open_next_card(self):
        pass

    def set_cards(self):
        pass

    def next_player(self):
        pass

    def showdown(self):
        pass

    def handler(self):
        pass


class Lobby1:

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

    def HandOutCards(self):
        pass

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

            x = [sorted(self.globalPool['OpenedCards']+self.PlayerList[1].localPool['Cards']), [], []]

            for __ in x[0]:

                x[1].append(__ % 13)

                x[2].append(int(__ / 13))

            z = []
            # Straight(-Flush)
            for __ in range(6, 0, -1):

                if x[1][__] - 1 == x[1][__ - 1]: z.append(__)

                else: z = []

                if len(z) == 5:

                    Ingame[1][Ingame[0].index(_)] = 400 + x[1][z[0]]

                    for ___ in range(5): z[___] = x[2][x[1].index(z[___])]

                    if z.count(0) == 5 or z.count(1) == 5 or z.count(2) == 5 or z.count(3) == 5: Ingame[1][Ingame[0].index(_)] += 400

                    break

            z = []
            # Flush
            for __ in range(4):

                if x[2].count(__) >= 5 and Ingame[1][Ingame[0].index(_)] < 500:

                    Ingame[1][Ingame[0].index(_)] = 500

                    for ___ in x[0]:

                        if x[2][x[0].index(___)] == __: z.append(___)

                    for ___ in range(len(z)): Ingame[1][Ingame[0].index(_)] += 0.5 * x[1][x[0].index(z[___])] / (10 ** (len(z) - ___))
            # Quads
            for __ in range(4):

                if x[1].count(x[1][__]) >= 4 and Ingame[1][Ingame[0].index(_)] < 700:

                    Ingame[1][Ingame[0].index(_)] = 700 + x[1][__]

                    break
            # Trips(Full House)
            for __ in range(6, 1, -1):

                if x[1].count(sorted(x[1])[__]) == 3:

                    for ___ in range(5, -1, -1):

                        if x[1].count(sorted(x[1])[__]) >= 2 and sorted(x[1])[__] != sorted(x[1])[___] and Ingame[1][Ingame[0].index(_)] < 600: Ingame[1][Ingame[0].index(_)] = 600 + sorted(x[1])[__] + sorted(x[1])[___] / 20

                    if Ingame[1][Ingame[0].index(_)] < 300:

                        Ingame[1][Ingame[0].index(_)] = 300 + sorted(x[1])[__]

                        a = sorted(x[1])

                        for __ in range(2): a.remove(sorted(x[1])[__])

                        for ___ in range(6): Ingame[1][Ingame[0].index(_)] += 0.5 * a[___] / (10 ** (6 - ___))
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

                            for ____ in range(3): Ingame[1][Ingame[0].index(_)] += 0.5 * sorted(x[1])[____] / (10 ** (3 - ____))

                            break

                    if Ingame[1][Ingame[0].index(_)] < 100:

                        Ingame[1][Ingame[0].index(_)] = 100 + x[1][__]

                        a = x[1]

                        for ___ in range(2): a.remove(sorted(x[1])[__])

                        for ___ in range(5): Ingame[1][Ingame[0].index(_)] += 0.5 * sorted(x[1])[___] / (10 ** (5 - ___))
            # High Card
            if not Ingame[1][Ingame[0].index(_)]:

                Ingame[1][Ingame[0].index(_)] = max(x[1])

                for __ in range(6): Ingame[1][Ingame[0].index(_)] += 0.5 * sorted(x[1])[__] / (10 ** (6 - __))
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

                if self.globalPool['check'] == len(self.globalPool['Ingame']): self.globalPool['check'] = 1

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


def open_server(HOST, PORT) -> socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(0)
    print(f"@SERVER :: online {datetime.now().strftime('%Y.%m.%d -> %H:%M:%S')}")
    return sock


def version_control():
    pass


def validation(client_socket, client_address):
    key = client_socket.recv(16)
    if key == b'gtzfh667zuioukj8':
        client_socket.send(bytes(str(client_address[0]) + ':' + str(client_address[1]), 'utf-8'))
        return True
    return False


def connections_handler(server: socket.socket):
    client_socket, client_address = server.accept()
    if validation(client_socket, client_address):
        threading.Thread(target=client_connection, args=(client_socket, client_address)).start()


def client_connection(client_socket, client_address):
    ClientConnection(client_socket, client_address)


def open_lobby(name, money, small_blind, player_num, player0):
    lobby = Lobby(name)
    lobby.set_parm(money, small_blind, player_num)
    lobby.add_player(player0)
    Lobby_list.append(lobby)
    return lobby


if __name__ == '__main__':
    TIME_FORMAT = '%Y.%m.%d -> %H:%M:%S'
    Lobby_list = []
    VERSION = "0.0"
    rMODES = ["C", "L", "G", "P"]  # C -> connect | L -> Lobby | G -> Gema | P -> Ping
    Update = False
    sock = open_server("", 62435)
    print("Server Online:", sock.getsockname())
    connections_handler(sock)
    while True:
        inp = input(": ")

        if inp == "1":
            print(Lobby_list)

        if inp == "2":
            sock.close()
            exit(0)
