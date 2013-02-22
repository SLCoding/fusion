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
import hashlib
from pygame.locals import *



def md5File(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()



#
# cKeycombo Class
#
#Used to manage keycombos, merely a structure
#
class cKeycombo(object):
    def __init__(self, keys):            
        btnkeys = []
        for key in keys:
            btnkeys.append("b" + str(key))
            
        self.keys = btnkeys
        self.pressed = False
        hashvalue = md5.new()
        
        
        for key in self.keys:
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
        self.hats = {}
        
        self.keycombos = []
        self.keymapName = ""
        self.keymap = {}
        self.loadKeymap(self.searchKeymap(self.joyObj.get_name()))
        
        for i in range(self.num_buttons):
            self.keys["b" + str(i)] = False
        
        
        
    def __del__(self):
        self.logger.debug("cGamepad destructor")
        self.joyObj.quit()
    
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
        
#TODO: Handle hat values
        elif event.type == JOYHATMOTION:
            try:
                if re.match("^b[0-9]+$", self.keymap["h" + str(event.axis)]):
                    eventDict["type"] = 0
                elif re.match("^a[0-9]+$", self.keymap["h" + str(event.hat) + "," + ""]):
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
#TODO: write function to create a new Keymap, maybe give option to use default one
        pass
    

    def registerKeycombo(self, keycombo):
        self.logger.debug("Gamepad registerKeycombo")
        self.keycombos.append(keycombo)
        
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
        
        self.registeredKeycombos = []
        self.gamepadsInitialized = False
        
        self.start()
        
        
    def run(self):
        clock = pygame.time.Clock()
        
        lastsum = ""
        while True:
            clock.tick(1)
#TODO: check last time changed, then do md5sum in order to maximize performance
            newsum = md5File("/proc/bus/input/devices")
            if newsum != lastsum:
                self.logger.debug("devices changed! Reinitializing Gamepads!")
                lastsum = newsum
                self.initialize_gamepads()
   
    def initialize_gamepads(self):
        self.logger.debug("Deleting old Gamepads")
        
        self.gamepadsInitialized = False
        
        #Uninitialize Gamepads
        for gamepad in self.gamepads:
            del gamepad
        self.gamepads = []
        
        #Uninitialize Joystick Module an clean up the garbage
        self.logger.debug("Uninitialize Joystick module")
        pygame.joystick.quit()
        self.logger.debug("Clear Event Queue")
        pygame.event.clear()
        
        #Reinitialize Joystick Module
        self.logger.debug("Initialize Joystick module")
        pygame.joystick.init()
        
        #Reinitialize Gamepads
        self.logger.debug("Initialize Gamepads")
        for i in range(pygame.joystick.get_count()):
            self.gamepads.append(cGamepad(i, self.btnQueue, self.logger))
        
        #Reregister Keycombos for all found Gamepads
        for keycombo in self.registeredKeycombos:
            for gamepad in self.gamepads:
                gamepad.registerKeycombo(keycombo)
        
        #Everything Reinitialized, new Gamepads should be registered
        self.gamepadsInitialized = True
        self.logger.debug("Reinitializing Gamedpads Done!")
        
        
    def passEvent(self, event):
        self.gamepads[event.joy].handleEvent(event)
        
    def registerKeycombo(self, keys, gamepad = None):
        self.logger.debug("DeviceHandler registerKeycombo")
        new_keycombo = cKeycombo(keys)
        self.registeredKeycombos.append(new_keycombo)
        
        if self.gamepadsInitialized:
            for gamepad in self.gamepads:
                gamepad.registerKeycombo(new_keycombo)
                
        return new_keycombo.id

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
        

        pygame.event.set_allowed((JOYBUTTONUP, JOYBUTTONDOWN, JOYAXISMOTION, JOYHATMOTION))
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




