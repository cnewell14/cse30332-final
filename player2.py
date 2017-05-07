#!/usr/bin/env python2.7

import pygame
import math
import random
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.python import log
import sys
import json

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
    def __init__(self,Gs, Player):
        self.image = pygame.image.load("graphics/rupee.png")
        self.image = pygame.transform.scale(self.image, (32, 24))
        self.rect = self.image.get_rect()
        self.player = Player
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
        if self.rect.colliderect(self.player.rect):
            self.rupee_pos()
            self.player.score += 1
            self.gs.Words = "SCORE     PLAYER1: " + str(0) + "     PLAYER2: " + str(self.player.score)
            self.gs.label = self.gs.myfont.render(self.gs.Words,1,(0,0,0))

    def tick(self):
        self.found()

class DataConnectionFactory(ClientFactory):
    def __init__(self, GS):
        self.GS = GS

    def buildProtocol(self,addr):
        myconn = Data(self.GS)
        self.GS.forwardData = myconn.forwardData
        return myconn

class Data(Protocol):
    def __init__(self, GS):
        self.GS = GS
        self.queue = []

    def dataReceived(self,data):
        #print (data)
        pass

    def connectionMade(self):
        print("Connection Made")

    def forwardData(self,data):
        self.transport.write(data)

class GameSpace:
    def __init__(self):
        #Game and Graphics
        pygame.init()
        log.startLogging(sys.stdout)
        self.myfont = pygame.font.SysFont(None, 30)
        self.myfont.set_bold(True)
        self.Words = "SCORE     PLAYER1: 0     PLAYER2: 0"
        self.label = self.myfont.render(self.Words,1,(0,0,0))
        self.size = self.width,self.height = 640,480
        self.black = 0,0,0
        self.screen = pygame.display.set_mode(self.size)

        #image classes
        self.bg = Background()
        
        self.link = Player("graphics/link.png")
        self.link.rect.centerx = 320
        self.link.rect.centery = 420

        self.kirby = Player("graphics/kirby.png")
        self.kirby.rect.centerx = 320
        self.kirby.rect.centery = 60

        self.rupee1 = Rupee(self, self.link)
        self.rupee2 = Rupee(self, self.link)

        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1,1)

    def gameplay(self):
            #link_pos = "linkx " + str(self.link.rect.centerx) + " linky " + str(self.link.rect.centery)
            kirby_pos = "kirbyx " + str(self.kirby.rect.centerx) + " kirbyy " + str(self.kirby.rect.centery) + "|"
            #data = link_pos + kirby_pos
            self.forwardData(kirby_pos)
            time_counter = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    reactor.stop()
                    while_loop = 0
                    break
            
            self.kirby.move()

            self.rupee1.tick()
            self.rupee2.tick()

            self.screen.fill(self.black)
            self.screen.blit(self.bg.image, self.bg.rect)
            self.screen.blit(self.rupee1.image, self.rupee1.rect)
            self.screen.blit(self.rupee2.image, self.rupee2.rect)
            self.screen.blit(self.link.image, self.link.rect)
            self.screen.blit(self.kirby.image, self.kirby.rect)
            self.screen.blit(self.label, (0,0))

            pygame.display.flip()

    def forwardData(self, data):
        pass

if __name__ == "__main__":
    gs = GameSpace()
    loop = LoopingCall(gs.gameplay)
    loop.start(1/60)
    reactor.connectTCP("ash.campus.nd.edu", 40080, DataConnectionFactory(gs))
    reactor.run()
    loop.stop()
