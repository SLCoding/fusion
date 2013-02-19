#-*- coding: utf-8 -*-

import time
import re
import Queue
import ConfigParser
import pygame
import threading
import logging
import sys
import os
import md5
from pygame.locals import *

#
# cKeycombo Class
#
#Used to manage keycombos, merely a structure
#
class cKeycombo(object):
    def __init__(self, keys):
        self.keys = keys
        self.pressed = False
        hashvalue = md5.new()
        for key in keys:
            hashvalue.update(str(key))
        self.id = hashvalue.hexdigest()
        
#
# cGamepad Class
#
#Used to store information like slot, keymapping etc
#passes button presses into the queue
#
class cGamepad(object):
    
    def __init__(self, slot, btnQueue, logger):
        self.logger = logger
        self.logger.debug("cGamepad initialized")
        self.slot = slot
        self.btnQueue = btnQueue

        self.joyObj = pygame.joystick.Joystick(slot)
        self.joyObj.init()
        self.num_axes = self.joyObj.get_numaxes()
        self.num_hats = self.joyObj.get_numhats()
        self.num_buttons = self.joyObj.get_numbuttons()
        self.keys = {}
        self.keycombos = []
        self.keymapName = ""
        self.keymap = {}
        self.loadKeymap(self.searchKeymap(self.joyObj.get_name()))
        
        for i in range(self.num_buttons):
            self.keys["b" + str(i)] = False
        
    #
    #react on button presses, axis etc.
    #
    def handleEvent(self, event):
        #eventDict is used to put a message of the event into the btnQueue
        eventDict = {}
        eventDict["slot"] = self.slot
        
        
        #if Button up
        if event.type == JOYBUTTONUP:
            #self.logger.debug("Controller " + str(self.slot) + " BUTTONUP " + str(self.keymap["b" + str(event.button)]))
            try:
                if re.match("^b[0-9]+$", self.keymap["b" + str(event.button)]):
                    eventDict["type"] = 0
                elif re.match("^a[0-9]+$", self.keymap["b" + str(event.button)]):
                    eventDict["type"] = 1
                else:
                    self.logger.error("Button mapping exception")
            except KeyError:
                pass
            else:
                eventDict["code"] = int((self.keymap["b" + str(event.button)])[1:])
                eventDict["value"] = 0
                self.btnQueue.put(eventDict)
                self.keys[self.keymap["b" + str(event.button)]] = False
            
        #if Button down
        elif event.type == JOYBUTTONDOWN:
            #self.logger.debug("Controller " + str(self.slot) + " BUTTONDOWN " + str(self.keymap["b" + str(event.button)]))
            try:
                if re.match("^b[0-9]+$", self.keymap["b" + str(event.button)]):
                    eventDict["type"] = 0
                elif re.match("^a[0-9]+$", self.keymap["b" + str(event.button)]):
                    eventDict["type"] = 1
                else:
                    self.logger.error("Button mapping exception")
            except KeyError:
                pass
            else:
                eventDict["code"] = int((self.keymap["b" + str(event.button)])[1:])
                eventDict["value"] = 1
                self.btnQueue.put(eventDict)
                self.keys[self.keymap["b" + str(event.button)]] = True
        
        #if Axis moved
        elif event.type == JOYAXISMOTION:
            try:
                if re.match("^b[0-9]+$", self.keymap["a" + str(event.axis)]):
                    eventDict["type"] = 0
                elif re.match("^a[0-9]+$", self.keymap["a" + str(event.axis)]):
                    eventDict["type"] = 1
                else:
                    self.logger.error("Button mapping exception")
            except KeyError:
                pass
            else:
                eventDict["code"] = int((self.keymap["a" + str(event.axis)])[1:])
                eventDict["value"] = event.value
                self.btnQueue.put(eventDict)
        
        
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
        configparser.read( os.path.expanduser('~/.fusion/hardware/keymaps.default.cfg') )
        
        
        for section in configparser.sections():
            self.logger.debug(section + " regex:" + configparser.get(section, "regex") + "name: " + name)
            if re.match(configparser.get(section, "regex"), name):
                self.logger.debug("Keymap found for Controller " + name + ": " + section)
                return section
        self.logger.debug("No Keymap found for Controller " + name)
        return None
    
    
    def loadKeymap(self, keymap):
        configparser = ConfigParser.SafeConfigParser()
        configparser.read( os.path.expanduser('~/.fusion/hardware/keymaps.default.cfg') )
        
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
    #generates a new Keymap for unknown gamepads
    #
    def newKeymap(self):
        pass
    
    
    def registerKeycombo(self, keys):
        self.logger.debug("Gamepad registerKeycombo")
        btnkeys = []
        for key in keys:
            btnkeys.append("b" + str(key))
        keycombo = cKeycombo(btnkeys)
        self.keycombos.append(keycombo)
        return keycombo.id
        
#
# cDeviceHandler Class
#
#keeps track of the Gamepads and registers new ones(creates object of cGamepad class)
#receives events from cGamepadListener and passes them to the gamepad object
#
class cDeviceHandler(threading.Thread):
    def __init__(self, btnQueue, devQueue, logger):
        threading.Thread.__init__(self)
        self.logger = logger
        self.logger.debug("cDeviceHandler initializing")
        
        self.btnQueue = btnQueue
        self.devQueue = devQueue
        self.gamepads = []
        
        self.start()
      
    def run(self):
        for i in range(pygame.joystick.get_count()):
            self.gamepads.append(cGamepad(i, self.btnQueue, self.logger))
            
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
        
    def registerKeycombo(self, keys, gamepad = None):
        self.logger.debug("DeviceHandler registerKeycombo")
        comboid = None
        if gamepad == None:
            for gamepad in self.gamepads:
                comboid = gamepad.registerKeycombo(keys)
        else:
            comboid = self.gamepads[gamepad].registerKeycombo(keys)
        
        return comboid

#
# cGamepadListener Class
#
#creates object of deviceHandler Class automatically, but needs to be created manually itself
#listens for gamepad events on pygame eventqueue
#passes events to the device handler for further processing
#
class cGamepadListener(threading.Thread):
    def __init__(self, btnQueue, devQueue):
        threading.Thread.__init__(self)
        self.logger = logging.getLogger("cGamepad")
        self.logger.debug("cGamepad class initializing")
        
        self.btnQueue = btnQueue
        self.devQueue = devQueue
        
        pygame.init()
        pygame.joystick.init()
        
        self.deviceHandler = cDeviceHandler(btnQueue, devQueue, self.logger)
        

        pygame.event.set_allowed((JOYBUTTONUP, JOYBUTTONDOWN, JOYAXISMOTION))
        self.logger.debug("Pygame and eventQueue initialized")
        self.start()
        
    def run(self):
        self.logger.debug("cGamepadListener: eventHandler Thread startet!")
        self.eventHandler()
        
    def eventHandler(self):
        while True:
            event = pygame.event.wait()
            self.deviceHandler.passEvent(event)
    
    def registerKeycombo(self, keys, gamepad = None):
        self.logger.debug("GamepadListener registerKeycombo")
        return self.deviceHandler.registerKeycombo(keys, gamepad)




