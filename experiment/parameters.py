from pandas import DataFrame, read_table


class Parameters:
    def __init__(self):
        self.hidden    = HiddenParams()
        self.mandatory = MandatoryParams()
        self.info      = InfoParams()
        
        
class ParamGroup:
    @property
    def dictionary(self): return self.__dict__
    @property
    def table(self):
        table_ = DataFrame()
        for param in self.dictionary:
            df = self.dictionary[param].table
            df.index = [param]
            table_ = table_.append(df)
        return table_
        
    def load(self, folder, file):
        df = read_table(f'{folder}/{file}', index_col=0).fillna('')
        for param in self.dictionary:
            if param in df.index:
                self.dictionary[param].set_value(df['value'][param])
                

class HiddenParams(ParamGroup):
    def __init__(self):
        self.sens  = Param("Sensitivity", "nA")
        self.tcons = Param("Time constant", "s")
        self.freq  = Param("THz chopper freq", "Hz")
        self.temp  = Param("Temperature", "K")
        

class MandatoryParams(ParamGroup):
    def __init__(self):
        self.thz_start = Param("Start", "mm")
        self.thz_end   = Param("End", "mm")
        self.thz_vel   = Param("Velocity", "mm/s")
        self.thz_step  = Param("Step size", "mm")
        self.thz_fixed = Param("Fixed")
        self.pmp_start = Param("Start", "mm")
        self.pmp_end   = Param("End", "mm")
        self.pmp_vel   = Param("Velocity", "mm/s")
        self.pmp_step  = Param("Step size", "mm")
        self.pmp_fixed = Param("Fixed")
        self.wait      = Param("Wait time", "tcons")
        
        
class InfoParams(ParamGroup):
    def __init__(self):
        self.setup  = Param("Setup no.")
        self.rh     = Param("Humidity", "%")
        self.emit   = Param("Emitter")
        self.detec  = Param("Detector")
        self.pols   = Param("Polarizers")
        self.sample = Param("Sample")
        self.obs    = Param("Obs")
        
    
class Param:
    def __init__(self, name, unit="", value=""):
        self._name  = name
        self._unit  = unit
        self._value = value
        
    def __repr__(self):
        return f"Parameter {self.name} @ {self.value}{self.unit}"
        
    @property
    def name(self): return self._name
    @property
    def unit(self): return self._unit
    @property
    def value(self): return self._value
    @property
    def table(self):
        return DataFrame({'name': self.name, 'value': self.value, 'unit': self.unit}, index=[0])
        
    def setValue(self, value):
        self._value = value