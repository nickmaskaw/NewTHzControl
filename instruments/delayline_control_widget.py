from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout

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
        self._buttonConfig()
        self._layoutConfig()
        
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
        
    def _layoutConfig(self):
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.button_get)
        self.layout.addWidget(self.button_set)
        self.layout.setContentsMargins(*self.CONTENTS_MARGINS)