import pygame as pg

import math as m

import time as t

import random as rand

from Server.Client import Client as c

from copy import *

from Karten import Cards

def Int(x):

    for _ in range(len(x)):

        x[_] = int(x[_])

    return x

def Chips(Money, Points, Chip, Angle):

    if Money > 250:

        for _ in range(int(Money / 250) - 1):

            dx, dy = Chip[3].get_width(), Chip[3].get_height()

            win.blit(Chip[3], (Points[0][0] + _ * m.sin(Angle) * m.ceil(dx / 25) - dx / 2,
                               Points[0][1] + _ * m.cos(Angle) * m.ceil(dx / 25) - dy / 2))

        Money = Money % 250 + 250

    if Money > 50:

        for _ in range(int(Money / 50) - 1):

            dx, dy = Chip[2].get_width(), Chip[2].get_height()

            win.blit(Chip[2], (Points[1][0] + _ * m.sin(Angle) * m.ceil(dx / 25) - dx / 2,
                               Points[1][1] + _ * m.cos(Angle) * m.ceil(dx / 25) - dy / 2))

        Money = Money % 50 + 50

    if Money > 10:

        for _ in range(int(Money / 10) - 1):

            dx, dy = Chip[1].get_width(), Chip[1].get_height()

            win.blit(Chip[1], (Points[2][0] + _ * m.sin(Angle) * m.ceil(dx / 25) - dx / 2,
                               Points[2][1] + _ * m.cos(Angle) * m.ceil(dx / 25) - dy / 2))

        Money = Money % 10 + 10

    if Money >= 2:

        for _ in range(int(Money / 2)):

            dx, dy = Chip[0].get_width(), Chip[0].get_height()

            win.blit(Chip[0], (Points[3][0] + _ * m.sin(Angle) * m.ceil(dx / 25) - dx / 2,
                               Points[3][1] + _ * m.cos(Angle) * m.ceil(dx / 25) - dy / 2))

def WIW(Anzahl):
    #WoIstWer?
    Position = [[[w/2, h/2]],
                [[w/2, h-55]],
                [[w/2, h-55], [w/2, 55]],
                [[w/2, h-55], [55, h/2], [w-55, h/2]],
                [[w/2, h-55], [55, h/2], [w/2, 55], [w-55, h/2]],
                [[w/2, h-55], [h/2+m.sin(-m.pi/4)*(h/2-55), h/2+m.cos(-m.pi/4)*(h/2-55)], [h/2+55, 55], [w-h/2-55, 55], [w-h/2+m.sin(m.pi/4)*(h/2-55), h/2+m.cos(m.pi/4)*(h/2-55)]],
                [[w/2, h-55], [h/2+m.sin(-m.pi/4)*(h/2-55), h/2+m.cos(-m.pi/4)*(h/2-55)], [h/2+m.sin(5*m.pi/4)*(h/2-55), h/2+m.cos(5*m.pi/4)*(h/2-55)], [w/2, 55], [w-h/2+m.sin(3*m.pi/4)*(h/2-55), h/2+m.cos(3*m.pi/4)*(h/2-55)], [w-h/2+m.sin(m.pi/4)*(h/2-55), h/2+m.cos(m.pi/4)*(h/2-55)]],
                [[w/2, h-55], [h/2+m.sin(-m.pi/4)*(h/2-55), h/2+m.cos(-m.pi/4)*(h/2-55)], [h/2+m.sin(5*m.pi/4)*(h/2-55), h/2+m.cos(5*m.pi/4)*(h/2-55)], [h/2+55, 55], [w-h/2-55, 55], [w-h/2+m.sin(3*m.pi/4)*(h/2-55), h/2+m.cos(3*m.pi/4)*(h/2-55)], [w-h/2+m.sin(m.pi/4)*(h/2-55), h/2+m.cos(m.pi/4)*(h/2-55)]],
                [[h/2+55, h-55], [h/2+m.sin(-m.pi/4)*(h/2-55), h/2+m.cos(-m.pi/4)*(h/2-55)], [h/2+m.sin(5*m.pi/4)*(h/2-55), h/2+m.cos(5*m.pi/4)*(h/2-55)], [h/2+55, 55], [w-h/2-55, 55], [w-h/2+m.sin(3*m.pi/4)*(h/2-55), h/2+m.cos(3*m.pi/4)*(h/2-55)], [w-h/2+m.sin(m.pi/4)*(h/2-55), h/2+m.cos(m.pi/4)*(h/2-55)], [w-h/2-55, h-55]]]

    Winkel = [[180],
              [180],
              [180, 0],
              [180, 90, 270],
              [180, 90, 0, 270],
              [180, 135, 0, 0, 225],
              [180, 135, 45, 0, 315, 225],
              [180, 135, 45, 0, 0, 315, 225],
              [180, 135, 45, 0, 0, 315, 225, 180]]

    return Position[Anzahl], Winkel[Anzahl]

