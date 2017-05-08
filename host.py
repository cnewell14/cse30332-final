#!/usr/bin/env python2.7

import pygame
import math
import random
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.python import log
import sys
import json
import time

class Background:
    def __init__(self):
        self.image = pygame.image.load("graphics/background.png")
        self.rect = self.image.get_rect()

class Player:
    def __init__(self, image_file):
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (64,48 ))
        self.rect = self.image.get_rect()
        self.score = 0

    def move(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.rect.centerx += 10
        elif key[pygame.K_LEFT]:
            self.rect.centerx -= 10
        elif key[pygame.K_UP]:
            self.rect.centery -= 10
        elif key[pygame.K_DOWN]:
            self.rect.centery += 10


class Rupee:
    def __init__(self,Gs, Player1, Player2):
        self.image = pygame.image.load("graphics/rupee.png")
        self.image = pygame.transform.scale(self.image, (32, 24))
        self.rect = self.image.get_rect()
        self.player1 = Player1
        self.player2 = Player2
        self.gs = Gs
        self.rupee_pos()

    def rupee_pos(self):
        pos = random.random()

        x = int(pos * 585) + 35
        pos = random.random()
        y = int(pos * 450) + 30

        self.rect.centerx = x
        self.rect.centery = y

    def found(self):
        if self.rect.colliderect(self.player1.rect):
            self.rupee_pos()
            self.player1.score += 1
            self.gs.Words = "SCORE     PLAYER1: " + str(self.player1.score) + "     PLAYER2: " + str(self.player2.score)
            self.gs.label = self.gs.myfont.render(self.gs.Words,1,(0,0,0))
            return

        elif self.rect.colliderect(self.player2.rect):
            self.rupee_pos()
            self.player2.score += 1
            self.gs.Words = "SCORE     PLAYER1: " + str(self.player1.score) + "     PLAYER2: " + str(self.player2.score)
            self.gs.label = self.gs.myfont.render(self.gs.Words,1,(0,0,0))
            return
        
    def tick(self):
        self.found()

class DataConnectionFactory(Factory):
    def __init__(self, GS):
        self.GS = GS

    def buildProtocol(self,addr):
        myconn = Data(self.GS)
        self.GS.forwardData = myconn.forwardData
        return myconn


class Data(Protocol):
    def __init__(self, GS):
        self.GS = GS
        self.connected = 0
        self.queue = []

    def connectionMade(self):
        print ("Connection Made")
        self.connected = 1
        self.GS.players_connected = 1
        self.GS.waitingWords = ""
        self.GS.waitingLabel = self.GS.myfont.render(self.GS.waitingWords,1,(0,0,0))
        self.transport.write("Go!|")

    def dataReceived(self, data):
        main_data = data.split("|")
        kirby_data = main_data[0]
        kirby = kirby_data.split(" ")
        self.GS.kirby.rect.centerx = int(kirby[0])
        self.GS.kirby.rect.centery = int(kirby[1])
        self.GS.rupee1.rect.centerx = int(kirby[2])
        self.GS.rupee1.rect.centery = int(kirby[3])
        self.GS.rupee2.rect.centerx = int(kirby[4])
        self.GS.rupee2.rect.centery = int(kirby[5])
        self.GS.kirby.score = int(kirby[6])

    def forwardData(self, data):
        if self.connected == 1:
            self.transport.write(data)


class GameSpace:
    #Game and Graphics
    def __init__(self):
        pygame.init()
        log.startLogging(sys.stdout)
        self.myfont = pygame.font.SysFont(None, 30)
        self.myfont.set_bold(True)
        self.Words = "SCORE     PLAYER1: 0     PLAYER2: 0"
        self.waitingWords = "WAITING FOR CONNECTION!"
        self.label = self.myfont.render(self.Words,1,(0,0,0))
        self.waitingLabel = self.myfont.render(self.waitingWords,1,(0,0,0))
        self.size = self.width,self.height = 640,480
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)
        self.players_connected = 0

        #image classes
        self.bg = Background()
        
        self.link = Player("graphics/link.png")
        self.link.rect.centerx = 320
        self.link.rect.centery = 420

        self.kirby = Player("graphics/kirby.png")
        self.kirby.rect.centerx = 320
        self.kirby.rect.centery = 60

        self.rupee1 = Rupee(self, self.link, self.kirby)
        self.rupee2 = Rupee(self, self.link, self.kirby)

        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1,1)

    def gameplay(self):
        
        link_pos = str(self.link.rect.centerx) + " " + str(self.link.rect.centery)
        rupee1_pos = str(self.rupee1.rect.centerx) + " " + str(self.rupee1.rect.centery)
        rupee2_pos = str(self.rupee2.rect.centerx) + " " + str(self.rupee2.rect.centery)
        score_player1 = str(self.link.score)
        data = link_pos + " " + rupee1_pos + " " + rupee2_pos + " " + score_player1 + "|"
        self.forwardData(data)

        time_counter = self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()
                break

        self.screen.fill(self.black)
        self.screen.blit(self.bg.image, self.bg.rect)
        self.screen.blit(self.waitingLabel, (100, 230))
        
        if self.players_connected == 1:
            self.link.move()

            self.rupee1.tick()
            self.rupee2.tick()

            #self.screen.fill(self.black)
            #self.screen.blit(self.bg.image, self.bg.rect)
            self.screen.blit(self.rupee1.image, self.rupee1.rect)
            self.screen.blit(self.rupee2.image, self.rupee2.rect)
            self.screen.blit(self.link.image, self.link.rect)
            self.screen.blit(self.kirby.image, self.kirby.rect)
        
            self.Words = "SCORE     PLAYER1: " + str(self.link.score) + "     PLAYER2: " + str(self.kirby.score)
            self.label = self.myfont.render(self.Words,1,(0,0,0))
            self.screen.blit(self.label, (0,0))
            #self.screen.blit(self.waitingLabel, (100,230))

            pygame.display.flip()

    def forwardData(self, data):
        pass

if __name__ == "__main__":
    gs = GameSpace()
    loop = LoopingCall(gs.gameplay)
    loop.start(1/60)
    reactor.listenTCP(40080, DataConnectionFactory(gs))
    reactor.run()
    loop.stop()
