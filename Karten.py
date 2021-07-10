import pygame as pg

import random as rand

import math as m

class Cards:

    def __init__(self, Card, W, H):

        self.open = 0

        if Card[1] == "a":

            self.color = 0

        if Card[1] == "e":

            self.color = 1

        if Card[1] == "i":

            self.color = 2

        if Card[1] == "r":

            self.color = 3

        self.number = Card[len(Card) - 2:len(Card)]

        if self.number[1] == '0':

            self.number = 10

        elif self.number[0] == 'b':

            self.number = 11

        elif self.number[0] == 'm':

            self.number = 12

        elif self.number[0] == 'i':

            self.number = 13

        elif self.number[0] == 's':

            self.number = 14

        else:

            self.number = int(self.number[1])

        self.front = pg.transform.scale(pg.image.load('Alle Karten/'+str(Card)+'.png').convert_alpha(), (W, H))

        self.back = pg.transform.scale(pg.image.load('Alle Karten/Rückseite.png').convert_alpha(), (W, H))

        self.width, self.dx = W, W

        self.height, self.dy = H, H

        self.pos = [0, 0]

        self.angle = 0

    def Draw(self, win):

        if self.open:

            win.blit(pg.transform.rotate(self.front, self.angle), (self.pos[0] - self.dx / 2, self.pos[1] - self.dy / 2))

        else:

            win.blit(pg.transform.rotate(self.back, self.angle), (self.pos[0] - self.dx / 2, self.pos[1] - self.dy / 2))

    def Hand(self, Count, pos, Point, Angle):

        self.angle = 11.25 - 22.5 * pos / Count + Angle

        self.dx, self.dy = pg.transform.rotate(self.front, self.angle).get_size()

        self.pos = [Point[0] + m.sin(m.radians(self.angle)) * self.height, Point[1] + m.cos(m.radians(self.angle)) * self.height]

    def Stapel(self, Point, pos, Count):

        self.pos = [Point[0] + pos - Count, Point[1]]

        self.dx, self.dy = self.width, self.height

        self.angle = 0

    def Scale(self, W, H):

        self.front = pg.transform.scale(self.front, (W, H))

        self.back = pg.transform.scale(self.back, (W, H))

        self.width = W

        self.dx = W

        self.height = H

        self.dy = H