def KartenAusteilen(Cards, HMP, Mitte, Karten):

    stapel = list(range(52))

    for _ in range(HMP):

        for __ in range(2):

            stapel.remove(Cards[_][__])

            Karten[Cards[_][__]].rotStapel(WIW(HMP)[0][_], __+1.5, 2, 10, WIW(HMP)[1][_])

    for _ in range(5):

        stapel.remove(Mitte[_])

        Karten[Mitte[_]].Stapel(WIW(0)[0][0], _+4, 5, 65)

    for _ in range(len(stapel)): Karten[stapel[_]].Stapel(WIW(0)[0][0], _-64, len(stapel), 2)

    return Mitte, Karten

def Pay(From, To, Much):

    From -= Much

    To += Much

    return From, To

def Winner(P, SBlind, BBlind, Players, B, M):

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

                    SBlind[0] = 0

                    BBlind[0] = 1

                    Game(Players, B, SBlind, BBlind, M)

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

def Showdown(K, M, Player, Mitte, I):

    I = [I, []]

    for _ in I[0]:

        I[1].append(0)

        x = sorted(M + Player[_][2])

        y = []

        for __ in x: y.append(int(__ / 13))

        z = []
#Straight(-Flush)
        for __ in range(6, -1, -1):

            if K[x[__]].number - 1 == K[x[__ - 1]].number:

                z.append(__)

            else:

                z = []

            if len(z) == 5:

                I[1][I[0].index(_)] = 400 + K[x[z[0]]].number

                for ___ in range(5): z[___] = y[z[___]]

                if z.count(0) == 5 or z.count(1) == 5 or z.count(2) == 5 or z.count(3) == 5:

                    I[1][I[0].index(_)] += 400

        z = []
#Flush
        for __ in range(4):

            if y.count(__) >= 5 and I[1][I[0].index(_)] < 500:

                I[1][I[0].index(_)] = 500

                for ___ in x:

                    if K[___].color == __:

                        z.append(___)

                for ___ in range(len(z)):

                    I[1][I[0].index(_)] += 0.5 * K[z[___]].number / (10 ** (len(z) - ___))

        for __ in range(7): y[__] = x[__] % 13

        y.sort()
#Quads
        for __ in range(4):

            if y.count(y[__]) >= 4 and I[1][I[0].index(_)] < 800:

                I[1][I[0].index(_)] = 700 + y[__]

                break
#Trips(Full House)
        for __ in range(6, 1, -1):

            if y.count(y[__]) == 3:

                for ___ in range(5, -1, -1):

                    if y.count(y[__]) >= 2 and y[__] != y[___] and I[1][I[0].index(_)] < 600:

                        I[1][I[0].index(_)] = 600 + y[__] + y[___] / 20

                if I[1][I[0].index(_)] < 300:

                    I[1][I[0].index(_)] = 300 + y[__]

                    a = y[__]

                    y.remove(a)

                    for ___ in range(6):

                        I[1][I[0].index(_)] += 0.5 * y[___] / (10 ** (6 - ___))

                    y.append(a)

                    y.sort()
