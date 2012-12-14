#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygame
import time
import re
well_known_gamepads = {"3":"PS3", "Xbox":"XBOX"}

class cGamepad(object):
	
	
	def __init__(self, p_slot):
		self.slot = p_slot
		if not pygame.joystick.get_init():
			pygame.jostick.init()
			
		self.joy_obj = pygame.joystick.Joystick(p_slot)

		if not self.joy_obj.get_init():
			self.joy_obj.init()
			
		self.name = self.joy_obj.get_name()
		
		for well_known in well_known_gamepads:
			print well_known
			if re.search(well_known, self.name ) != None:
				self.type = well_known_gamepads[well_known]
				break
			else:
				self.type = "UNKNOWN"
		
		
		
		
	@staticmethod
	def get_Gamepads(num = 0):
		if num != 0:
			return cGamepad(num)
			
		if not pygame.joystick.get_init():
			pygame.joystick.init()
		gamepads = []
		
		gamepad_count = pygame.joystick.get_count()
		
		for i in range(0, gamepad_count):
			gamepads.append(cGamepad(i))
		return gamepads
			
			
	def printInfo(self):
		print "Slot: " + str(self.slot)
		print "Name: " + str(self.name)
		print "Type: " + str(self.type)




#pygame.init()
pygame.joystick.init()

#well_known_controller = ("PLAYSTATION", "XBOX")

gamepads = cGamepad.get_Gamepads()
for gamepad in gamepads:
	gamepad.printInfo()
#gamepad = cGamepad.get_Gamepads()
#gamepad.printInfo()

a = raw_input("Zum Beenden Taste drücken")


print "test"
