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
    Initialisation of the standard Python logger.
    Sets root logger and its config.
    """

    def __init__(self, console_level = None):
        
        #read configfile 
        configfile = SafeConfigParser()
        configfile.read( os.path.expanduser('~/.fusion/fusion.cfg') )
        
        log_file = configfile.get('logger', 'file')
        file_level = configfile.get('logger', 'file_level')
        #get console logginglevel from config if logging param isn't set
        if console_level == None:
            console_level = configfile.get('logger', 'console_level')

        
        log_dateformat = '%Y%m%d %H:%M'
        #set format for logging to file
        file_format = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(name)-12s: %(message)s', datefmt=log_dateformat)
        # set a format which is simpler for console use
        console_format = logging.Formatter(fmt='%(levelname)-8s %(name)-12s: %(message)s', datefmt=log_dateformat)
                        
        # set up rootlogger
        logging.basicConfig(level=logging.DEBUG, filename='/dev/null')
        
        if not file_level == '0':
            #create a file logger
            filelogger = logging.FileHandler(log_file)
            
            if file_level == '1':
                filelogger.setLevel(logging.DEBUG)
            elif file_level == '2':
                filelogger.setLevel(logging.INFO)
            elif file_level == '3':
                filelogger.setLevel(logging.WARNING)
            elif file_level == '4':
                filelogger.setLevel(logging.ERROR)
            elif file_level == '5':
                filelogger.setLevel(logging.CRITICAL)
            
            # tell the handler to use this format
            filelogger.setFormatter(file_format)
            
            # add the handler to the root logger
            logging.getLogger('').addHandler(filelogger)
        
        if not console_level == '0':
            #create a console logger
            consolelogger = logging.StreamHandler()
            
            if console_level == '1':
                consolelogger.setLevel(logging.DEBUG)
            elif console_level == '2':
                consolelogger.setLevel(logging.INFO)
            elif console_level == '3':
                consolelogger.setLevel(logging.WARNING)
            elif console_level == '4':
                consolelogger.setLevel(logging.ERROR)
            elif console_level == '5':
                consolelogger.setLevel(logging.CRITICAL)
            
            # tell the handler to use this format
            consolelogger.setFormatter(console_format)
            
            # add the handler to the root logger
            logging.getLogger('').addHandler(consolelogger)
            

if __name__ == "__main__":
    pass