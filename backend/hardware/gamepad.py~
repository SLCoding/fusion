#-*- coding: utf-8 -*-

import time
import re
import ConfigParser
import pygame
import threading
import logging
from pygame.locals import *

#
# cKeycombo Class
#
#Used to manage keycombos, merely a structure
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
class cGamepad(object):
    
    def __init__(self, slot, dev, btnQueue, logger):
        self.logger = logger
        self.logger.debug("cGamepad initialized")
        self.slot = slot
        self.dev = dev
        self.btnQueue = btnQueue

        self.joyObj = pygame.joystick.Joystick(slot)
        self.joyObj.init()
        self.num_axes = self.joyObj.get_numaxes()
        self.num_hats = self.joyObj.get_numhats()
        self.num_buttons = self.joyObj.get_numbuttons()
        self.keycombos = []
        self.keymapName = ""
        self.keymap = {}
        self.loadKeymap(self.searchKeymap(self.joyObj.get_name()))
        
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
            self.logger.debug("Controller " + self.slot + " BUTTONUP " + self.keymap["b" + event.button])
            eventDict["type"] = 0
            eventDict["code"] = self.keymap["b" + event.button]
            eventDict["value"] = 0
            self.btnQueue.put(eventDict)
            self.keys[self.keymap["b" + event.button]] = False
            
        #if Button down
        elif event.type == JOYBUTTONDOWN:
            self.logger.debug("Controller " + self.slot + " BUTTONDOWN " + self.keymap["b" + event.button])
            eventDict["type"] = 0
            eventDict["code"] = self.keymap["b" + event.button]
            eventDict["value"] = 1
            self.btnQueue.put(eventDict)
            self.keys[self.keymap["b" + event.button]] = True
            
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
                self.btnQueue.put(eventDict)
    
    #
    #loads presaved Keymap for known gamepads         
    #
    def searchKeymap(self, name):
        configparser = ConfigParser.SafeConfigParser()
        #TODO: configfile angeben
        
        for section in configparser.sections():
            if re.match(configparser.get(section, "regex"), name):
                return section
        return None
    
    
    def loadKeymap(self, keymap):
        configparser = ConfigParser.SafeConfigParser()
        #TODO: configfile angeben
        
        if keymap == None:
            self.newKeymap()
        else:
            if configparser.has_section(keymap):
                self.keymapName = keymap
                for option in configparser.options(keymap):
                    self.keymap[configparser.get(keymap, option)] = option
            else:
                return None
    
    #
    #gnerates a new Keymap for unknown gamepads
    #
    def newKeymap(self):
        pass
#
# cDeviceHandler Class
#
#keeps track of the Gamepads and registers new ones(creates object of cGamepad class)
#receives events from cGamepadListener and passes them to the gamepad object
#
class cDeviceHandler(threading.Thread):
    def __init__(self, btnQueue, devQueue, logger):
        self.logger = logger
        self.logger.debug("cDeviceHandler initializing")
        
        self.btnQueue = btnQueue
        self.devQueue = devQueue
        self.gamepads = []
        
        self.start()
      
    def run(self):
        for i in range(pygame.joystick.get_count):
            self.gamepads.append(pygame.joystick.Joystick(i))
            self.gamepads[i].init()
            
#        clock = pygame.time.Clock()
#        time_change_prev = 0
#        while True:
#            clock.tick(5)
#            
#            time_change = time.mktime(time.localtime(ps.path.getmtime("")))
#            if time_change_prev != time_change:
#                time_change_prev = time_change
#                self.gamepad_refresh()
#            
#    def gamepad_refresh(self):
#        pass
#    
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
    def __init__(self, btnQueue, devQueue):
        self.logger = logging.getLogger("cGamepad")
        self.logger.debug("cGamepad class initializing")
        
        self.deviceHandler = deviceHandler(btnQueue, devQueue, self.logger)
        
        pygame.init()
        pygame.event.set_allowed(JOYBUTTONUP, JOYBUTTONDOWN)
        self.logger.debug("Pygame and eventQueue initialized")
        self.start()
        
    def run(self):
        self.logger.debug("cGamepadListener: eventHandler Thread startet!")
        self.eventHandler()
        
    def eventHandler(self):
        self.logger.debug(eventHandler)
        while True:
            event = pygame.event.wait()
            self.deviceHandler.passEvent(event)