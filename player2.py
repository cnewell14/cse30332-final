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
        pass
        '''if self.rect.colliderect(self.player1.rect):
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
            if self.player2.score >= 5:
                self.gs.waitingWords = "PLAYER 2 WINS\n GAME OVER"
                self.gs.waitingLabel = self.gs.myfont.render(self.gs.waitingWords,1,(0,0,0))
                #reactor.stop()
            return'''

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
        self.connected = 0

    def dataReceived(self,data):
        if data.split("|")[0] == "Go!":
            self.connected == 1
            self.GS.players_connected = 1

        elif self.connected == 1:
            main_data = data.split("|")
            link_data = main_data[0]
            link = link_data.split(" ")
            self.GS.link.rect.centerx = int(link[0])
            self.GS.link.rect.centery = int(link[1])
            self.GS.rupee1.rect.center = (int(link[2]), int(link[3]))
            self.GS.rupee2.rect.center = (int(link[4]), int(link[5]))
            self.GS.link.score = int(link[6])
            self.GS.kirby.score = int(link[7])

    def connectionMade(self):
        print("Connection Made")

    def forwardData(self,data):
        if self.connected == 1:
            self.GS.waitingWords = ""
            self.GS.waitingLabel = self.GS.myfont.render(self.GS.waitingWords,1,(0,0,0))
        self.transport.write(data)

class GameSpace:
    def __init__(self):
        #Game and Graphics
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
            kirby_pos = str(self.kirby.rect.centerx) + " " + str(self.kirby.rect.centery)
            #rupee1_pos = str(self.rupee1.rect.centerx) + " " + str(self.rupee1.rect.centery)
            #rupee2_pos = str(self.rupee2.rect.centerx) + " " + str(self.rupee2.rect.centery)
            #score_player2 = str(self.kirby.score)
            data = kirby_pos#" " + rupee1_pos + " " + rupee2_pos + " " + score_player2 + "|"
            self.forwardData(data)

            time_counter = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    reactor.stop()
                    while_loop = 0
                    break

            self.screen.fill(self.black)
            self.screen.blit(self.bg.image, self.bg.rect)
            self.screen.blit(self.waitingLabel, (100, 230))
           
            if self.players_connected == 1:
                self.kirby.move()

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
                #self.screen.blit(self.waitingLabel, (100, 230))

                pygame.display.flip()

    def forwardData(self, data):
        pass

if __name__ == "__main__":
    gs = GameSpace()
    loop = LoopingCall(gs.gameplay)
    loop.start(1/60)
    reactor.connectTCP("newt.campus.nd.edu", 40080, DataConnectionFactory(gs))
    reactor.run()
    loop.stop()
