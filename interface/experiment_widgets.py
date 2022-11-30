from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QCheckBox, QGroupBox
from PyQt6.QtCore import Qt, pyqtSlot


class ExperimentWidgets:
    def __init__(self, parameters):
        self.parameters = ParametersContainer(parameters)


class ParametersContainer(QWidget):
    def __init__(self, parameters):   
        super().__init__()
        
        thz_group = ScanGroupWidget("THz Scan", *self._thzGroupParams(parameters))
        pmp_group = ScanGroupWidget("Pump Scan", *self._pmpGroupParams(parameters)) 
        
        layout = QVBoxLayout(self)
        for widget in (thz_group, pmp_group):
            layout.addWidget(widget)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def _thzGroupParams(self, parameters):
        tags   = ("thz_start", "thz_end", "thz_vel", "thz_step", "thz_fixed")
        return (parameters.mandatory.dictionary[tag] for tag in tags)
        
    def _pmpGroupParams(self, parameters):
        tags   = ("pmp_start", "pmp_end", "pmp_vel", "pmp_step", "pmp_fixed")
        return (parameters.mandatory.dictionary[tag] for tag in tags)
        
        
#class InfoGroupWidget(QGroupBox):
#    def __init__(self, 

class ScanGroupWidget(QGroupBox):
    def __init__(self, name, start_param, end_param, vel_param, step_param, fixed_param):
        super().__init__()
    
        start_entry = EntryWidget(start_param)
        end_entry   = EntryWidget(end_param)
        vel_entry   = EntryWidget(vel_param)
        step_entry  = EntryWidget(step_param)
        fixed_check = CheckWidget(fixed_param)
        
        layout = QGridLayout(self)
        layout.addWidget(start_entry, 0, 0)
        layout.addWidget(end_entry, 0, 1)
        layout.addWidget(fixed_check, 0, 2)
        layout.addWidget(vel_entry, 1, 0)
        layout.addWidget(step_entry, 1, 1)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.setTitle(name)


class CheckWidget(QCheckBox):
    def __init__(self, param):
        super().__init__()
        
        self.param = param
        self.setText(self.param.name)
        self.stateChanged.connect(lambda state: self.setValueToParam(state))
        
    @pyqtSlot()
    def setValueToParam(self, state):
        self.param.setValue(state)
        

class EntryWidget(QWidget):
    LABEL_WIDTH = 60
    UNIT_WIDTH  = 40
    ENTRY_WIDTH = 60
    CONTENTS_MARGINS = 0, 5, 0, 0

    def __init__(self, param, validator=None):
        super().__init__()
        
        self.param = param
        self.label = QLabel()
        self.entry = QLineEdit()
        self.unit  = QLabel()
        
        self._configLabels()
        self._configEntry(validator)
        
        layout = QHBoxLayout(self)
        for widget in (self.label, self.entry, self.unit):
            layout.addWidget(widget)
            
        layout.setContentsMargins(*self.CONTENTS_MARGINS)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.entry.editingFinished.connect(self.setValueToParam)

    def _configLabels(self):
        self.label.setText(f"{self.param.name}:")
        self.unit.setText(f"{self.param.unit}")
        self.label.setFixedWidth(self.LABEL_WIDTH)
        self.unit.setFixedWidth(self.UNIT_WIDTH)
        
    def _configEntry(self, validator):
        if validator: self.entry.setValidator(validator)        
        self.entry.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.entry.setFixedWidth(self.ENTRY_WIDTH)
        
    @pyqtSlot()
    def setValueToParam(self):
        if self.entry.hasAcceptableInput():
            self.param.setValue(self.entry.text())
        else:
            self.param.setValue("")
        

class ControlButtons(QWidget):
    BUTTON_WIDTH     = 100
    CONTENTS_MARGINS = 0, 5, 0, 0
    
    def __init__(self):
        self.set_button   = QPushButton("Set")
        self.start_button = QPushButton("Start")
        self.stop_button  = QPushButton("Stop")
        
        layout = QHBoxLayout(self)
        for button in (self.set_button, self.start_button, self.stop_button):
            button.setFixedWidth(self.BUTTON_WIDTH)
            layout.addWidget(button)
        
        layout.setContentsMargins(*self.CONTENTS_MARGINS)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        