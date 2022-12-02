import os
from pandas import DataFrame, read_table, concat


class Parameters:
    PRESET_FOLDER = './preset'
    PRESET_FILE   = 'parameters'
    
    def __init__(self):
        self.hidden    = HiddenParams()
        self.mandatory = MandatoryParams()
        self.info      = InfoParams()
        self.unsavable = UnsavableParams()
        
        self._load_preset()
        
    @property
    def table(self): return concat([self.mandatory.table, self.info.table, self.hidden.table])
    
    def save(self, folder, file):
        self.table.to_csv(f'{folder}/{file}', sep='\t')
        print(f"Saved parameters to {folder}/{file}")
        
    def save_preset(self):
        if not os.path.exists(self.PRESET_FOLDER): os.makerdirs(self.PRESET_FOLDER)
        self.save(self.PRESET_FOLDER, self.PRESET_FILE)
        
    def _load_preset(self):
        try:
            for group in (self.mandatory, self.info, self.hidden):
                group.load(self.PRESET_FOLDER, self.PRESET_FILE)
            print("Loaded preset parameters")
        except:
            print("Could not load preset parameters")
        
        
class ParamGroup:
    @property
    def dictionary(self): return self.__dict__
    @property
    def table(self):
        table_ = DataFrame()
        for param in self.dictionary:
            df = self.dictionary[param].table
            df.index = [param]
            table_ = concat([table_, df])
        return table_
        
    def load(self, folder, file):
        df = read_table(f'{folder}/{file}', index_col=0).fillna('')
        for param in self.dictionary:
            if param in df.index:
                self.dictionary[param].setValue(df['value'][param])
                

class HiddenParams(ParamGroup):
    def __init__(self):
        self.sens  = Param("Sensitivity", "nA")
        self.tcons = Param("Time constant", "s")
        self.freq  = Param("THz chopper freq", "Hz")
        self.temp  = Param("Temperature", "K")
        

class MandatoryParams(ParamGroup):
    def __init__(self):
        self.thz_start = Param("Start", "mm", "", 0.0, 100.0)
        self.thz_end   = Param("End", "mm", "", 0.0, 100.0)
        self.thz_vel   = Param("THz velocity", "mm/s", "", 0.0, 100.0)
        self.thz_step  = Param("Step size", "mm", "", 0.0, 100.0)
        self.thz_fixed = Param("Fix at start position")
        self.pmp_start = Param("Start", "mm", "", 0.0, 200.0)
        self.pmp_end   = Param("End", "mm", "", 0.0, 200.0)
        self.pmp_vel   = Param("Pump velocity", "mm/s", "", 0.0, 100.0)
        self.pmp_step  = Param("Step size", "mm", "", 0.0, 200.0)
        self.pmp_fixed = Param("Fix at start position")
        self.wait      = Param("Wait time", "tcons", "", 0.0, 10.0)
        self.plot_rate = Param("Plot rate", "pts/f", "", 1, 1000)
        
        
class InfoParams(ParamGroup):
    def __init__(self):
        self.setup  = Param("Setup no.")
        self.rh     = Param("Humidity", "%")
        self.emit   = Param("Emitter")
        self.detec  = Param("Detector")
        self.pcapow = Param("PCA power", "mW")
        self.vbias  = Param("V Bias", "V")
        self.pmppow = Param("Pump power", "mW")
        self.pmppol = Param("Pump polariz")
        self.pols   = Param("Polarizers")
        self.sample = Param("Sample")
        self.obs    = Param("Obs")
        
        
class UnsavableParams(ParamGroup):
    def __init__(self):
        self.repeat = Param("Repeat", "x", "1", 1, 1000)
        
    
class Param:
    def __init__(self, name, unit="", value="", min_value=None, max_value=None):
        self._name      = name
        self._unit      = unit
        self._value     = value
        self._min_value = min_value
        self._max_value = max_value
        
    def __repr__(self):
        return f"Parameter {self.name} @ {self.value}{self.unit}"
        
    @property
    def name(self): return self._name
    @property
    def unit(self): return self._unit
    @property
    def value(self): return self._value
    @property
    def min_value(self): return self._min_value
    @property
    def max_value(self): return self._max_value
    @property
    def table(self):
        return DataFrame({'name': self.name, 'value': self.value, 'unit': self.unit}, index=[0])
        
    def setValue(self, value):
        self._value = value