from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QLineEdit, QHBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import Qt, QLocale
from pyvisa import ResourceManager


class InstrumentConnectionWidget(QWidget):
    LABEL_FIXED_WIDTH  = 100
    BUTTON_FIXED_WIDTH = 80
    CONTENTS_MARGINS   = 0, 5, 0, 0
    
    def __init__(self, instrument):
        super().__init__()
        
        self._instrument = instrument
        self._label  = QLabel()
        self._combo  = QComboBox()
        self._button = QPushButton()
        self._layout = QHBoxLayout(self)
        
        self._labelConfig()
        self._comboConfig()
        self._buttonConfig()
        self._layoutConfig()
        
    @property
    def instrument(self): return self._instrument
    @property
    def label(self): return self._label
    @property
    def combo(self): return self._combo
    @property
    def button(self): return self._button
    @property
    def layout(self): return self._layout
    
    def _labelConfig(self):
        self.label.setText(f"{self.instrument.name}:")
        self.label.setFixedWidth(self.LABEL_FIXED_WIDTH)
        
    def _comboConfig(self):
        rm = ResourceManager()
        self.combo.addItems(self.instrument.addressList())
        self.combo.setEditable(True)
        self.combo.setCurrentText(self.instrument.loadPresetAddress())
        
    def _buttonConfig(self):
        self.button.setText("Connect")
        self.button.setFixedWidth(self.BUTTON_FIXED_WIDTH)
        self.button.clicked.connect(self._buttonClicked)
        
    def _layoutConfig(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.button)
        self.layout.setContentsMargins(*self.CONTENTS_MARGINS)
        
    def _buttonClicked(self):
        if self.button.text() == "Connect":
            self.instrument.setAddress(self.combo.currentText())
            self.instrument.connect()
            if self.instrument.isConnected():
                self.combo.setEnabled(False)
                self.button.setText("Disconnect")
                self.instrument.control.setEnabled(True)
                self.instrument.savePresetAddress()
                
        elif self.button.text() == "Disconnect":
            self.instrument.disconnect()
            if not self.instrument.isConnected():
                self.combo.setEnabled(True)
                self.button.setText("Connect")
                self.instrument.control.setEnabled(False)


class DelaylineControlWidget(QWidget):
    LABEL_FIXED_WIDTH  = 100
    BUTTON_FIXED_WIDTH = 40
    CONTENTS_MARGINS   = 0, 5, 0, 0
    
    def __init__(self, instrument):
        super().__init__()
        
        self._instrument = instrument
        self._label      = QLabel()
        self._entry      = QLineEdit()
        self._button_get = QPushButton()
        self._button_set = QPushButton()
        self._layout     = QHBoxLayout(self)        
        
        self._labelConfig()
        self._entryConfig()
        self._buttonConfig()
        self._layoutConfig()
        
        self.setEnabled(False)
        
    @property
    def instrument(self): return self._instrument
    @property
    def label(self): return self._label
    @property
    def entry(self): return self._entry
    @property
    def button_get(self): return self._button_get
    @property
    def button_set(self): return self._button_set
    @property
    def layout(self): return self._layout
    
    def _labelConfig(self):
        self.label.setText(f"{self.instrument.name}:")
        self.label.setFixedWidth(self.LABEL_FIXED_WIDTH)
        
    def _buttonConfig(self):
        self.button_get.setText("Get")
        self.button_set.setText("Set")
        self.button_get.setFixedWidth(self.BUTTON_FIXED_WIDTH)
        self.button_set.setFixedWidth(self.BUTTON_FIXED_WIDTH)
        self.button_get.clicked.connect(self._getCommand)
        self.button_set.clicked.connect(self._setCommand)
        
    def _entryConfig(self):
        validator = QDoubleValidator()
        locale = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
        validator.setLocale(locale)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setBottom(self.instrument.MINIMUM_POSITION)
        validator.setTop(self.instrument.MAXIMUM_POSITION)
        
        self.entry.setValidator(validator)
        self.entry.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.entry.returnPressed.connect(self._setCommand)
        
    def _layoutConfig(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.button_get)
        self.layout.addWidget(self.button_set)
        self.layout.setContentsMargins(*self.CONTENTS_MARGINS)
        
    def _setCommand(self):
        if self.entry.hasAcceptableInput():
            position = float(self.entry.text())
            try:
                self.instrument.returnTo(position)
                print(f"{self.instrument.name} returned to {position}mm")
            except:
                print(f"Could not return the {self.instrument.name} to {position}mm")
                
    def _getCommand(self):
        try:
            self.entry.setText(str(self.instrument.currentPosition()))
        except:
            print(f"Could not retrieve the {self.instrument.name} current position")