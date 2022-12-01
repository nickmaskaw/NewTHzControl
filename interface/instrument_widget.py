from PyQt6.QtWidgets import QWidget, QTabWidget, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import Qt, QLocale, pyqtSlot


class InstrumentWidget(QTabWidget):
    def __init__(self, lockin, cernox, thz_dl, pmp_dl):
        super().__init__()
        
        self.connection_page = InstrumentConnectionContainer(lockin, cernox, thz_dl, pmp_dl)
        self.controller_page = InstrumentControllerContainer(lockin, cernox, thz_dl, pmp_dl)
        
        self.addTab(self.connection_page, "Connections")
        self.addTab(self.controller_page, "Controllers")
        

class InstrumentConnectionContainer(QWidget):
    def __init__(self, lockin, cernox, thz_dl, pmp_dl):
        super().__init__()
        
        layout = QVBoxLayout(self)
        for instr in (lockin, cernox, thz_dl, pmp_dl):
            layout.addWidget(InstrumentConnectionWidget(instr))
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        
class InstrumentControllerContainer(QWidget):
    def __init__(self, lockin, cernox, thz_dl, pmp_dl):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.addWidget(LockinControllerWidget(lockin))
        layout.addWidget(CernoxControllerWidget(cernox))
        layout.addWidget(KBD101ControllerWidget(thz_dl))
        layout.addWidget(OttimeControllerWidget(pmp_dl))
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)        

        
class InstrumentConnectionWidget(QWidget):
    LABEL_WIDTH      = 100
    COMBO_WIDTH      = 280
    BUTTON_WIDTH     = 80
    CONTENTS_MARGINS = 0, 5, 0, 0
    
    def __init__(self, instrument):
        super().__init__()
        
        self.instrument = instrument
        self.label      = QLabel(f"{self.instrument.name}:")
        self.combo      = QComboBox()
        self.button     = QPushButton("Connect")
        
        self.label.setFixedWidth(self.LABEL_WIDTH)
        self.combo.setFixedWidth(self.COMBO_WIDTH)
        self.button.setFixedWidth(self.BUTTON_WIDTH)
        
        self._initCombo()
        self._configSlots()
        
        layout = QHBoxLayout(self)
        for item in (self.label, self.combo, self.button):
            layout.addWidget(item)
        
        layout.setContentsMargins(*self.CONTENTS_MARGINS)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
    def _initCombo(self):
        self.combo.addItems(self.instrument.addressList())
        self.combo.setEditable(True)
        self.combo.setCurrentText(self.instrument.loadPresetAddress())
        self.instrument.setAddress(self.combo.currentText())
        
    def _configSlots(self):
        self.instrument.signals.connected.connect(self._instrumentConnected)
        self.instrument.signals.disconnected.connect(self._instrumentDisconnected)
        self.combo.currentTextChanged.connect(lambda address: self._setInstrumentAddress(address))
        self.button.clicked.connect(self._buttonClicked)
        
    @pyqtSlot()
    def _instrumentConnected(self):
        self.combo.setEnabled(False)
        self.button.setText("Disconnect")
        self.instrument.savePresetAddress()
    @pyqtSlot()
    def _instrumentDisconnected(self):
        self.combo.setEnabled(True)
        self.button.setText("Connect")
    @pyqtSlot()
    def _setInstrumentAddress(self, address):
        self.instrument.setAddress(address)
    @pyqtSlot()
    def _buttonClicked(self):
        if self.button.text() == "Connect":
            self.instrument.connect()
        elif self.button.text() == "Disconnect":
            self.instrument.disconnect()
            
            
class GeneralControllerWidget(QWidget):
    LABEL_WIDTH  = 100
    ENTRY_WIDTH  = 150
    BUTTON_WIDTH = 80
    COMBO_WIDTH  = 80
    CONTENTS_MARGINS = 0, 5, 0, 0
    
    def __init__(self, instrument):
        super().__init__()
        
        self.instrument = instrument
        self.label      = QLabel(f"{self.instrument.name}:")
        self.entry      = QLineEdit()
        
        self.label.setFixedWidth(self.LABEL_WIDTH)
        self.entry.setFixedWidth(self.ENTRY_WIDTH)
        self.entry.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        self.__configSlots()
        
        layout = QHBoxLayout(self)
        for item in (self.label, self.entry):
            layout.addWidget(item)
            
        layout.setContentsMargins(*self.CONTENTS_MARGINS)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.setEnabled(False)
        
    def __configSlots(self):
        self.instrument.signals.connected.connect(self._instrumentConnected)
        self.instrument.signals.disconnected.connect(self._instrumentDisconnected)
    
    @pyqtSlot()
    def _instrumentConnected(self):
        self.setEnabled(True)
    @pyqtSlot()
    def _instrumentDisconnected(self):
        self.setEnabled(False)
        
        
