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

Get more information at: https://github.com/SLCoding/fusion

@author: wiesendaniel (Daniel Wiesendorf)
@author: Japortie (Marcus Schütte)
@version: v0.1
"""

import os
import sys
import getopt
import backend.hardware.gamepad
import Queue
import time
import thread

def mappingThread(devQueue):
    while True:
        evt = devQueue.get()
        if evt["key"] != None:
            print "Press " + evt["key"]
        else:
            print "Mapping succesful"
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def start(loggervalue):
    # create logger
    from backend.logger.logger import logger
    logger(loggervalue)

    listener = backend.hardware.gamepad.cGamepadHandler()
    
    devQueue = listener.devQueue
    btnQueue = listener.btnQueue
    
    #combo = listener.registerKeycombo((0,3, 8, 9, 10, 11))
    #thread.start_new_thread(mappingThread, (devQueue, ))
    while True:
        evt = btnQueue.get()
        print evt
    
    listener.join()
    
    
    #from backend.lang.lang import lang
    #langinst = lang('de')
    #langinst.getString('test1', 'string3')
    #langinst.getCurrent()
    #print langinst.getAvailable()
    
    return 0

def main(argv=None):
    """
usage: fusion [options] 
Options:
            [-h] [--help]                     show help
            [-u] [--usage]                    show this
            [-d] (1-5) [--debug] (1-5)        debug output level
            [-s] [--start]                    start the script
    """
    
#   if not os.geteuid()==0:
#       sys.exit("Only root can run this script")    
      
    
    
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hud:", ["help", "usage", "debug="])
        except getopt.error, msg:
            raise Usage(msg)
        
        loggervalue = None
        
        for option, value in opts:
            if option in ("-h", "--help"):
                print __doc__
                break
                
            elif option in ("-u", "--usage"):
                print main.__doc__
                break
                
            elif option in ("-d", "--debug"):
                if int(value) > 5 or int(value) < 1:
                    raise Usage('Debugvalue has to be between 1 and 5')
                loggervalue = value
                break
            
        sys.exit(start(loggervalue))

    except Usage, err:
        print str(err.msg)
        print "for help use --help or --usage"
        return 2


if __name__ == "__main__":
    sys.exit(main())