#(2) Pair
        for __ in range(6, 0, -1):

            if y.count(y[__]) == 2:

                for ___ in range(6, 0, -1):

                    if y.count(y[___]) == 2 and y[__] != y[___] and I[1][I[0].index(_)] < 200:

                        I[1][I[0].index(_)] = 200 + y[__] + y[___] / 100

                        a = [y[__], y[___]]

                        for ____ in range(2): y.remove(a[0])

                        for ____ in range(2): y.remove(a[1])

                        for ___ in range(3):

                            I[1][I[0].index(_)] += 0.5 * y[___] / (10 ** (3 - ___))

                        for ____ in range(2): y.append(a[0])

                        for ____ in range(2): y.append(a[1])

                        y.sort()

                        break

                if I[1][I[0].index(_)] < 100:

                    I[1][I[0].index(_)] = 100 + y[__]

                    a = y[__]

                    for ___ in range(2): y.remove(a)

                    for ___ in range(5): I[1][I[0].index(_)] += 0.5 * y[___] / (10 ** (5 - ___))

                    for ___ in range(2): y.append(a)

                    y.sort()
#High Card
        if not I[1][I[0].index(_)]:

            I[1][I[0].index(_)] = y[6]

            for __ in range(6):

                I[1][I[0].index(_)] += 0.5 * y[__] / (10 ** (6 - __))

#Who Wins?
    for _ in range(len(I[0])):

        if I[1][0] < max(I[1]):

            del I[0][0]

            del I[1][0]

        else:

            I[0].append(I[0][0])

            I[1].append(I[1][0])

            del I[0][0]

            del I[1][0]

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

def Reset(Mitte, Player, Karten, a, SBlind, BBlind):

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

    SBlind[0] = (SBlind[0] + 1) % len(Player)

    BBlind[0] = (BBlind[0] + 1) % len(Player)

    Turn = (BBlind[0] + 1) % len(Player)

    Player, Mitte, stapel, Karten = KartenAusteilen(Player, Mitte, stapel, Karten, SBlind, BBlind)

    Raise = BBlind[1]

    return Player, Karten, Mitte, stapel, SBlind, BBlind, Turn, Raise, Ingame, AllIn

def Test(Ingame, AllIn, Player, Mitte, Karten, SBlind, BBlind, stapel, Chip, SChip, BP, SBP, Turn, run, M):
#Nur noch ein Spieler übrig
    if len(Ingame) + len(AllIn) == 1:

        Ingame = Ingame + AllIn

        Player, Karten, Mitte, stapel, SBlind, BBlind, Turn, Raise, Ingame, AllIn = Reset(Mitte, Player, Karten, Ingame, SBlind, BBlind)
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

        Player, Karten, Mitte, stapel, SBlind, BBlind, Turn, Raise, Ingame, AllIn = Reset(Mitte, Player, Karten, a, SBlind, BBlind)

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

        SBlind[0] = SBlind[0] % len(Player)

        BBlind[0] = BBlind[0] % len(Player)

        Turn = (BBlind[0] + 1) % len(Player)

        Player, Mitte, stapel, Karten = KartenAusteilen(Player, Mitte, stapel, Karten, SBlind, BBlind)

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

        run = Winner(Player[0], SBlind, BBlind, *M)

    return Ingame, AllIn, Player, Mitte, Karten, SBlind, BBlind, Chip, SChip, stapel, BP, SBP, Turn, run

def Enter(Karten, Player, Turn, Ingame, Mitte, Raise, run, stapel, SBlind, BBlind, Chip, SChip, BP, SBP, AllIn, M):

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
#Fold
    elif Raise < max(Mitte[1]):

        Ingame.remove(a)
