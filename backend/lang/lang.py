#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

@author: wiesendaniel (Daniel Wiesendorf)
"""

import os
from ConfigParser import SafeConfigParser

class lang(object):
	"""
	Languagefile Support
	
	"""
	def __init__(self, langcode):
		self.langpath='lang'
		
		# Read Configfile
		self.langfile = SafeConfigParser()
		self.langfile.read(os.path.join(self.langpath, langcode + '.lang'))

		
	def __del__(self):
		pass


	def getString(self, section, name):
		return self.langfile.get(section, name)
		
	def getCurrent(self):
		return {'code': self.langfile.get('general', 'code'),
			'name': self.langfile.get('general', 'name'), 
			'author': self.langfile.get('general', 'author')}
		
	def getAvailable(self):
		avlangs = []
		
		for avlangfile in os.listdir(self.langpath):
			tempfile = SafeConfigParser()
			tempfile.read(os.path.join(self.langpath, avlangfile))
			
			avlangs.append( {'code': tempfile.get('general', 'code'),
				'name': tempfile.get('general', 'name'), 
				'author': tempfile.get('general', 'author')} )
			
		return avlangs
		

if __name__ == "__main__":
	langinst = lang('de')
	print langinst.getString('test', 'string1')
	print langinst.getCurrent()
	print langinst.getAvailable()