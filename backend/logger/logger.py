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

class logger(object):
    """
    Loggerinit
    
    """
    def __init__(self, levelconsole = None):
        
        #read configfile
        
        configfile = SafeConfigParser()
        configfile.read( os.path.expanduser('~/.fusion/fusion.cfg') )
        
        level = configfile.get('logger', 'file_level')
                
        log_format = '%(asctime)s %(levelname)-8s %(name)-12s: %(message)s'
        log_dateformat = '%Y%m%d %H:%M'
        log_file = configfile.get('logger', 'file')
                
        # set up logging to file - see previous section for more details
        if level == '1':
            logging.basicConfig(level=logging.DEBUG,
                format=log_format, datefmt=log_dateformat,
                filename=log_file, filemode='w')
        elif level == '2':
            logging.basicConfig(level=logging.INFO,
                format=log_format, datefmt=log_dateformat,
                filename=log_file, filemode='w')
        elif level == '3':
            logging.basicConfig(level=logging.WARNING,
                format=log_format, datefmt=log_dateformat,
                filename=log_file, filemode='w')
        elif level == '4':
            logging.basicConfig(level=logging.ERROR,
                format=log_format, datefmt=log_dateformat,
                filename=log_file, filemode='w')
        elif level == '5':
            logging.basicConfig(level=logging.CRITICAL,
                format=log_format, datefmt=log_dateformat,
                filename=log_file, filemode='w')

        console = logging.StreamHandler()
        
        if levelconsole == None:
            levelconsole = configfile.get('logger', 'console_level')
        
        if levelconsole == '1':
            console.setLevel(logging.DEBUG)
        elif levelconsole == '2':
            console.setLevel(logging.INFO)
        elif levelconsole == '3':
            console.setLevel(logging.WARNING)
        elif levelconsole == '4':
            console.setLevel(logging.ERROR)
        elif levelconsole == '5':
            console.setLevel(logging.CRITICAL)
        
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(levelname)-8s %(name)-12s: %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
        

if __name__ == "__main__":
    pass