#Check & Call
    elif Raise == Mitte[1][a]:

        if run != len(Ingame):

            run += 1

            Raise = max(Mitte[1])

            return Karten, Player, Turn, Ingame, Mitte, Raise, run, stapel, SBlind, BBlind, Chip, SChip, BP, SBP, AllIn
#Raise
    else:

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

                Player, Karten, Mitte, stapel, SBlind, BBlind, Turn, Raise, Ingame, AllIn = Reset(Mitte, Player, Karten, a, SBlind, BBlind)

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

    Ingame, AllIn, Player, Mitte, Karten, SBlind, BBlind, Chip, SChip, stapel, BP, SBP, Turn, run = Test(Ingame, AllIn, Player, Mitte, Karten, SBlind, BBlind, stapel, Chip, SChip, BP, SBP, Turn, run, M)

    return Karten, Player, Turn, Ingame, Mitte, Raise, run, stapel, SBlind, BBlind, Chip, SChip, BP, SBP, AllIn

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

def Pause(P, B, SBlind, BBlind, M):

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

                    Game(P, B, SBlind, BBlind, M)

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

def Game(HMP, SBlind, MPP):     #HowManyPlayers     MonyPerPerson

    client = Client.Client(Name, ('127.0.0.1', 62435))
    Input = client.getServerPool()      #Mitte, Karten, Startguthaben
    s = list(range(52))

    rand.shuffle(s)

    Input = {"Mitte": [s[0], s[1], s[2], s[3], s[4]], "Karten": [], "Startguthaben": MPP}

    for _ in range(5): del s[0]

    for _ in range(HMP):

        Input["Karten"].append([s[0], s[1]])

        for __ in range(2): del s[0]

    #HMP = len(Input["Karten"])

    Karten = ['karo-2', 'karo-3', 'karo-4', 'karo-5', 'karo-6', 'karo-7', 'karo-8', 'karo-9', 'karo-10', 'karo-bube', 'karo-dame', 'karo-koenig', 'karo-ass',
              'herz-2', 'herz-3', 'herz-4', 'herz-5', 'herz-6', 'herz-7', 'herz-8', 'herz-9', 'herz-10', 'herz-bube', 'herz-dame', 'herz-koenig', 'herz-ass',
              'pik-2', 'pik-3', 'pik-4', 'pik-5', 'pik-6', 'pik-7', 'pik-8', 'pik-9', 'pik-10', 'pik-bube', 'pik-dame', 'pik-koenig', 'pik-ass',
              'kreuz-2', 'kreuz-3', 'kreuz-4', 'kreuz-5', 'kreuz-6', 'kreuz-7', 'kreuz-8', 'kreuz-9', 'kreuz-10', 'kreuz-bube', 'kreuz-dame', 'kreuz-koenig', 'kreuz-ass']

    for _ in range(len(Karten)):

        Karten[_] = Cards(Karten[_], int(w/22.8), int(h/8.5))        #126 179

    You = {"Name": "Name", "Cards": Input["Karten"][0], "Chips": Input["Startguthaben"]}

    Mitte = Input["Mitte"]

    Pot = []

    Money = []

    for _ in range(HMP): Money.append(Input["Startguthaben"])

    Ingame = []

    for _ in range(HMP):

        Pot.append(0)

        Ingame.append(_)

    Chip = [pg.transform.scale(pg.image.load('Chips/2.png').convert_alpha(), (50, 50)),
            pg.transform.scale(pg.image.load('Chips/10.png').convert_alpha(), (50, 50)),
            pg.transform.scale(pg.image.load('Chips/50.png').convert_alpha(), (50, 50)),
            pg.transform.scale(pg.image.load('Chips/250.png').convert_alpha(), (50, 50))]

    Mitte, Karten = KartenAusteilen(Input["Karten"], HMP, Mitte, Karten)

    BP = []

    for a in [1,4/3]:

        for _ in range(HMP):

            BP.append([WIW(HMP)[0][_][0] + m.sin(m.radians(WIW(HMP)[1][_])) * 90 * a,
                       WIW(HMP)[0][_][1] + m.cos(m.radians(WIW(HMP)[1][_])) * 90 * a])

            for __ in range(4):

                BP[-1].append([BP[-1][0] - (1.5 - __) * m.sin(m.radians(WIW(HMP)[1][_]) + m.pi / 2) * Chip[0].get_width(),
                              BP[-1][1] - (1.5 - __) * m.cos(m.radians(WIW(HMP)[1][_]) + m.pi / 2) * Chip[0].get_width()])

            for __ in range(2): del BP[-1][0]

    font = pg.font.Font(None, 50)

    run = 1

    win.fill((100, 100, 100))

    pg.draw.circle(win, (0, 90, 20), (h / 2, h / 2), h / 2)

    pg.draw.circle(win, (0, 90, 20), (w - h / 2, h / 2), h / 2)

    pg.draw.circle(win, (0, 0, 0), (h / 2, h / 2), h / 2, 10)

    pg.draw.circle(win, (0, 0, 0), (w - h / 2, h / 2), h / 2, 10)

    pg.draw.rect(win, (0, 90, 20), (h / 2, 0, w - h, h))

    pg.draw.line(win, (0, 0, 0), (h / 2, 4), (w - h / 2, 4), 10)

    pg.draw.line(win, (0, 0, 0), (h / 2, h - 5), (w - h / 2, h - 5), 10)

    while run:

        for _ in Karten:

            _.Draw(win)

        for _ in range(HMP):

            Chips(Pot[_], BP[_], Chip, m.radians(WIW(HMP)[1][_]))

            Chips(Money[_], BP[_+HMP], Chip, m.radians(WIW(HMP)[1][_]))

        pg.display.flip()

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if pg.Rect(WIW(2)[0][0][0]-int(w/22.8)-10, WIW(2)[0][0][1]-int(h/8.5)-5, int(w/11.4)+20, int(h/4.25)+10).collidepoint(event.pos):

                        Karten[You["Cards"][0]].open = not Karten[You["Cards"][0]].open

                        Karten[You["Cards"][1]].open = not Karten[You["Cards"][1]].open

                if event.button == 4:

                    if Mitte[0] < max(Mitte):

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

                if event.button == 3: Enter()

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:

                    run = Pause()

                if event.key == pg.K_SPACE:

                    Karten[You["Cards"][0]].open = not Karten[You["Cards"][0]].open

                    Karten[You["Cards"][1]].open = not Karten[You["Cards"][1]].open

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

                if event.key == pg.K_RETURN: Enter()

                if event.key == pg.K_BACKSPACE: Ingame.remove(You["Name"])

