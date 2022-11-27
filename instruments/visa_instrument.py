import os
from pyvisa import ResourceManager
from instruments import InstrumentConnectionWidget

class VISAInstrument:
    PRESET_FOLDER = './preset'

    def __init__(self, name):
        self._name    = name
        self._address = None
        self._instr   = None
        self._widget  = InstrumentConnectionWidget(self)
        self._control = None
        
    @property
    def name(self): return self._name
    @property
    def address(self): return self._address
    @property
    def instr(self): return self._instr
    @property
    def widget(self): return self._widget
    @property
    def control(self): return self._control
    @property
    def idn(self): return ""
    
    def isConnected(self):
        return True if self.instr else False
    
    def connect(self):
        rm = ResourceManager()
        if self.address:
            try:
                self._instr = rm.open_resource(self.address)
                print(f"Connected the {self.name}: {self.idn} ({self.instr})")
            except:
                print(f"Failed to connect the {self.name} ({self.address})")
        else:
            print(f"Failed to connect the {self.name}. You must specify an address within:\n{rm.list_resources()}")
            
    def disconnect(self):
        try:
            self.instr.close()
            print(f"Disconnected the {self.name} ({self.instr})")
            self._instr = None
        except:
            print(f"Failed to disconnect the {self.name} ({self.instr})")
            
    def setAddress(self, address):
        self._address = address
        
    def addressList(self):
        rm = ResourceManager()
        return rm.list_resources()
                
    def loadPresetAddress(self):
        preset_address = ""
        try:
            with open(f'{self.PRESET_FOLDER}/{self.name}_address') as file:
                preset_address = file.readlines()[0]
            print(f"Loaded {self.name} preset address")
        except:
            print(f"No {self.name} address found in the preset folder")
        finally:
            return preset_address
            
    def savePresetAddress(self):
        if not os.path.exists(self.PRESET_FOLDER): os.makedirs(self.PRESET_FOLDER)
        try:
            with open(f'{self.PRESET_FOLDER}/{self.name}_address', 'w') as file:
                file.write(self.address)
            print(f"Saved {self.name} current address ({self.address}) to preset folder")
        except:
            print(f"Failed to save {self.name} current address to preset folder")