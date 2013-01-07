#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import pygame
import threading
from pygame.locals import *

#
#Gamepad Class
#
#Used to store information like slot, keymapping etc
#passes button presses into the queue
#
#
#

class gamepad(object):
	def __init__(self, slot, dev, buttonQueue):
		self.slot = slot
		self.dev = dev
		self.buttonQueue = buttonQueue
	
		self.joyObj = pygame.joystick.Joystick(slot)
		self.joyObj.init()
		
		for i in range(joy.Obj.get_numbuttons()):
			self.keys[i] = False
		
	def handleEvent(self, event):
		if event.type == JOYBUTTONUP:
			self.keys[event.button] = False
		elif event.type == JOYBUTTONDOWN:
			self.keys[event.button] = True
		
		#tastenkombo




#
# deviceHandler Class
#
#keeps track of the Gamepads and registers new ones(creates object of gamepad class)
#
#
#receives events from gamepadListener and passes them to the gamepad object
#
class deviceHandler(threading.Thread):
	def __init__(self, buttonQueue, devQueue):
		self.buttonQueue = buttonQueue
		self.devQueue = devQueue
		self.start()
		
		self.gamepads = []
		
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
# gamepadListener Class
#
#creates object of deviceHandler Class automatically, but needs to be created manually itself
#
#listens for gamepad events on pygame eventqueue
#
#passes events to the device handler for further processing
#

class gamepadListener(threading.Thread):
	def __init__(self, buttonQueue, devQueue):
		self.deviceHandler = deviceHandler(buttonQueue, devQueue)
		
		pygame.init()
		pygame.event.set_allowed(JOYBUTTONUP, JOYBUTTONDOWN)
		self.start()
	
	def run(self):
		self.eventHandler()
		
		
	def eventHandler(self):
		while True:
			event = pygame.event.wait()
			self.deviceHandler.passEvent(event)