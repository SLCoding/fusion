import threading
import abc

class cEmulator(threading.Thread):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def startEmulator():
        """Starts emulator"""
        raise "startEmulator() not implemented"
    
    @abc.abstractmethod
    def killEmulator():
        """Kills emulator instantly"""
        raise "killEmulator() not implemented"
    
    