def GameStats():

    Players = 3

    SBlind = 10

    Money = 100

    Text = ['Start', '100 $', 'Small Blind = 10', '3 Players', 'Quit']

    Box = [[w / 8, h / 13, 5 * w / 16, 2 * h / 13], [9 * w / 16, h / 13, 5 * w / 16, 2 * h / 13],
           [w / 8, 4 * h / 13, 3 * w / 4, 2 * h / 13], [w / 8, 7 * h / 13, 3 * w / 4, 2 * h / 13],
           [w / 8, 10 * h / 13, 3 * w / 4, 2 * h / 13]]

    run = True

    while run:

        win.fill((0, 90, 20))

        for _ in range(5):
            pg.draw.rect(win, (0, 135, 30), Box[_], 2)

            pg.draw.rect(win, (150, 150, 150), Box[_])

            dx, dy = pg.font.Font(None, int(Box[_][3] / 2)).size(Text[_])

            win.blit(pg.font.Font(None, int(Box[_][3] / 2)).render(Text[_], False, (0, 90, 20)),
                     (Box[_][0] + (Box[_][2] - dx) / 2, Box[_][1] + (Box[_][3] - dy) / 2))

        pg.display.flip()

        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if pg.Rect(Box[0]).collidepoint(event.pos):
                        Game(Players, SBlind, Money)

                    if pg.Rect(Box[4]).collidepoint(event.pos):
                        run = False

                        break

                x = 1

                if pg.mouse.get_pressed()[1]:
                    x = 10

                if event.button == 4:

                    if pg.Rect(Box[1]).collidepoint(event.pos): Money += x

                    if pg.Rect(Box[2]).collidepoint(event.pos):

                        if SBlind + x <= Money / 10:

                            SBlind += x

                        else:

                            SBlind = int(Money / 10)

                    if pg.Rect(Box[3]).collidepoint(event.pos):

                        if Players + x <= 8:

                            Players += x

                        else:

                            Players = 8

                if event.button == 5:

                    if pg.Rect(Box[1]).collidepoint(event.pos):

                        if Money - x >= 100:

                            Money -= x

                        else:

                            Money = 100

                    if pg.Rect(Box[2]).collidepoint(event.pos):

                        if SBlind - x >= 1:

                            SBlind -= x

                        else:

                            SBlind = 1

                    if pg.Rect(Box[3]).collidepoint(event.pos):

                        if Players - x >= 3:

                            Players -= x

                        else:

                            Players = 3

                Text[1] = str(Money) + ' $'

                Text[2] = 'Small Blind = ' + str(SBlind)

                Text[3] = str(Players) + ' Players'

        for _ in range(len(Box)):

            if pg.Rect(Box[_]).collidepoint(pg.mouse.get_pos()):

                if Box[_][3] < 3 * h / 13:
                    Box[_][0] -= 1

                    Box[_][1] -= 0.5

                    Box[_][2] += 2

                    Box[_][3] += 1

            elif Box[_][3] > 2 * h / 13:

                Box[_][0] += 1

                Box[_][1] += 0.5

                Box[_][2] -= 2

                Box[_][3] -= 1

