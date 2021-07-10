import socket
from typing import List


class Client:

    def __init__(self, name: str, connect: (int, str)):
        self.name = name
        self.connect = connect
        pass

    def openLobby(self) -> bool:
        pass

    def joinLobby(self, lobbyId: str) -> bool:
        pass

    def OnTurn(self) -> bool:
        pass

    def getLobbyist(self) -> List[str]:
        pass

    def ping(self) -> float:
        pass

    def sendTurn(self, commitment: dict):  # {name, commitment # 0 = hold -1 = fold}
        pass

    def getPlayerCommitment(self) -> (bool, int, int):
        pass

    def setLobbyParameter(self, money, smallBlind, bigBlind, playerNum, BotNum) -> str:
        pass

    def playAgain(self) -> bool:
        pass

    def leveLobby(self) -> bool:
        pass

    def disconnect(self) -> bool:
        pass

    def getServerPool(self) -> dict:
        return {
            "OpenCards": 0,
            "OpenCardsType": ...,
            "moneyPool": ...,
            "winner": ...,
            "ifWinner": False,
            "onwCards": [...],
            "name": self.name
        }
        pass