class DelaylineValidator(QDoubleValidator):
    def __init__(self, minimum_position, maximum_position):
        super().__init__()
        
        locale = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
        self.setLocale(locale)
        self.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.setBottom(minimum_position)
        self.setTop(maximum_position)
        
        
class KBD101ControllerWidget(GeneralControllerWidget):
    def __init__(self, instrument):
        super().__init__(instrument)
        
        self.get_button = QPushButton("Get")
        self.set_button = QPushButton("Set")
        
        self._configEntry()
        self._configSlots()
        
        for item in (self.get_button, self.set_button):
            item.setFixedWidth(self.BUTTON_WIDTH)
            self.layout().addWidget(item)
            
    def _configEntry(self):
        min_pos, max_pos = self.instrument.MINIMUM_POSITION, self.instrument.MAXIMUM_POSITION
        self.entry.setValidator(DelaylineValidator(min_pos, max_pos))
        
    def _configSlots(self):
        self.get_button.clicked.connect(self._getPosition)
        self.set_button.clicked.connect(self._setPosition)
        self.entry.returnPressed.connect(self._setPosition)
        
    @pyqtSlot()
    def _getPosition(self):
        try:
            self.entry.setText(str(self.instrument.currentPosition()))
        except:
            print(f"Could not retrieve the {self.instrument.name} current position")
    @pyqtSlot()
    def _setPosition(self):
        if self.entry.hasAcceptableInput():
            position = float(self.entry.text())
            try:
                self.instrument.returnTo(position)
                print(f"{self.instrument.name} returned to {position}mm")
            except:
                print(f"Could not return the {self.instrument.name} to {position}mm")
        else:
            print(f"Out of {self.instrument.name} range({self.instrument.MINIMUM_POSITION} to {self.instrument.MAXIMUM_POSITION}mm)")
            
            
class OttimeControllerWidget(GeneralControllerWidget):
    def __init__(self, instrument):
        super().__init__(instrument)
        
        self.home_button = QPushButton("Home")
        self.set_button  = QPushButton("Set")
        
        self._configEntry()
        self._configSlots()
        
        for item in (self.home_button, self.set_button):
            item.setFixedWidth(self.BUTTON_WIDTH)
            self.layout().addWidget(item)
            
    def _configEntry(self):
        min_pos, max_pos = self.instrument.MINIMUM_POSITION, self.instrument.MAXIMUM_POSITION
        self.entry.setValidator(DelaylineValidator(min_pos, max_pos))
        
    def _configSlots(self):
        self.home_button.clicked.connect(self._findHome)
        self.set_button.clicked.connect(self._setPosition)
        self.entry.returnPressed.connect(self._setPosition)
        
    @pyqtSlot()
    def _findHome(self):
        try:
            self.instrument.home()
            print(f"{self.instrument.name} found the home")
        except:
            print(f"Could not home the {self.instrument.name}")
    @pyqtSlot()
    def _setPosition(self):
        if self.entry.hasAcceptableInput():
            position = float(self.entry.text())
            try:
                self.instrument.returnTo(position)
                print(f"{self.instrument.name} returned to {position}mm")
            except:
                print(f"Could not return the {self.instrument.name} to {position}mm")
        else:
            print(f"Out of {self.instrument.name} range({self.instrument.MINIMUM_POSITION} to {self.instrument.MAXIMUM_POSITION}mm)")
            
            
class CernoxControllerWidget(GeneralControllerWidget):
    def __init__(self, instrument):
        super().__init__(instrument)
        
        self.button = QPushButton("Get")
        self.button.setFixedWidth(self.BUTTON_WIDTH)
        self.button.clicked.connect(self._getTemperature)
        
        self.layout().addWidget(self.button)
        
    @pyqtSlot()
    def _getTemperature(self):
        try:
            self.entry.setText(str(self.instrument.temperature()))
        except:
            print(f"Could not retrieve the {self.instrument.name} current temperature")


class LockinControllerWidget(GeneralControllerWidget):
    def __init__(self, instrument):
        super().__init__(instrument)
        
        self.combo  = QComboBox()
        self.button = QPushButton("Get")
        
        self.combo.setFixedWidth(self.COMBO_WIDTH)
        self.combo.addItems(("X", "Y", "phase", "freq", "sens", "tcons"))
        
        self.button.setFixedWidth(self.BUTTON_WIDTH)        
        self.button.clicked.connect(self._getValue)
        
        for item in (self.combo, self.button):
            self.layout().addWidget(item)
            
    def _getValue(self):
        prop = self.combo.currentText()
        
        if prop == "X":
            fn = self.instrument.X
        elif prop == "Y":
            fn = self.instrument.Y
        elif prop == "phase":
            fn = self.instrument.phase
        elif prop == "freq":
            fn = self.instrument.freq
        elif prop == "sens":
            fn = self.instrument.sens
        elif prop == "tcons":
            fn = self.instrument.tcons
                
        try:
            self.entry.setText(str(fn()))
        except:
            print(f"Could not retrieve the {self.instrument.name} {prop}")
            