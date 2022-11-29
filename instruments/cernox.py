from instruments import Multimeter
from numpy import interp
from pandas import read_table


class Cernox(Multimeter):
    CALIBRATION_FILE = './instruments/cernox_calibration/table.dat'

    def __init__(self, name="Cernox"):
        super().__init__(name)
        
        self._calibration = read_table(self.CALIBRATION_FILE)
        
    @property
    def calibration(self): return self._calibration

    # Try to implement some sort of temperature conversion...
    def temperature(self):
        measured_R = self.fres()
        tabled_R   = self.calibration['R']
        tabled_T   = self.calibration['T']
        
        return interp(measured_R, tabled_R, tabled_T)