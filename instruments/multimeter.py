from instruments import VISAInstrument


class Multimeter(VISAInstrument):
    def __init__(self, name="Multimeter"):
        super().__init__(name)
        
    @property
    def idn(self): return self.device.query('*IDN?')

    def volt(self):
        volt = self.device.query('MEAS?')
        return float(volt)

    def curr(self):
        curr = self.device.query('MEAS:CURR?')
        return float(curr)

    def fres(self):
        fres = self.device.query('MEAS:FRES?')
        return float(fres)

    def res(self):
        res = self.device.query('MEAS:RES?')
        return float(res)