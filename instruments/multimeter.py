from instruments import VISAInstrument


class Multimeter(VISAInstrument):
    def __init__(self, name="Multimeter"):
        super().__init__(name)

    def volt(self):
        volt = self.instr.query('MEAS?')
        return float(volt)

    def curr(self):
        curr = self.instr.query('MEAS:CURR?')
        return float(curr)

    def fres(self):
        fres = self.instr.query('MEAS:FRES?')
        return float(fres)

    def res(self):
        res = self.instr.query('MEAS:RES?')
        return float(res)