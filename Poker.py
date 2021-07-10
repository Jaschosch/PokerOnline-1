import pygame as pg

import math as m

import time as t

import random as rand

from copy import *

from Karten import Cards

from Server import Client


def Int(x):

    for _ in range(len(x)):

        x[_] = int(x[_])

    return x


def Chips(P, Points, Chip):

    if P > 250:

        for _ in range(int(P / 250) - 1):

            dx, dy = Chip[3].get_width(), Chip[3].get_height()

            win.blit(Chip[3], (Points[0][0] + _ * m.sin(Points[4]) * m.ceil(dx / 25) - dx / 2,
                               Points[0][1] + _ * m.cos(Points[4]) * m.ceil(dx / 25) - dy / 2))

        P = P % 250 + 250

    if P > 50:

        for _ in range(int(P / 50) - 1):

            dx, dy = Chip[2].get_width(), Chip[2].get_height()

            win.blit(Chip[2], (Points[1][0] + _ * m.sin(Points[4]) * m.ceil(dx / 25) - dx / 2,
                               Points[1][1] + _ * m.cos(Points[4]) * m.ceil(dx / 25) - dy / 2))

        P = P % 50 + 50

    if P > 10:

        for _ in range(int(P / 10) - 1):

            dx, dy = Chip[1].get_width(), Chip[1].get_height()

            win.blit(Chip[1], (Points[2][0] + _ * m.sin(Points[4]) * m.ceil(dx / 25) - dx / 2,
                               Points[2][1] + _ * m.cos(Points[4]) * m.ceil(dx / 25) - dy / 2))

        P = P % 10 + 10

    if P >= 2:

        for _ in range(int(P / 2)):

            dx, dy = Chip[0].get_width(), Chip[0].get_height()

            win.blit(Chip[0], (Points[3][0] + _ * m.sin(Points[4]) * m.ceil(dx / 25) - dx / 2,
                               Points[3][1] + _ * m.cos(Points[4]) * m.ceil(dx / 25) - dy / 2))


def Handkarten(Player, Karten, client):

    Player[0][2] = client.getServerPool()["Handkarten"]

    for __ in range(2):

        Karten[Player[0][2][__]] = Cards(['karo-2', 'karo-3', 'karo-4', 'karo-5', 'karo-6', 'karo-7', 'karo-8', 'karo-9', 'karo-10', 'karo-bube', 'karo-dame', 'karo-koenig', 'karo-ass',
                                          'herz-2', 'herz-3', 'herz-4', 'herz-5', 'herz-6', 'herz-7', 'herz-8', 'herz-9', 'herz-10', 'herz-bube', 'herz-dame', 'herz-koenig', 'herz-ass',
                                          'pik-2', 'pik-3', 'pik-4', 'pik-5', 'pik-6', 'pik-7', 'pik-8', 'pik-9', 'pik-10', 'pik-bube', 'pik-dame', 'pik-koenig', 'pik-ass',
                                          'kreuz-2', 'kreuz-3', 'kreuz-4', 'kreuz-5', 'kreuz-6', 'kreuz-7', 'kreuz-8', 'kreuz-9', 'kreuz-10', 'kreuz-bube', 'kreuz-dame', 'kreuz-koenig', 'kreuz-ass'][Player[0][2][__]], int(252 / len(Player) + 42), int(357 / len(Player) + 60))

        Karten[Player[0][2][__]].Hand(2, __ + 1, [w / 2, h], m.degrees(- m.pi))

    return Player, Karten


def Pay(From, To, Much):

    From -= Much

    To += Much

    return From, To


def Winner(P, Players, B, M):

    run = True

    Text = [str(P[3]) + ' wins!', 'Restart', 'Quit']

    Box = [[w / 8, h / 10, 3 * w / 4, h / 5], [w / 8, 2 * h / 5, 3 * w / 4, h / 5],
           [w / 8, 7 * h / 10, 3 * w / 4, h / 5]]

    Inf = [200, 200, 200]

    Color = [0, 255, 0]

    while run:

        win.fill(Color)

        for _ in range(3):

            pg.draw.rect(win, (Color[1], Color[2], Color[0]), Box[_])

            pg.draw.rect(win, (Color[2], Color[0], Color[1]), Box[_], 2)

            dx, dy = pg.font.Font(None, int(300 - Inf[_])).size(Text[_])

            win.blit(pg.font.Font(None, int(300 - Inf[_])).render(Text[_], False, (Color[2], Color[0], Color[1])), (Box[_][0] + (Box[_][2] - dx) / 2, Box[_][1] + (Box[_][3] - dy) / 2))

        pg.display.flip()

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

                if pg.Rect(Box[1]).collidepoint(event.pos):

                    Game(Players, B, M)

                    return False

                if pg.Rect(Box[2]).collidepoint(event.pos):

                    return False

        for _ in range(3):

            if pg.Rect(Box[_]).collidepoint(pg.mouse.get_pos()):

                if Box[_][3] - h / 5 < h / 24:

                    Box[_][0] -= 0.4

                    Box[_][1] -= 0.2

                    Box[_][2] += 0.8

                    Box[_][3] += 0.4

                    Inf[_] -= 1

            elif Box[_][3] - h / 5:

                Box[_][0] += 0.4

                Box[_][1] += 0.2

                Box[_][2] -= 0.8

                Box[_][3] -= 0.4

                Inf[_] += 1

        if not Color[0] and Color[1] != 255 and Color[2] == 255:

            Color[1] += 1

        if not Color[0] and Color[1] == 255 and Color[2]:

            Color[2] -= 1

        if Color[0] != 255 and Color[1] == 255 and not Color[2]:

            Color[0] += 1

        if Color[0] == 255 and Color[1] and not Color[2]:

            Color[1] -= 1

        if Color[0] == 255 and not Color[1] and Color[2] != 255:

            Color[2] += 1

        if Color[0] and not Color[1] and Color[2] == 255:

            Color[0] -= 1


