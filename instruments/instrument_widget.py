from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QComboBox, QHBoxLayout
from pyvisa import ResourceManager

class InstrumentWidget(QWidget):
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
            if self.instrument.instr:
                self.combo.setEnabled(False)
                self.button.setText("Disconnect")
                self.instrument.savePresetAddress()
                
        elif self.button.text() == "Disconnect":
            self.instrument.disconnect()
            if not self.instrument.instr:
                self.combo.setEnabled(True)
                self.button.setText("Connect")
