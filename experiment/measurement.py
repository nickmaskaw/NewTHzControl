import os
import time as tm
import numpy as np
from pandas import DataFrame
from PyQt6.QtCore import QObject, QThreadPool, QRunnable, pyqtSignal, pyqtSlot


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
    started  = pyqtSignal()
    updated  = pyqtSignal(object, object)
    finished = pyqtSignal()
    
    
class MeasurementWorker(QRunnable):
    def __init__(self, func):
        super().__init__()
        self.func = func
    
    @pyqtSlot()
    def run(self):
        self.func()
        
        
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
        self.break_  = False
        
        self._checkOutputFolders()
    
    def _checkOutputFolders(self):
        folders = [self.DATA_FOLDER, self.INFO_FOLDER, self.PLOT_FOLDER]
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created {folder} folder")
        print("Measurement output folders OK")

    def scan(self):
        thz_start = float(self.parameters.mandatory.thz_start.value)
        thz_end   = float(self.parameters.mandatory.thz_end.value)
        thz_step  = float(self.parameters.mandatory.thz_step.value) 
        thz_vel   = float(self.parameters.mandatory.thz_vel.value)
        
        pmp_start = float(self.parameters.mandatory.pmp_start.value)
        pmp_end   = float(self.parameters.mandatory.pmp_end.value)
        pmp_step  = float(self.parameters.mandatory.pmp_step.value) 
        pmp_vel   = float(self.parameters.mandatory.pmp_vel.value)
        
        tcons     = float(self.parameters.hidden.tcons.value) 
        wait      = float(self.parameters.mandatory.wait.value)
        plot_rate = int(self.parameters.mandatory.plot_rate.value)
        repeat    = int(self.parameters.unsavable.repeat.value)
        
        thz_N = int( abs(thz_end - thz_start) / thz_step ) + 1
        pmp_N = int( abs(pmp_end - pmp_start) / pmp_step ) + 1
        
        thz_pos = np.linspace(thz_start, thz_end, thz_N)
        pmp_pos = np.linspace(pmp_start, pmp_end, pmp_N)
        
        for rep in range(repeat):
            self.thz_dl.returnTo(thz_start)
            self.pmp_dl.returnTo(pmp_start)
            self.thz_dl.setVelocity(thz_vel)
            self.pmp_dl.setVelocity(pmp_vel)
            tm.sleep(10 * tcons)

            self.thzScan(thz_N, thz_pos, wait, tcons)
                    
        self.signals.finished.emit()
             
    
    def thzScan(self, N, pos, wait, tcons):
        X = np.full(N, np.nan)
        
        for i in range(N):
            self.thz_dl.moveTo(pos[i])
            tm.sleep(wait * tcons)
            X[i] = self.lockin.X()
            if i% plot_rate == 0:
                self.signals.updated.emit(pos, X)
                    
            if self.break_:
                self.break_ = False
                break
        
        print(DataFrame({'pos': pos, 'X': X}))

    
    def thzScan_(self):
        thz_start = float(self.parameters.mandatory.thz_start.value)
        thz_end   = float(self.parameters.mandatory.thz_end.value)
        thz_step  = float(self.parameters.mandatory.thz_step.value) 
        thz_vel   = float(self.parameters.mandatory.thz_vel.value)
        tcons     = float(self.parameters.hidden.tcons.value) 
        wait      = float(self.parameters.mandatory.wait.value)
        plot_rate = float(self.parameters.mandatory.plot_rate.value)
    
        self.thz_dl.returnTo(thz_start)
        self.thz_dl.startPolling(10)
        self.thz_dl.setVelocity(thz_vel)
        tm.sleep(10 * tcons)
        
        N   = int( abs(thz_end - thz_start) / thz_step ) + 1
        pos = np.linspace(thz_start, thz_end, N)
        X   = np.full(N, np.nan)
        R   = np.full(N, np.nan)
        
        R[0] = self.cernox.fres()
        
        for i in range(N):
            self.thz_dl.moveTo(pos[i])
            tm.sleep(wait * tcons)
            X[i] = self.lockin.X()
            if i % plot_rate == 0:
                self.signals.updated.emit(pos, X)
                
            if self.break_:
                self.break_ = False
                break
            
        self.thz_dl.stopPolling()
        R[i] = self.cernox.fres()
        self.signals.finished.emit()
        print(DataFrame({'pos': pos, 'X': X}))  
       
    def dumbScan(self):
        t0 = tm.time()
        thz_start = float(self.parameters.mandatory.thz_start.value)
        thz_end   = float(self.parameters.mandatory.thz_end.value)
        thz_step  = float(self.parameters.mandatory.thz_step.value)
        thz_vel   = float(self.parameters.mandatory.thz_vel.value)
        tcons     = .1
        wait      = float(self.parameters.mandatory.wait.value)
        plot_rate = float(self.parameters.mandatory.plot_rate.value)
        
        N   = int( abs(thz_end - thz_start) / thz_step ) + 1
        pos = np.linspace(thz_start, thz_end, N)
        X   = np.full(N, np.nan)
        
        self.signals.started.emit()
        
        for i in range(N):
            tm.sleep(wait * tcons)
            X[i] = (np.random.normal() + i)
            if i % plot_rate == 0:
                self.signals.updated.emit(pos, X)
            
            if self.break_:
                self.break_ = False
                break

        self.signals.finished.emit()
        print(tm.time() - t0)
        
    @pyqtSlot()
    def setBreak(self, state):
       self.break_ = state
    @pyqtSlot()
    def run(self):
        pool = QThreadPool.globalInstance()
        worker = MeasurementWorker(self.scan)
        pool.start(worker)