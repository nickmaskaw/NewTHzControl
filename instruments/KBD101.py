from instruments import InstrumentConnectionWidget, DelaylineControlWidget
import os
import time as tm
import sys
import clr
from System import String
from System import Decimal
from System.Collections import *

if not r'C:\Program Files\Thorlabs\Kinesis' in sys.path:
    sys.path.append(r'C:\Program Files\Thorlabs\Kinesis')
    
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI

clr.AddReference("Thorlabs.MotionControl.KCube.BrushlessMotorCLI")
from Thorlabs.MotionControl.KCube.BrushlessMotorCLI import KCubeBrushlessMotor


class KBD101:
    PRESET_FOLDER = './preset'
    MINIMUM_POSITION = 0.0
    MAXIMUM_POSITION = 100.0

    def __init__(self, name):
        self._name    = name
        self._serial  = None
        self._device  = None
        self._widget  = InstrumentConnectionWidget(self)
        self._control = DelaylineControlWidget(self)
        
    @property
    def name(self): return self._name
    @property
    def serial(self): return self._serial
    @property
    def device(self): return self._device
    @property
    def widget(self): return self._widget
    @property
    def control(self): return self._control
    @property
    def idn(self):
        try:
            device_info = self.device.GetDeviceInfo()
            return f"{device_info.Name} (serial no. {device_info.SerialNumber})"
        except:
            return ""
            
    def isConnected(self):
        return True if self.device else False
    
    def connect(self):
        if isinstance(self.serial, str) and self.serial[:2] == "28":
            if self.serial in self.addressList():
                try:
                    self._device = KCubeBrushlessMotor.CreateKCubeBrushlessMotor(self.serial)
                    self.device.Connect(self.serial)
                    tm.sleep(.2)
                    self.device.LoadMotorConfiguration(self.serial)
                    print(f"Connected the {self.name}: {self.idn}")
                except:
                    self._device = None
                    print(f"Failed to connect the {self.name} ({self.serial})")
            else:
                print(f"Failed to connect the {self.name}. You must specify an address within:\n{list(self.addressList())}")
            
        else:
            print(f"Failed to connect the {self.name}. Check if the intended serial number is a string that begins with '28'")
            
    def disconnect(self):
        try:
            self.device.Disconnect()
            print(f"Disconnected the {self.name} ({self.serial})")
            self._device = None
        except:
            print(f"Failed to disconnect the {self.name} ({self.serial})")
            
    def setAddress(self, serial):
        self._serial = serial
            
    def addressList(self):
        DeviceManagerCLI.BuildDeviceList()
        return DeviceManagerCLI.GetDeviceList()
        
    def loadPresetAddress(self):
        preset_serial = ""
        try:
            with open(f'{self.PRESET_FOLDER}/{self.name}_serial') as file:
                preset_serial = file.readlines()[0]
            print(f"Loaded {self.name} preset serial")
        except:
            print(f"No {self.name} serial found in the preset folder")
        finally:
            return preset_serial
            
    def savePresetAddress(self):
        if not os.path.exists(self.PRESET_FOLDER): os.makedirs(self.PRESET_FOLDER)
        try:
            with open(f'{self.PRESET_FOLDER}/{self.name}_serial', 'w') as file:
                file.write(self.serial)
            print(f"Saved {self.name} current serial ({self.serial}) to preset folder")
        except:
            print(f"Failed to save {self.name} current serial to preset folder")
            
    # DELAY LINE COMMANDS ##################################################################
    def startPolling(self, rate=50):
        self.device.StartPolling(rate)
        
    def stopPolling(self):
        self.device.StopPolling()
        
    def setVelocity(self, velocity, acceleration=999):
        self.device.SetVelocityParams(Decimal(velocity), Decimal(acceleration))
        
    def moveTo(self, position, timeout=60000):
        self.device.MoveTo(Decimal(float(position)), timeout)
        
    def returnTo(self, position, timeout=60000):
        self.setVelocity(100)
        self.moveTo(position, timeout)
        
    def requestPosition(self):
        self.device.RequestPosition()
        
    def getPosition(self):
        position = str(self.device.Position).replace(',', '.')
        return float(position)
        
    def currentPosition(self):
        self.requestPosition()
        return self.getPosition()