def FindLobby(Name):

    client = c(Name, ('192.168.0.9', 62435))

    Ping = client.first_connection()

    Lobbys = client.get_lobby_list()

    Text = ['+', *Lobbys]
    print(Text)
    Box = []

    for _ in range(len(Text)): Box.append([w/8, h/13+_*3*h/13, 3*w/4, h/6])

    run = True

    while run:

        win.fill((0, 90, 20))

        for _ in range(len(Box)):

            pg.draw.rect(win, (150, 150, 150), Box[_], 2)

            dx, dy = pg.font.Font(None, int(Box[_][3] / 2)).size(Text[_])

            win.blit(pg.font.Font(None, int(Box[_][3] / 2)).render(Text[_], False, (0, 90, 20)), (Box[_][0] + (Box[_][2] - dx) / 2, Box[_][1] + (Box[_][3] - dy) / 2))

        pg.display.flip()

        for event in pg.event.get():

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:

                    run = False

                    break

pg.init()

win = pg.display.set_mode((0, 0), pg.FULLSCREEN)

w, h = win.get_size()

run = True

while run:

    Name = 'Bitte Namen Eingeben'

    run = True

    while run:

        win.fill((0, 90, 20))

        dx, dy = pg.font.Font(None, 100).size(Name)

        win.blit(pg.font.Font(None, 100).render(Name, False, (150, 150, 150)), ((w-dx)/2, (h-dy)/2))

        pg.display.flip()

        for event in pg.event.get():

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:

                    run = False

                    break

                elif event.key == pg.K_RETURN:

                    if Name != 'Bitte Namen Eingeben': FindLobby(Name)

                elif event.key == pg.K_BACKSPACE:

                    if Name != 'Bitte Namen Eingeben':Name = Name[:-1]

                    if Name == '': Name = 'Bitte Namen Eingeben'

                else:

                    if Name == 'Bitte Namen Eingeben': Name = ''

                    Name += event.unicode

                    #Markins befehl gegen Sonderzeichen