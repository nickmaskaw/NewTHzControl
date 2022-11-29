from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtCore import Qt, QLocale, pyqtSlot


class ConnectionContainer(QWidget):
    def __init__(self, lockin, cernox, pmp_dl, thz_dl):
        super().__init__()
        
        layout = QVBoxLayout(self)
        for instr in (lockin, cernox, pmp_dl, thz_dl): 
            layout.addWidget(InstrumentConnectionWidget(instr))
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        
class ControlContainer(QWidget):
    def __init__(self, pmp_dl, thz_dl):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.addWidget(DelaylineControlWidget(pmp_dl))
        layout.addWidget(DelaylineControlWidget(thz_dl))
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)


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
        
        self._configLabel()
        self._configCombo()
        self._configButton()
        self._configLayout()
        self._configSlots()
        
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
    
    def _configLabel(self):
        self.label.setText(f"{self.instrument.name}:")
        self.label.setFixedWidth(self.LABEL_FIXED_WIDTH)
        
    def _configCombo(self):
        self.combo.addItems(self.instrument.addressList())
        self.combo.setEditable(True)
        self.combo.setCurrentText(self.instrument.loadPresetAddress())
        
    def _configButton(self):
        self.button.setText("Connect")
        self.button.setFixedWidth(self.BUTTON_FIXED_WIDTH)
        self.button.clicked.connect(self._buttonClicked)
        
    def _configLayout(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.button)
        self.layout.setContentsMargins(*self.CONTENTS_MARGINS)
        
    def _configSlots(self):
        self.instrument.signals.connected.connect(self._instrumentConnected)
        self.instrument.signals.disconnected.connect(self._instrumentDisconnected)
       
    @pyqtSlot()
    def _buttonClicked(self):
        if self.button.text() == "Connect":
            self.instrument.setAddress(self.combo.currentText())
            self.instrument.connect()
        elif self.button.text() == "Disconnect":
            self.instrument.disconnect()
       
    @pyqtSlot()
    def _instrumentConnected(self):
        self.combo.setEnabled(False)
        self.button.setText("Disconnect")
        self.instrument.savePresetAddress()
        
    @pyqtSlot()
    def _instrumentDisconnected(self):
        self.combo.setEnabled(True)
        self.button.setText("Connect")
        
        
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
        
        self._configLabel()
        self._configEntry()
        self._configButton()
        self._configLayout()
        self._configSlots()
        
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
    
    def _configLabel(self):
        self.label.setText(f"{self.instrument.name}:")
        self.label.setFixedWidth(self.LABEL_FIXED_WIDTH)
        
    def _configEntry(self):
        validator = QDoubleValidator()
        locale = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
        validator.setLocale(locale)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setBottom(self.instrument.MINIMUM_POSITION)
        validator.setTop(self.instrument.MAXIMUM_POSITION)
        
        self.entry.setValidator(validator)
        self.entry.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.entry.returnPressed.connect(self._buttonSetClicked)
        
    def _configButton(self):
        self.button_get.setText("Get")
        self.button_set.setText("Set")
        self.button_get.setFixedWidth(self.BUTTON_FIXED_WIDTH)
        self.button_set.setFixedWidth(self.BUTTON_FIXED_WIDTH)
        self.button_get.clicked.connect(self._buttonGetClicked)
        self.button_set.clicked.connect(self._buttonSetClicked)
        
    def _configLayout(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.button_get)
        self.layout.addWidget(self.button_set)
        self.layout.setContentsMargins(*self.CONTENTS_MARGINS)
        
    def _configSlots(self):
        self.instrument.signals.connected.connect(self._instrumentConnected)
        self.instrument.signals.disconnected.connect(self._instrumentDisconnected)
        
    @pyqtSlot()
    def _buttonGetClicked(self):
        try:
            self.entry.setText(str(self.instrument.currentPosition()))
        except:
            print(f"Could not retrieve the {self.instrument.name} current position")
        
    @pyqtSlot()
    def _buttonSetClicked(self):
        if self.entry.hasAcceptableInput():
            position = float(self.entry.text())
            try:
                self.instrument.returnTo(position)
                print(f"{self.instrument.name} returned to {position}mm")
            except:
                print(f"Could not return the {self.instrument.name} to {position}mm")
        else:
            print(f"Out of {self.instrument.name} range ({self.instrument.MINIMUM_POSITION} to {self.instrument.MAXIMUM_POSITION}mm)")
                
    @pyqtSlot()
    def _instrumentConnected(self):
        self.setEnabled(True)
        
    @pyqtSlot()
    def _instrumentDisconnected(self):
        self.combo.setEnabled(False)