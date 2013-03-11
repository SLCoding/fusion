#-*- coding: utf-8 -*-

import thread
import pygame
from pygame.locals import *
import logging
import Queue
import md5
import hashlib
import re
import time
import commands

#TODO: write with md5 module, purge hashlib
def md5File(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()


class cMapping(object):
    """maps physical gamepad buttons to functions or keycodes for specific
    emulators or similar"""
    def __init__(self, pJoyName, pMapName):
        pass
#TODO: Mapping Class

class cGamepad(object):
    """holds information about input device"""
    def __init__(self, pSlot, pDevQueue, pLogger):
        self.logger = pLogger
        self.logger.debug("cGamepad initialized")
        self.slot = pSlot
        self.devQueue = pDevQueue
        self.batStat = -1
        
        self.joyObj = pygame.joystick.Joystick(self.slot)
        self.joyObj.init()
        self.name = self.joyObj.get_name()
        self.num_axes = self.joyObj.get_numaxes()
        self.num_hats = self.joyObj.get_numhats()
        self.num_buttons = self.joyObj.get_numbuttons()
        
        self.mapping = {}
        #self.loadKeymap(self.searchKeymap(self.joyObj.get_name()))
        
        
        #set mac-adress if sixaxis controller
        if re.match("^PLAYSTATION\(R\)3 Controller \([A-F0-9:]{17}\)$", self.name):
            self.mac = re.findall("[A-F0-9:]{17}", self.name)[0]
        else:
            self.mac = None
#TODO: check if battery status is available
        
        #if theres a mac adderss (its a sixaxis controller) start batteryListener
        if self.mac != None:
            thread.start_new_thread(self.batteryListener, ())
        
    def __del__(self):
        self.logger.debug("cGamepad destructor")
        self.joyObj.quit()


    def getBattery(self):
        batQuery = "sudo hcidump -R -O '"+self.mac
        +"' | head -n 5 | tail -n 1 | awk '{printf$1}'"
        return int(commands.getoutput(batQuery)) * 20
    
    def batteryListener(self):
        while True:
            newBatStat = self.getBattery()
            self.logger.debug("Controller " + str(self.slot) +
                              " Battery Status: " + str(batStat))
            
            
        #commands.getoutput("sudo killall hcidump > /dev/null")
            #if battery Status changed, pusch it to the Queue
            if self.batStat != newBatStat:
                self.logger.info("Controller " + str(self.slot) +
                                 " New Battery Status: " + str(batStat))
            time.sleep(20)
#TODO: battery status ->queue


class cGamepadHandler(object):
    """handles gamepads and passes button events"""
    def __init__(self):
        #Set class-variables
        #initialize logger
        self.logger = logging.getLogger("cGamepad")
        self.logger.debug("cGamepad class initializing")
        
        self.gamepadsInitialized = False
        self.gamepads = {}
        
        self.btnQueue = Queue.Queue()
        self.devQueue = Queue.Queue()
        
        #initialize pygame modules
        pygame.init()
        pygame.joystick.init()
#TODO: enable JOYHATMOTION
        pygame.event.set_allowed((JOYBUTTONUP, JOYBUTTONDOWN,
                                  JOYAXISMOTION))
        self.logger.debug("Pygame and eventQueue initialized")
        
        #Now start Threads (gamepadListener and eventHandler)
        thread.start_new_thread(self.gamepadListener, ())
        thread.start_new_thread(self.eventHandler, ())
        
    #
    #Threaded! watches for recently (dis-)connected gamepads
    def gamepadListener(self):
        clock = pygame.time.Clock()
        
        lastsum = ""
        while True:
            clock.tick(1)
#TODO: check last time changed, then do md5sum in order to maximize performance
            newsum = md5File("/proc/bus/input/devices")
            if newsum != lastsum:
                self.logger.debug("Devices changed! Reinitializing Gamepads!")
                lastsum = newsum
                self.initializeGamepads()
        
    #
    #Threaded! waits for events in pygame eventQueue and passes them on
    def eventHandler(self):
        while True:
            event = pygame.event.wait()
            self.btnQueue.put(event)
    
    def initializeGamepads(self):
        self.logger.debug("Deleting old Gamepads")
        #set gamepads uninitialized to prevent from errors while reinitializing
        self.gamepadsInitialized = False
        
        #Uninitialize Gamepads
        for gamepad in self.gamepads:
            del gamepad
        self.gamepads = []
        
        #Uninitialize Joystick Module and clean up the garbage
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
            self.gamepads.append(cGamepad(i, self.devQueue, self.logger))
        
        
        #Everything Reinitialized, new Gamepads should be registered
        self.gamepadsInitialized = True
        self.logger.debug("Reinitializing Gamedpads Done!")
        