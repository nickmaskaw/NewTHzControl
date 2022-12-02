import os
import time as tm
import numpy as np
from pandas import DataFrame
from PyQt6.QtCore import QObject, pyqtSignal

class Constants:
    C = 299_792_458e3/1e12  # mm/ps (~0.3mm/ps)
    

class Convert:
    @staticmethod
    def ps_to_mm(t):
        return t * Constants.C

    @staticmethod
    def mm_to_ps(d):
        return d / Constants.C
        
        
class MeasurementSignals(QObject):
    update = pyqtSignal(object)
    finish = pyqtSignal()
        
        
class Measurement:
    DATA_FOLDER = './output/data'
    INFO_FOLDER = './output/info'
    PLOT_FOLDER = './output/plot'
    
    def __init__(self, parameters, lockin, cernox, thz_dl, pmp_dl):
        self.parameters = parameters
        self.lockin  = lockin
        self.cernox  = cernox
        self.thz_dl  = thz_dl
        self.pmp_dl  = pmp_dl
        self.signals = MeasurementSignals()
        
        self._checkOutputFolders()
    
    def _checkOutputFolders(self):
        folders = [self.DATA_FOLDER, self.INFO_FOLDER, self.PLOT_FOLDER]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created {folder} folder")
        print("Measurement output folders OK")
            
    def thzScan(self):
        thz_start = float(parameters.mandatory.thz_start)
        thz_end   = float(parameters.mandatory.thz_end)
        thz_step  = float(parameters.mandatory.thz_step) 
        thz_vel   = float(parameters.mandatory.thz_vel)
        tcons     = float(parameters.hidden.tcons) 
        wait      = float(parameters.mandatory.wait)   
    
        self.thz_dl.returnTo(thz_start)
        self.thz_dl.startPolling(10)
        self.thz_dl.setVelocity(thz_velocity)
        tm.sleep(10 * time_constant)
        
        N   = int( abs(thz_end - thz_start) / thz_step ) + 1
        pos = np.linspace(thz_start, thz_end, N)
        X   = np.full(N, np.nan)
        R   = np.full(N, np.nan)
        
        R[0] = self.cernox.fres()
        
        for i in range(N):
            self.thz_dl.moveTo(pos[i])
            tm.sleep(wait_time * time_constant)
            X[i] = self.lockin.X()
            
        
        R[i] = self.cernox.fres()
        
        self.thz_dl.stopPolling()