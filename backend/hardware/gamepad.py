#-*- coding: utf-8 -*-

import time
import pygame
import threading
import logging
from pygame.locals import *


#
# cKeycombo Class
#
#Used to manage keycombos, its merely a structure
#

class cKeycombo(object):
    def __init__(self, id, keys, pressed = False):
        self.id = id
        self.keys = keys
        self.pressed = pressed


#
# cGamepad Class
#
#Used to store information like slot, keymapping etc
#passes button presses into the queue
#
#
#

class cGamepad(object):
    
    def __init__(self, slot, dev, btnQueue):
        self.slot = slot
        self.dev = dev
        self.btnQueue = btnQueue

        self.joyObj = pygame.joystick.Joystick(slot)
        self.joyObj.init()
        self.num_axes = self.joyObj.get_numaxes()
        self.num_hats = self.joyObj.get_numhats()
        self.num_buttons = self.joyObj.get_numbuttons()
        self.keycombos = []
        
        for i in range(joy.num_buttons):
            self.keys[i] = False
        
        
    #
    #react on button presses, axis etc.
    #
    def handleEvent(self, event):
        #eventDict is used to put a message of the event into the btnQueue
        eventDict = {}
        eventDict["slot"] = self.slot
        
        #if Button up
        if event.type == JOYBUTTONUP:
            eventDict["type"] = 0
            eventDict["code"] = event.button
            eventDict["value"] = 0
            self.btnQueue.put(eventDict)
            self.keys[event.button] = False
            
        #if Button down
        elif event.type == JOYBUTTONDOWN:
            eventDict["type"] = 0
            eventDict["code"] = event.button
            eventDict["value"] = 1
            self.btnQueue.put(eventDict)
            self.keys[event.button] = True
            
        
        #check if event had influence on registered Keycombos
        eventDict = {}
        eventDict["slot"] = self.slot
        for combo in self.keycombos:
            pressed = True
            for key in combo.keys:
                if self.keys[key] == False:
                    pressed = False
                    break
                
            #if keycombo is pressed and wasnt pressed before
            #or isnt pressed but was before
            if pressed != combo.pressed:
                combo.pressed = pressed
                eventDict["type"] = 2
                eventDict["code"] = combo.id
                if pressed == True:
                    eventDict["value"] = 1
                else:
                    eventDict["value"] = 0    
                
        
        




#
# cDeviceHandler Class
#
#keeps track of the Gamepads and registers new ones(creates object of cGamepad class)
#receives events from gamepadListener and passes them to the gamepad object
#
class cDeviceHandler(threading.Thread):
    def __init__(self, buttonQueue, devQueue, logger):
        self.logger = logger
        self.logger.debug("cDeviceHandler initializing")
        
        self.buttonQueue = buttonQueue
        self.devQueue = devQueue
        self.gamepads = []
        
        self.start()
        
        
    def run(self):
        clock = pygame.time.Clock()
        time_change_prev = 0
        while True:
            clock.tick(5)
            
            time_change = time.mktime(time.localtime(ps.path.getmtime("")))
            if time_change_prev != time_change:
                time_change_prev = time_change
                self.gamepad_refresh()
            
    
    def gamepad_refresh(self):
        pass
    
    def passEvent(self, event):
        self.gamepads[event.joy].handleEvent(event)




#
# cGamepadListener Class
#
#creates object of deviceHandler Class automatically, but needs to be created manually itself
#listens for gamepad events on pygame eventqueue
#passes events to the device handler for further processing
#

class cGamepadListener(threading.Thread):
    def __init__(self, buttonQueue, devQueue):
        self.logger = logging.getLogger("cGamepad")
        self.logger.debug("cGamepad class initializing")
        
        self.deviceHandler = deviceHandler(buttonQueue, devQueue, self.logger)
        
        pygame.init()
        pygame.event.set_allowed(JOYBUTTONUP, JOYBUTTONDOWN)
        self.logger.debug("Pygame and eventQueue initialized")
        self.start()
        
    def run(self):
        self.eventHandler()
        
    def eventHandler(self):
        self.logger.debug(eventHandler)
        while True:
            event = pygame.event.wait()
            self.deviceHandler.passEvent(event)