def Showdown(Player):

    while True:

        for _ in range(len(Player)):

            Color = [0, 150, 0]

            if _ in I[0]:

                Color = [255, 180, 180]

            if _ not in I[0]:

                Color = [150, 150, 150]

            pg.draw.polygon(win, Color, ((w / 2, h / 2), (
            w / 2 + m.sin(-_ * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2,
            h / 2 + m.cos(-_ * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2), (w / 2 + m.sin(
                (-_ - 0.5) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2, h / 2 + m.cos(
                (-_ - 0.5) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2), (w / 2 + m.sin(
                (-_ - 1) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2, h / 2 + m.cos(
                (-_ - 1) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2)))

            pg.draw.polygon(win, (0, 0, 0), ((w / 2, h / 2), (
            w / 2 + m.sin(-_ * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2,
            h / 2 + m.cos(-_ * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2), (w / 2 + m.sin(
                (-_ - 0.5) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2, h / 2 + m.cos(
                (-_ - 0.5) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2), (w / 2 + m.sin(
                (-_ - 1) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2, h / 2 + m.cos(
                (-_ - 1) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2)), 5)

            a = [(K[Player[_][2][0]].pos[0] + K[Player[_][2][1]].pos[0]) / 2,
                 (K[Player[_][2][0]].pos[1] + K[Player[_][2][1]].pos[1]) / 2]

        for _ in Player:

            K[_[2][0]].Draw(win)

            K[_[2][1]].Draw(win)

        for _ in Mitte[0]:

            K[_].Draw(win)

        pg.display.flip()

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:

                return I[0]

            if event.type == pg.KEYDOWN:

                return I[0]


def Reset(Mitte, Player, Karten, a):

    b = 0

    Ingame = []

    for __ in range(len(Player)):

        b += Mitte[1][__]

        Mitte[1][__] = 0

        Player[__][2] = [0, 0]

        Ingame.append(__)

    rand.shuffle(a)

    for __ in range(len(a)):

        Player[a[__]][1] += int(b / (len(a) - __))

        b -= int(b / (len(a) - __))

    for __ in range(52):

        Karten[__].open = 0

    Mitte[0] = []

    AllIn = []

    stapel = list(range(52))

    rand.shuffle(stapel)

    Player, Mitte, stapel, Karten = KartenAusteilen(Player, Mitte, stapel, Karten)

    Raise = BBlind[1]

    return Player, Karten, Mitte, stapel, Turn, Raise, Ingame, AllIn


def Test(Ingame, AllIn, Player, Mitte, Karten, stapel, Chip, SChip, BP, SBP, Turn, run, M):
#Nur noch ein Spieler übrig
    if len(Ingame) + len(AllIn) == 1:

        Ingame = Ingame + AllIn

        Player, Karten, Mitte, stapel, Turn, Raise, Ingame, AllIn = Reset(Mitte, Player, Karten, Ingame)
#ALle Spieler sind All In gegangen
    if not len(Ingame) and len(AllIn) > 1:

        for __ in range(5 - len(Mitte[0])):

            Mitte[0].append(stapel[0])

            Karten[Mitte[0][__]].open = 1

            Karten[Mitte[0][__]].pos = [w / 2 + __ * 65, h / 2]

            del stapel[0]

        for __ in AllIn:

            Karten[Player[__][2][0]].open, Karten[Player[__][2][1]].open = 1, 1

        a = Showdown(Karten, Mitte[0], deepcopy(Player), Mitte, AllIn)

        Player, Karten, Mitte, stapel, Turn, Raise, Ingame, AllIn = Reset(Mitte, Player, Karten, a)

#Spieler fliegen raus
    for _ in range(len(Player)):

        if Player[_][1] <= 0 and _ not in AllIn:

            Player[_] = False

    if False in Player:

        while False in Player:

            del Mitte[1][Player.index(False)]

            Player.remove(False)

        Ingame = []

        for _ in range(len(Player)):

            Ingame.append(_)

        Karten = ['karo-2', 'karo-3', 'karo-4', 'karo-5', 'karo-6', 'karo-7', 'karo-8', 'karo-9', 'karo-10',
                  'karo-bube', 'karo-dame', 'karo-koenig', 'karo-ass',
                  'herz-2', 'herz-3', 'herz-4', 'herz-5', 'herz-6', 'herz-7', 'herz-8', 'herz-9', 'herz-10',
                  'herz-bube', 'herz-dame', 'herz-koenig', 'herz-ass',
                  'pik-2', 'pik-3', 'pik-4', 'pik-5', 'pik-6', 'pik-7', 'pik-8', 'pik-9', 'pik-10', 'pik-bube',
                  'pik-dame', 'pik-koenig', 'pik-ass',
                  'kreuz-2', 'kreuz-3', 'kreuz-4', 'kreuz-5', 'kreuz-6', 'kreuz-7', 'kreuz-8', 'kreuz-9',
                  'kreuz-10', 'kreuz-bube', 'kreuz-dame', 'kreuz-koenig', 'kreuz-ass']

        for _ in range(len(Karten)):

            Karten[_] = Cards(Karten[_], int(252 / len(Player) + 42), int(357 / len(Player) + 60))

        stapel = list(range(52))

        rand.shuffle(stapel)

        Player, Mitte, stapel, Karten = KartenAusteilen(Player, Mitte, stapel, Karten)

        BP = []

        SBP = []

        Chip = [pg.transform.scale(pg.image.load('Chips/2.png').convert_alpha(), (int(300 / len(Player) + 25), int(300 / len(Player) + 25))),
                pg.transform.scale(pg.image.load('Chips/10.png').convert_alpha(), (int(300 / len(Player) + 25), int(300 / len(Player) + 25))),
                pg.transform.scale(pg.image.load('Chips/50.png').convert_alpha(), (int(300 / len(Player) + 25), int(300 / len(Player) + 25))),
                pg.transform.scale(pg.image.load('Chips/250.png').convert_alpha(), (int(300 / len(Player) + 25), int(300 / len(Player) + 25)))]

        SChip = [pg.transform.scale(pg.image.load('Chips/2.png').convert_alpha(), (int(195 / len(Player) + 10), int(195 / len(Player) + 10))),
                 pg.transform.scale(pg.image.load('Chips/10.png').convert_alpha(), (int(195 / len(Player) + 10), int(195 / len(Player) + 10))),
                 pg.transform.scale(pg.image.load('Chips/50.png').convert_alpha(), (int(195 / len(Player) + 10), int(195 / len(Player) + 10))),
                 pg.transform.scale(pg.image.load('Chips/250.png').convert_alpha(), (int(195 / len(Player) + 10), int(195 / len(Player) + 10)))]

        for _ in range(len(Player)):

            a = [(Karten[Player[_][2][0]].pos[0] + Karten[Player[_][2][1]].pos[0]) / 2,
                 (Karten[Player[_][2][0]].pos[1] + Karten[Player[_][2][1]].pos[1]) / 2]
            # Position der großen Chips
            BP.append([a[0] + m.sin(-_ * 2 * m.pi / len(Player)) * (Karten[Player[_][2][0]].height / 2 + Chip[0].get_width()),
                       a[1] + m.cos(-_ * 2 * m.pi / len(Player)) * (Karten[Player[_][2][0]].height / 2 + Chip[0].get_width())])

            for __ in range(4):
                BP[_].append(
                    [BP[_][0] - (1.5 - __) * m.sin(-_ * 2 * m.pi / len(Player) + m.pi / 2) * Chip[0].get_width(),
                     BP[_][1] - (1.5 - __) * m.cos(-_ * 2 * m.pi / len(Player) + m.pi / 2) * Chip[0].get_width()])

            BP[_].append(-_ * 2 * m.pi / len(Player))

            for __ in range(2): del BP[_][0]
            # Position der kleinen Chips
            SBP.append([a[0] - m.sin(-_ * 2 * m.pi / len(Player)) * (
                        Karten[Player[_][2][0]].height / 2 + SChip[0].get_width() / 2 + 2),
                        a[1] - m.cos(-_ * 2 * m.pi / len(Player)) * (
                                    Karten[Player[_][2][0]].height / 2 + SChip[0].get_width() / 2) + 2])

            for __ in range(4):
                SBP[_].append(
                    [SBP[_][0] - (1.5 - __) * m.sin(-_ * 2 * m.pi / len(Player) + m.pi / 2) * SChip[0].get_width(),
                     SBP[_][1] - (1.5 - __) * m.cos(-_ * 2 * m.pi / len(Player) + m.pi / 2) * SChip[0].get_width()])

            SBP[_].append(-_ * 2 * m.pi / len(Player) + m.pi)

            for __ in range(2): del SBP[_][0]
#Ein Spieler gewinnt
    if len(Player) == 1:

        run = Winner(Player[0], *M)

    return Ingame, AllIn, Player, Mitte, Karten, Chip, SChip, stapel, BP, SBP, Turn, run


def Enter(Karten, Player, Turn, Ingame, Mitte, Raise, run, stapel, Chip, SChip, BP, SBP, AllIn, M, client):

    Karten[Player[Turn][2][0]].open, Karten[Player[Turn][2][1]].open = 0, 0

    a = Turn
#Next Turn
    if Turn == Ingame[-1]:

        Turn = Ingame[0]

    else:

        Turn = Ingame[Ingame.index(Turn) + 1]

#AllIn
    if Player[a][1] <= Raise - Mitte[1][a]:

        AllIn.append(a)

        Ingame.remove(a)

        Player[a][1], Mitte[1][a] = Pay(Player[a][1], Mitte[1][a], Player[a][1])

        client.sendTurn(-2)

#Fold
    elif Raise < max(Mitte[1]):

        Ingame.remove(a)

        client.sendTurn(-1)
#Check & Call
    elif Raise == Mitte[1][a]:

        client.sendTurn(0)

        if run != len(Ingame):

            run += 1

            Raise = max(Mitte[1])

            return Karten, Player, Turn, Ingame, Mitte, Raise, run, stapel, Chip, SChip, BP, SBP, AllIn
#Raise
    else:

        client.sendTurn(Raise - Mitte[1][a])

        Player[a][1], Mitte[1][a] = Pay(Player[a][1], Mitte[1][a], Raise - Mitte[1][a])

        run = 1

    Raise = max(Mitte[1])

    for _ in Ingame:

        if Mitte[1][_] != Raise:

            break

        elif _ == Ingame[-1]:

            if run == len(Ingame):

                run = 1

            if len(Mitte[0]) == 5:

                Ingame = Ingame + AllIn

                for __ in Ingame:

                    Karten[Player[__][2][0]].open, Karten[Player[__][2][1]].open = 1, 1

                a = Showdown(Karten, Mitte[0], deepcopy(Player), Mitte, Ingame)

                Player, Karten, Mitte, stapel, Turn, Raise, Ingame, AllIn = Reset(Mitte, Player, Karten, a)

            if len(Mitte[0]) == 4:

                Mitte[0].append(stapel[0])

                Karten[Mitte[0][4]].open = 1

                Karten[Mitte[0][4]].pos = [w / 2 + 260, h / 2]

                del stapel[0]

            if len(Mitte[0]) == 3:

                Mitte[0].append(stapel[0])

                Karten[Mitte[0][3]].open = 1

                Karten[Mitte[0][3]].pos = [w / 2 + 195, h / 2]

                del stapel[0]

            if not len(Mitte[0]) and Mitte[1][0]:

                for __ in range(3):

                    Mitte[0].append(stapel[0])

                    Karten[Mitte[0][__]].open = 1

                    Karten[Mitte[0][__]].pos = [w / 2 + __ * 65, h / 2]

                    del stapel[0]

    Ingame, AllIn, Player, Mitte, Karten, Chip, SChip, stapel, BP, SBP, Turn, run = Test(Ingame, AllIn, Player, Mitte, Karten, stapel, Chip, SChip, BP, SBP, Turn, run, M)

    return Karten, Player, Turn, Ingame, Mitte, Raise, run, stapel, Chip, SChip, BP, SBP, AllIn


def Info(P, M, Raise):

    font = pg.font.Font(None, 100)

    Grey = pg.Surface((int(w), int(h)))

    Grey.fill((200, 200, 200))

    Grey.set_alpha(200)

    win.blit(Grey, (0, 0))

    HKarten = [Cards(['karo-2', 'karo-3', 'karo-4', 'karo-5', 'karo-6', 'karo-7', 'karo-8', 'karo-9', 'karo-10', 'karo-bube', 'karo-dame', 'karo-koenig', 'karo-ass',
              'herz-2', 'herz-3', 'herz-4', 'herz-5', 'herz-6', 'herz-7', 'herz-8', 'herz-9', 'herz-10', 'herz-bube', 'herz-dame', 'herz-koenig', 'herz-ass',
              'pik-2', 'pik-3', 'pik-4', 'pik-5', 'pik-6', 'pik-7', 'pik-8', 'pik-9', 'pik-10', 'pik-bube', 'pik-dame', 'pik-koenig', 'pik-ass',
              'kreuz-2', 'kreuz-3', 'kreuz-4', 'kreuz-5', 'kreuz-6', 'kreuz-7', 'kreuz-8', 'kreuz-9', 'kreuz-10', 'kreuz-bube', 'kreuz-dame', 'kreuz-koenig', 'kreuz-ass'][P[2][0]], int(126 * h / 716), int(h / 4)), Cards(['karo-2', 'karo-3', 'karo-4', 'karo-5', 'karo-6', 'karo-7', 'karo-8', 'karo-9', 'karo-10', 'karo-bube', 'karo-dame', 'karo-koenig', 'karo-ass',
              'herz-2', 'herz-3', 'herz-4', 'herz-5', 'herz-6', 'herz-7', 'herz-8', 'herz-9', 'herz-10', 'herz-bube', 'herz-dame', 'herz-koenig', 'herz-ass',
              'pik-2', 'pik-3', 'pik-4', 'pik-5', 'pik-6', 'pik-7', 'pik-8', 'pik-9', 'pik-10', 'pik-bube', 'pik-dame', 'pik-koenig', 'pik-ass',
              'kreuz-2', 'kreuz-3', 'kreuz-4', 'kreuz-5', 'kreuz-6', 'kreuz-7', 'kreuz-8', 'kreuz-9', 'kreuz-10', 'kreuz-bube', 'kreuz-dame', 'kreuz-koenig', 'kreuz-ass'][P[2][1]], int(126 * h / 716), int(h / 4))]

    for _ in range(2):

        HKarten[_].pos = [w / 2 + (2 * _ - 1) * (126 * h / 1432 + 2), 3 * h / 4]

        HKarten[_].open = 1

    MKarten = []

    for _ in M:

        MKarten.append(Cards(['karo-2', 'karo-3', 'karo-4', 'karo-5', 'karo-6', 'karo-7', 'karo-8', 'karo-9', 'karo-10', 'karo-bube', 'karo-dame', 'karo-koenig', 'karo-ass',
              'herz-2', 'herz-3', 'herz-4', 'herz-5', 'herz-6', 'herz-7', 'herz-8', 'herz-9', 'herz-10', 'herz-bube', 'herz-dame', 'herz-koenig', 'herz-ass',
              'pik-2', 'pik-3', 'pik-4', 'pik-5', 'pik-6', 'pik-7', 'pik-8', 'pik-9', 'pik-10', 'pik-bube', 'pik-dame', 'pik-koenig', 'pik-ass',
              'kreuz-2', 'kreuz-3', 'kreuz-4', 'kreuz-5', 'kreuz-6', 'kreuz-7', 'kreuz-8', 'kreuz-9', 'kreuz-10', 'kreuz-bube', 'kreuz-dame', 'kreuz-koenig', 'kreuz-ass'][_], int(126 * h / 716), int(h / 4)))

    for _ in range(len(M)):

        MKarten[_].pos = [w / 2 + (2 * _ - len(M) / 2) * (126 * h / 1432 + 2), 3 * h / 8]

        MKarten[_].open = 1

    for _ in MKarten + HKarten:

        _.Draw(win)

    dx, dy = font.size(str(P[1]) + '$')

    win.blit(font.render(str(P[1]) + '$', False, (50, 50, 50)), ((w - dx) / 2, 15 * h / 16 - dy / 2))

    dx, dy = font.size(str(Raise) + '$')

    win.blit(font.render(str(Raise) + '$', False, (50, 50, 50)), ((w - dx) / 2, 9 * h / 16 - dy / 2))


def Pause(P, B, M):

    run = True

    Text = ['Resume', 'Restart', 'Quit']

    Box = [[w / 8, h / 10, 3 * w / 4, h / 5], [w / 8, 2 * h / 5, 3 * w / 4, h / 5],
           [w / 8, 7 * h / 10, 3 * w / 4, h / 5]]

    Inf = [200, 200, 200]

    while run:

        win.fill((150, 150, 150))

        for _ in range(3):

            pg.draw.rect(win, (Inf[_], Inf[_], Inf[_]), Box[_])

            pg.draw.rect(win, (Inf[_] + 50, Inf[_] + 50, Inf[_] + 50), Box[_], 2)

            dx, dy = pg.font.Font(None, int(300 - Inf[_])).size(Text[_])

            win.blit(pg.font.Font(None, int(300 - Inf[_])).render(Text[_], False, (Inf[_] + 50, Inf[_] + 50, Inf[_] + 50)), (Box[_][0] + (Box[_][2] - dx) / 2, Box[_][1] + (Box[_][3] - dy) / 2))

        pg.display.flip()

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

                if pg.Rect(Box[0]).collidepoint(event.pos):

                    return True

                if pg.Rect(Box[1]).collidepoint(event.pos):

                    Game(P, B, M)

                    return False

                if pg.Rect(Box[2]).collidepoint(event.pos):

                    return False

        for _ in range(3):

            if pg.Rect(Box[_]).collidepoint(pg.mouse.get_pos()):

                if Box[_][3] - h / 5 < h / 24:

                    Box[_][0] -= 0.4

                    Box[_][1] -= 0.2

                    Box[_][2] += 0.8

                    Box[_][3] += 0.4

                    Inf[_] -= 1

            elif Box[_][3] - h / 5:

                Box[_][0] += 0.4

                Box[_][1] += 0.2

                Box[_][2] -= 0.8

                Box[_][3] -= 0.4

                Inf[_] += 1


def Game(P, B, M, Name):

    Karten = ['karo-2', 'karo-3', 'karo-4', 'karo-5', 'karo-6', 'karo-7', 'karo-8', 'karo-9', 'karo-10', 'karo-bube', 'karo-dame', 'karo-koenig', 'karo-ass',
              'herz-2', 'herz-3', 'herz-4', 'herz-5', 'herz-6', 'herz-7', 'herz-8', 'herz-9', 'herz-10', 'herz-bube', 'herz-dame', 'herz-koenig', 'herz-ass',
              'pik-2', 'pik-3', 'pik-4', 'pik-5', 'pik-6', 'pik-7', 'pik-8', 'pik-9', 'pik-10', 'pik-bube', 'pik-dame', 'pik-koenig', 'pik-ass',
              'kreuz-2', 'kreuz-3', 'kreuz-4', 'kreuz-5', 'kreuz-6', 'kreuz-7', 'kreuz-8', 'kreuz-9', 'kreuz-10', 'kreuz-bube', 'kreuz-dame', 'kreuz-koenig', 'kreuz-ass']

    stapel = list(range(52))

    Player = []

    Mitte = [[], []]

    Ingame = []

    AllIn = []

    client = Client.Client(Name, ('127.0.0.1', 62435))

    for _ in range(P + B):

        Player.append([_, M, [0, 0]])

        Mitte[1].append(0)

        Ingame.append(_)

    for _ in range(len(Karten)):

        Karten[_] = Cards(Karten[_], int(252 / len(Player) + 42), int(357 / len(Player) + 60))              #126, 179

    rand.shuffle(stapel)

    Chip = [pg.transform.scale(pg.image.load('Chips/2.png').convert_alpha(), (int(300 / len(Player) + 25), int(300 / len(Player) + 25))),
            pg.transform.scale(pg.image.load('Chips/10.png').convert_alpha(), (int(300 / len(Player) + 25), int(300 / len(Player) + 25))),
            pg.transform.scale(pg.image.load('Chips/50.png').convert_alpha(), (int(300 / len(Player) + 25), int(300 / len(Player) + 25))),
            pg.transform.scale(pg.image.load('Chips/250.png').convert_alpha(), (int(300 / len(Player) + 25), int(300 / len(Player) + 25)))]

    SChip = [pg.transform.scale(pg.image.load('Chips/2.png').convert_alpha(), (int(195 / len(Player) + 10), int(195 / len(Player) + 10))),
             pg.transform.scale(pg.image.load('Chips/10.png').convert_alpha(), (int(195 / len(Player) + 10), int(195 / len(Player) + 10))),
             pg.transform.scale(pg.image.load('Chips/50.png').convert_alpha(), (int(195 / len(Player) + 10), int(195 / len(Player) + 10))),
             pg.transform.scale(pg.image.load('Chips/250.png').convert_alpha(), (int(195 / len(Player) + 10), int(195 / len(Player) + 10)))]

    Player, Mitte, stapel, Karten = KartenAusteilen(Player, Mitte, stapel, Karten)

    BP = []

    SBP = []

    for _ in range(len(Player)):

        a = [(Karten[Player[_][2][0]].pos[0] + Karten[Player[_][2][1]].pos[0]) / 2,
             (Karten[Player[_][2][0]].pos[1] + Karten[Player[_][2][1]].pos[1]) / 2]
#Position der großen Chips
        BP.append([a[0] + m.sin(-_ * 2 * m.pi / len(Player)) * (Karten[Player[_][2][0]].height / 2 + Chip[0].get_width()),
                   a[1] + m.cos(-_ * 2 * m.pi / len(Player)) * (Karten[Player[_][2][0]].height / 2 + Chip[0].get_width())])

        for __ in range(4):

            BP[_].append([BP[_][0] - (1.5 - __) * m.sin(-_ * 2 * m.pi / len(Player) + m.pi / 2) * Chip[0].get_width(),
                          BP[_][1] - (1.5 - __) * m.cos(-_ * 2 * m.pi / len(Player) + m.pi / 2) * Chip[0].get_width()])

        BP[_].append(-_ * 2 * m.pi / len(Player))

        for __ in range(2): del BP[_][0]
#Position der kleinen Chips
        SBP.append([a[0] - m.sin(-_ * 2 * m.pi / len(Player)) * (Karten[Player[_][2][0]].height / 2 + SChip[0].get_width() / 2 + 2),
                    a[1] - m.cos(-_ * 2 * m.pi / len(Player)) * (Karten[Player[_][2][0]].height / 2 + SChip[0].get_width() / 2) + 2])

        for __ in range(4):

            SBP[_].append([SBP[_][0] - (1.5 - __) * m.sin(-_ * 2 * m.pi / len(Player) + m.pi / 2) * SChip[0].get_width(),
                           SBP[_][1] - (1.5 - __) * m.cos(-_ * 2 * m.pi / len(Player) + m.pi / 2) * SChip[0].get_width()])

        SBP[_].append(-_ * 2 * m.pi / len(Player) + m.pi)

        for __ in range(2): del SBP[_][0]

    Raise = BBlind[1]

    Turn = 0

    font = pg.font.Font(None, 50)

    run = 1

    while run:
#Draw Playground & other Chips
        for _ in range(len(Player)):
#Draw Playground
            Color = [0, 150, 0]

            if _ == client.getServerPool()['SBlind']:

                Color = [0, 50, 255]

            if _ == client.getServerPool()['BBlind']:

                Color = [205, 255, 0]

            if _ == Turn:

                Color = [255, 50, 0]

            if _ not in Ingame:

                Color = [150, 150, 150]

            if _ in AllIn:

                Color = [150, 50, 150]

            pg.draw.polygon(win, Color, ((w / 2, h / 2), (
            w / 2 + m.sin(-_ * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2,
            h / 2 + m.cos(-_ * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2), (w / 2 + m.sin(
                (-_ - 0.5) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2, h / 2 + m.cos(
                (-_ - 0.5) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2), (w / 2 + m.sin(
                (-_ - 1) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2, h / 2 + m.cos(
                (-_ - 1) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2)))

            pg.draw.polygon(win, (0, 0, 0), ((w / 2, h / 2), (
            w / 2 + m.sin(-_ * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2,
            h / 2 + m.cos(-_ * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2), (w / 2 + m.sin(
                (-_ - 0.5) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2, h / 2 + m.cos(
                (-_ - 0.5) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2), (w / 2 + m.sin(
                (-_ - 1) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2, h / 2 + m.cos(
                (-_ - 1) * 2 * m.pi / len(Player) + m.pi / len(Player)) * w * 2)), 5)
#Draw Chips of other Players

            '''a = [(Karten[Player[_][2][0]].pos[0] + Karten[Player[_][2][1]].pos[0]) / 2,
                 (Karten[Player[_][2][0]].pos[1] + Karten[Player[_][2][1]].pos[1]) / 2]

            b = [1, 1]

            if int(Player[_][1] / 250) >= 1: b[0] = 1.5

            elif int(Player[_][1] / 50) >= 1: b[0] = 1

            elif int(Player[_][1] / 10) >= 1: b[0] = 0.5

            else: b[0] = 0

            if int(Mitte[1][_] / 250) >= 1: b[1] = 1.5

            elif int(Mitte[1][_] / 50) >= 1: b[1] = 1

            elif int(Mitte[1][_] / 10) >= 1: b[1] = 0.5

            else: b[1] = 0'''

            if _ != Turn:

                '''for __ in range(int(b[0] * 2 + 1)):

                    BP[_][__ + 2] = [BP[_][0] - (b[0] - __) * m.sin(-_ * 2 * m.pi / len(Player) + m.pi / 2) * Chip[0].get_width(),
                                     BP[_][1] - (b[0] - __) * m.cos(-_ * 2 * m.pi / len(Player) + m.pi / 2) * Chip[0].get_width()]

                for __ in range(int(b[1] * 2) + 1):

                    SBP[_][__ + 2] = [SBP[_][0] - (b[1] - __) * m.sin(-_ * 2 * m.pi / len(Player) + m.pi / 2) * SChip[0].get_width(),
                                      SBP[_][1] - (b[1] - __) * m.cos(-_ * 2 * m.pi / len(Player) + m.pi / 2) * SChip[0].get_width()]'''

                Chips(Player[_][1], BP[_], Chip)

                Chips(Mitte[1][_], SBP[_], SChip)
#Draw your Chips
        a = [(Karten[Player[Turn][2][0]].pos[0] + Karten[Player[Turn][2][1]].pos[0]) / 2,
             (Karten[Player[Turn][2][0]].pos[1] + Karten[Player[Turn][2][1]].pos[1]) / 2]

        if Raise < max(Mitte[1]) and Player[Turn][1] > Raise:

            Chips(Player[Turn][1], BP[Turn], Chip)

            dx, dy = font.size('Fold?')

            win.blit(font.render('Fold?', False, (150, 50, 150)), (a[0] - m.sin(-Turn * 2 * m.pi / len(Player)) * (Karten[Player[Turn][2][0]].height / 2 + 50) - dx / 2,
                                                                     a[1] - m.cos(-Turn * 2 * m.pi / len(Player)) * (Karten[Player[Turn][2][0]].height / 2 + 50) - dy / 2))

        else:

            Chips(Player[Turn][1] - Raise + Mitte[1][Turn], BP[Turn], Chip)

            Chips(Raise, SBP[Turn], SChip)
#Draw all Cards
        for _ in Karten:

            _.Draw(win)

        if pg.key.get_pressed()[pg.K_i]: Info(Player[Turn], Mitte[0], Raise)

        pg.display.flip()

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if pg.Rect(Karten[Player[Turn][2][0]].pos[0] - Karten[Player[Turn][2][0]].dx / 2,
                               Karten[Player[Turn][2][0]].pos[1] - Karten[Player[Turn][2][0]].dy / 2,
                               Karten[Player[Turn][2][0]].dx, Karten[Player[Turn][2][0]].dy).collidepoint(event.pos) \
                            or pg.Rect(Karten[Player[Turn][2][1]].pos[0] - Karten[Player[Turn][2][1]].dx / 2,
                                       Karten[Player[Turn][2][1]].pos[1] - Karten[Player[Turn][2][1]].dy / 2,
                                       Karten[Player[Turn][2][1]].dx, Karten[Player[Turn][2][1]].dy).collidepoint(event.pos):

                        Karten[Player[Turn][2][0]].open = not Karten[Player[Turn][2][0]].open

                        Karten[Player[Turn][2][1]].open = not Karten[Player[Turn][2][1]].open

                if event.button == 4:

                    if Raise < max(Mitte[1]):

                        Raise = max(Mitte[1])

                    elif Raise + 2 <= Player[Turn][1] + Mitte[1][Turn]:

                        Raise += 2

                    else:

                        Raise = Player[Turn][1] + Mitte[1][Turn]

                if event.button == 5:

                    if Raise - 2 >= max(Mitte[1]):

                        Raise -= 2

                    elif Player[Turn][1] < max(Mitte[1]):

                        Raise = int((Player[Turn][1] - 1) / 2) * 2

                    else:

                        Raise = max(Mitte[1]) - 2

                if event.button == 3:

                    Karten, Player, Turn, Ingame, Mitte, Raise, run, stapel, Chip, SChip, BP, SBP, AllIn = Enter(Karten, Player, Turn, Ingame, Mitte, Raise, run, stapel, Chip, SChip, BP, SBP, AllIn, [P, B, M], client)

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:

                    run = Pause(P, B, M)

                if event.key == pg.K_SPACE:

                    Karten[Player[Turn][2][0]].open = not Karten[Player[Turn][2][0]].open

                    Karten[Player[Turn][2][1]].open = not Karten[Player[Turn][2][1]].open

                if event.key == pg.K_UP:

                    if Raise < max(Mitte[1]):

                        Raise = max(Mitte[1])

                    elif Raise + 2 <= Player[Turn][1] + Mitte[1][Turn]:

                        Raise += 2

                    else:

                        Raise = Player[Turn][1] + Mitte[1][Turn]

                if event.key == pg.K_DOWN:

                    if Raise - 2 >= max(Mitte[1]):

                        Raise -= 2

                    elif Player[Turn][1] < max(Mitte[1]):

                        Raise = int((Player[Turn][1] - 1) / 2) * 2

                    else:

                        Raise = max(Mitte[1]) - 2

                if event.key == pg.K_RETURN:

                    Karten, Player, Turn, Ingame, Mitte, Raise, run, stapel, Chip, SChip, BP, SBP, AllIn = Enter(Karten, Player, Turn, Ingame, Mitte, Raise, run, stapel, Chip, SChip, BP, SBP, AllIn, [P, B, M], client)

pg.init()

win = pg.display.set_mode((0, 0), 0)#pg.FULLSCREEN)

w, h = win.get_size()

run = True

Bots = 2

Players = 1

SBlind = 10

BBlind = 20

Money = 100

Text = ['Start', '100 $', 'Small Blind = 10', 'Big Blind = 20', '1 Player', '2 Bots', 'Quit']

Box = [[w / 8, h / 13, 5 * w / 16, 2 * h / 13], [9 * w / 16, h / 13, 5 * w / 16, 2 * h / 13],
       [w / 8, 4 * h / 13, 5 * w / 16, 2 * h / 13], [9 * w / 16, 4 * h / 13, 5 * w / 16, 2 * h / 13],
       [w / 8, 7 * h / 13, 5 * w / 16, 2 * h / 13], [9 * w / 16, 7 * h / 13, 5 * w / 16, 2 * h / 13],
       [w / 8, 10 * h / 13, 3 * w / 4, 2 * h / 13]]

Inf = []

for _ in range(len(Box)):

    Inf.append(200)

while run:

    win.fill((150, 150, 150))

    for _ in range(len(Box)):

        pg.draw.rect(win, Int([Inf[_], Inf[_], Inf[_]]), Box[_])

        pg.draw.rect(win, Int([Inf[_] + 50, Inf[_] + 50, Inf[_] + 50]), Box[_], 2)

        dx, dy = pg.font.Font(None, int(300 - Inf[_])).size(Text[_])

        win.blit(pg.font.Font(None, int(300 - Inf[_])).render(Text[_], False, (Inf[_] + 50, Inf[_] + 50, Inf[_] + 50)), (Box[_][0] + (Box[_][2] - dx) / 2, Box[_][1] + (Box[_][3] - dy) / 2))

    pg.display.flip()

    for event in pg.event.get():

        if event.type == pg.MOUSEBUTTONDOWN:

            x = 1

            if pg.mouse.get_pressed()[1]:

                x = 10

            if pg.Rect(Box[0]).collidepoint(event.pos) and event.button == 1:

                Game(Players, Bots, [(-2) % (Players + Bots), SBlind], [(-1) % (Players + Bots), BBlind], Money)

            if pg.Rect(Box[1]).collidepoint(event.pos):

                if event.button == 4:

                    Money += x

                if event.button == 5:

                    if Money - x >= 100:

                        Money -= x

                    else:

                        Money = 100

                Text[1] = str(Money) + ' $'

            if pg.Rect(Box[2]).collidepoint(event.pos):

                if event.button == 4:

                    if SBlind + x <= BBlind / 2:

                        SBlind += x

                    else:

                        SBlind = int(BBlind / 2)

                if event.button == 5:

                    if SBlind - x >= 1:

                        SBlind -= x

                    else:

                        SBlind = 1

                Text[2] = 'Small Blind = ' + str(SBlind)

            if pg.Rect(Box[3]).collidepoint(event.pos):

                if event.button == 4:

                    if BBlind + x <= Money / 5:

                        BBlind += x

                    else:

                        BBlind = int(Money / 5)

                if event.button == 5:

                    if BBlind - x >= SBlind * 2:

                        BBlind -= x

                    else:

                        BBlind = SBlind * 2

                Text[3] = 'Big Blind = ' + str(BBlind)

            if pg.Rect(Box[4]).collidepoint(event.pos):

                if event.button == 4:

                    if Players + x + Bots <= 23:

                        Players += x

                    else:

                        Players = 23 - Bots

                if event.button == 5:

                    if Players + Bots - x >= 3 and Players - x > 0:

                        Players -= x

                    elif Bots > 3:

                        Players = 0

                    else:

                        Players = 3 - Bots

                Text[4] = str(Players) + ' Player'

            if pg.Rect(Box[5]).collidepoint(event.pos):

                if event.button == 4:

                    if Players + x + Bots <= 23:

                        Bots += x

                    else:

                        Bots = 23 - Players

                if event.button == 5:

                    if Bots + Players - x >= 3 and Bots - x > 0:

                        Bots -= x

                    elif Players > 3:

                        Bots = 0

                    else:

                        Bots = 3 - Players

                Text[5] = str(Bots) + ' Bots'

            if pg.Rect(Box[6]).collidepoint(event.pos) and event.button == 1:

                run = False

        if event.type == pg.KEYDOWN:

            if event.key == pg.K_RETURN:

                Game(Players, Bots, [0, SBlind], [1, BBlind], Money)

    for _ in range(len(Box)):

        if pg.Rect(Box[_]).collidepoint(pg.mouse.get_pos()):

            if Box[_][3] < 3 * h / 13:

                Box[_][0] -= 1

                Box[_][1] -= 0.5

                Box[_][2] += 2

                Box[_][3] += 1

                Inf[_] -= 0.5

        elif Box[_][3] > 2 * h / 13:

            Box[_][0] += 1

            Box[_][1] += 0.5

            Box[_][2] -= 2

            Box[_][3] -= 1

            Inf[_] += 0.5