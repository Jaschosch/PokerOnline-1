import socket
from typing import List
import string
import threading


def decode2(data):
    return data


def encode1(data):
    return data


class Client:

    def __init__(self, name: str, connect: (int, str)):
        self.name = name
        self.connect = connect
        pass

    def joinLobby(self, lobbyId: str) -> bool:
        pass

    def OnTurn(self) -> bool:
        pass

    def getLobbyList(self) -> List[str]:
        pass

    def ping(self) -> float:
        pass

    def sendTurn(self, commitment: int):  # 0 = hold -1 = fold -2 = allin}
        pass

    def OpenLobby(self, name, money, smallBlind, bigBlind, playerNum) -> str:
        pass

    def playAgain(self) -> bool:
        pass

    def leveLobby(self) -> bool:
        pass

    def disconnect(self) -> bool:
        pass

    def getServerPool(self) -> dict:
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


