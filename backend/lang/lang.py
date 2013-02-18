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
import logging
from ConfigParser import SafeConfigParser

class lang(object):
    """
    Languagefile Support
    
    """
    def __init__(self, langcode = None):
        self.logger = logging.getLogger('lang')
        self.langcode = langcode
        self.langpath = os.path.join(os.getcwd(), 'lang')
        
        fullpath = os.path.join(self.langpath, langcode + '.lang')
        if not os.path.isfile(fullpath):
            self.logger.warn('"%s.lang" dosn\'t exist. '
                '"en.lang" is taken instead' % self.langcode)
            
            fullpath = os.path.join(self.langpath, 'en.lang')
            if not os.path.isfile(fullpath):
                self.logger.error('Default file dosn\'t exist either...')
                
        
        # Read Langfile
        self.langfile = SafeConfigParser()
        self.langfile.read(fullpath)
        
        self.logger.debug('Instance of lang created')
        
    def __del__(self):
        pass

    def getString(self, section, name):
        try:
            return self.langfile.get(section, name)
        except:
            self.logger.warn('String (%s) or Seciton (%s) '
                'in laguagefile not found' % (name, section) )
            return None
        
        
    def getCurrent(self):
        try:
            return { 'code': self.langfile.get('general', 'code'),
                'name': self.langfile.get('general', 'name'), 
                'author': self.langfile.get('general', 'author') }
        except:
            self.logger.error('Missing general information '
                'in languagefile "%s.lang"' % self.langcode)
            return -1
        
    def getAvailable(self):
        avlangs = []

        try:
            for avlangfile in os.listdir(self.langpath):
                tempfile = SafeConfigParser()
                tempfile.read(os.path.join(self.langpath, avlangfile))
                try:
                    avlangs.append( {'code': tempfile.get('general', 'code'),
                        'name': tempfile.get('general', 'name'), 
                        'author': tempfile.get('general', 'author')} )
                except:
                    self.logger.error('Missing general information '
                        'in languagefile "%s"' % avlangfile)
        except OSError:
            self.logger.critical( 'Path to langfiles don\'t exist!' )
            return -1
            
        return avlangs
        

if __name__ == "__main__":
    pass