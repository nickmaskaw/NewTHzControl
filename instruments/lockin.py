from instruments import VISAInstrument


class LockIn(VISAInstrument):
    # first col: lock-in index; second col: values in nA (or mV)
    SENS_LIST = {
        '17': 1,
        '18': 2,
        '19': 5,
        '20': 10,
        '21': 20,
        '22': 50,
        '23': 100,
        '24': 200,
        '25': 500,
        '26': 1000
    }

    # first col: lock-in index; second col: values in s
    TCONS_LIST = {
        '0':  10e-6,
        '1':  30e-6,
        '2':  100e-6,
        '3':  300e-6,
        '4':  1e-3,
        '5':  3e-3,
        '6':  10e-3,
        '7':  30e-3,
        '8':  100e-3,
        '9':  300e-3,
        '10': 1,
        '11': 3,
        '12': 10,
        '13': 30,
        '14': 100,
        '15': 300,
        '16': 1e3,
        '17': 3e3,
        '18': 10e3,
        '19': 30e3
    }

    def __init__(self, name="Lock-in"):
        super().__init__(name)
        
    @property
    def idn(self): return self.device.query('*IDN?')

    def XY(self):
        X, Y = self.device.query('SNAP?1,2').split(',')
        return float(X), float(Y)

    def X(self):
        X = self.device.query('OUTP?1')
        return float(X)

    def Y(self):
        Y = self.device.query('OUTP?2')
        return float(Y)

    def phase(self):
        phase = self.device.query('PHAS?')
        return float(phase)

    def freq(self):
        freq = self.device.query('FREQ?')
        return float(freq)

    def sens(self):
        """ Returns 0 if sensitivity out of range """
        i = self.device.query('SENS?')
        return self.SENS_LIST[i] if i in self.SENS_LIST else 0

    def tcons(self):
        i = self.device.query('OFLT?')
        return self.TCONS_LIST[i]
    