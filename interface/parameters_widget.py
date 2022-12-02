from PyQt6.QtWidgets import (QWidget, QTabWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy,
                            QGroupBox, QCheckBox, QPushButton, QTextEdit)
from PyQt6.QtGui import QDoubleValidator, QIntValidator, QFont
from PyQt6.QtCore import Qt, QLocale, pyqtSlot

class ParametersWidget(QTabWidget):
    def __init__(self, parameters):
        super().__init__()
        
        self.info_page    = ParametersInfoPage(parameters)
        self.scan_page    = ParametersScanPage(parameters)
        self.control_page = MeasurementControlPage(parameters)
        
        self.addTab(self.info_page, "Info")
        self.addTab(self.scan_page, "Scan")
        self.addTab(self.control_page, "Control")
        
        self.control_page.set_button.toggled.connect(lambda state: self.info_page.setEnabled(not state))
        self.control_page.set_button.toggled.connect(lambda state: self.scan_page.setEnabled(not state))
        
        
class MeasurementControlPage(QWidget):
    BUTTON_WIDTH = 100

    def __init__(self, parameters):
        super().__init__()
        
        self.parameters   = parameters
        self.repeat       = EntryWidget(self.parameters.unsavable.repeat, IntValidator, 30)
        self.set_button   = QPushButton("Set")
        self.start_button = QPushButton("Start")
        self.text_area    = QTextEdit()
        
        self.set_button.setFixedWidth(self.BUTTON_WIDTH)
        self.start_button.setFixedWidth(self.BUTTON_WIDTH)
        
        self.set_button.setCheckable(True)
        self.start_button.setCheckable(True)
        
        self.start_button.setEnabled(False)
        
        self.text_area.setReadOnly(True)
        self.text_area.setCurrentFont(QFont("Consolas", 10))
        
        self._configSlots()
        
        control_group = self._createControlGroup()
        
        layout = QVBoxLayout(self)
        layout.addWidget(control_group)
        layout.addWidget(self.text_area)
        
    def _configSlots(self):
        self.set_button.toggled.connect(lambda state: self._setCommand(state))
        self.start_button.toggled.connect(lambda state: self._startCommand(state))
        
    def _createControlGroup(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(self.repeat)
        layout.addSpacing(self.BUTTON_WIDTH)
        layout.addWidget(self.set_button)
        layout.addWidget(self.start_button)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        return widget
        
    pyqtSlot()
    def _setCommand(self, state):
        self.repeat.setEnabled(not state)
        self.start_button.setEnabled(state)
        if state:
            self.set_button.setText("Unset")
            self.parameters.save_preset()
            self.text_area.append(repr(self.parameters.table))
        else:
            self.set_button.setText("Set")
            self.text_area.clear()
    pyqtSlot()
    def _startCommand(self, state):
        self.set_button.setEnabled(not state)
        if state:
            self.start_button.setText("Stop")
        else:
            self.start_button.setText("Start")
            self.set_button.setChecked(False)
        
        
class ParametersInfoPage(QWidget):
    def __init__(self, parameters):
        super().__init__()
        
        p = parameters.info
        
        setup  = EntryWidget(p.setup)
        rh     = EntryWidget(p.rh)
        emit   = EntryWidget(p.emit)
        detec  = EntryWidget(p.detec)
        pcapow = EntryWidget(p.pcapow)
        vbias  = EntryWidget(p.vbias)
        pmppow = EntryWidget(p.pmppow)
        pmppol = EntryWidget(p.pmppol)
        pols   = EntryWidget(p.pols, ENTRY_WIDTH=340)
        sample = EntryWidget(p.sample, ENTRY_WIDTH=340)
        obs    = EntryWidget(p.obs, ENTRY_WIDTH=340)
        
        layout = QGridLayout(self)
        layout.addWidget(setup, 0, 0)
        layout.addWidget(rh, 0, 1)
        layout.addWidget(emit, 1, 0)
        layout.addWidget(detec, 1, 1)
        layout.addWidget(vbias, 2, 0)
        layout.addWidget(pcapow, 2, 1)
        layout.addWidget(pmppol, 3, 0)
        layout.addWidget(pmppow, 3, 1)
        layout.addWidget(pols, 4, 0, 1, 2)
        layout.addWidget(sample, 5, 0, 1, 2)
        layout.addWidget(obs, 6, 0, 1, 2)
        
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)  


class ParametersScanPage(QWidget):
    ENTRY_WIDTH = 80

    def __init__(self, parameters):
        super().__init__()
        
        p = parameters.mandatory
    
        thz_start = EntryWidget(p.thz_start, DoubleValidator, self.ENTRY_WIDTH)
        thz_end   = EntryWidget(p.thz_end, DoubleValidator, self.ENTRY_WIDTH)
        thz_vel   = EntryWidget(p.thz_vel, DoubleValidator, self.ENTRY_WIDTH)
        thz_step  = EntryWidget(p.thz_step, DoubleValidator, self.ENTRY_WIDTH)
        pmp_start = EntryWidget(p.pmp_start, DoubleValidator, self.ENTRY_WIDTH)
        pmp_end   = EntryWidget(p.pmp_end, DoubleValidator, self.ENTRY_WIDTH)
        pmp_vel   = EntryWidget(p.pmp_vel, DoubleValidator, self.ENTRY_WIDTH)
        pmp_step  = EntryWidget(p.pmp_step, DoubleValidator, self.ENTRY_WIDTH)
        thz_fixed = CheckBoxWidget(p.thz_fixed)
        pmp_fixed = CheckBoxWidget(p.pmp_fixed)
        wait      = EntryWidget(p.wait, DoubleValidator, self.ENTRY_WIDTH)
        plot_rate = EntryWidget(p.plot_rate, IntValidator, self.ENTRY_WIDTH)
        
        thz_group   = self._createVGroup("THz delay-line", thz_start, thz_end, thz_vel, thz_step, thz_fixed)
        pmp_group   = self._createVGroup("Pump delay-line", pmp_start, pmp_end, pmp_vel, pmp_step, pmp_fixed)
        other_group = self._createHGroup("Other configs", wait, plot_rate)
        
        thz_fixed.toggled.connect(lambda state: self._fixCommand(state, thz_end))
        pmp_fixed.toggled.connect(lambda state: self._fixCommand(state, pmp_end))
        
        layout = QGridLayout(self)
        layout.addWidget(thz_group, 0, 0)
        layout.addWidget(pmp_group, 0, 1)
        layout.addWidget(other_group, 1, 0, 1, 2)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)        
        
    def _createVGroup(self, name, *items):
        group = QGroupBox(name)
        layout = QVBoxLayout(group)
        for item in items:
            layout.addWidget(item)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        return group
        
    def _createHGroup(self, name, *items):
        group = QGroupBox(name)
        layout = QHBoxLayout(group)
        for item in items:
            layout.addWidget(item)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        return group
        
    @pyqtSlot()
    def _fixCommand(self, state, entry_widget):
        entry_widget.entry.setReadOnly(state)
        if state:
            entry_widget.entry.setText("")


class EntryWidget(QWidget):
    LABEL_WIDTH      = 80
    UNIT_WIDTH       = 40
    CONTENTS_MARGINS = 0, 5, 0, 0
    
    def __init__(self, param, Validator=None, ENTRY_WIDTH=100):
        super().__init__()
        
        self.ENTRY_WIDTH = ENTRY_WIDTH
        
        self.param = param
        self.label = QLabel(f"{self.param.name}:")
        self.entry = QLineEdit()
        self.unit  = QLabel(self.param.unit)
        
        self.label.setFixedWidth(self.LABEL_WIDTH)
        self.entry.setFixedWidth(self.ENTRY_WIDTH)
        self.unit.setFixedWidth(self.UNIT_WIDTH)
        
        self.entry.setText(self.param.value)
        
        self.entry.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.entry.textChanged.connect(self.setValueToParam)
        
        if Validator:
            self.entry.setValidator(Validator(self.param.min_value, self.param.max_value))
        
        layout = QHBoxLayout(self)
        for item in (self.label, self.entry, self.unit):
            layout.addWidget(item)
            
        layout.setContentsMargins(*self.CONTENTS_MARGINS)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        
    @pyqtSlot()
    def setValueToParam(self):
        if self.entry.hasAcceptableInput():
            self.param.setValue(self.entry.text())
        else:
            self.param.setValue("")
            
            
class CheckBoxWidget(QCheckBox):
    def __init__(self, param):
        super().__init__()
        
        self.param = param
        self.setText(self.param.name)
        self.toggled.connect(lambda state: self.setValueToParam(state))
    
    @pyqtSlot()
    def setValueToParam(self, state):
        self.param.setValue(state)
            
            
class DoubleValidator(QDoubleValidator):
    def __init__(self, min_value, max_value):
        super().__init__()
        
        locale = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
        self.setLocale(locale)
        self.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.setBottom(min_value)
        self.setTop(max_value)
        
        
class IntValidator(QIntValidator):
    def __init__(self, min_value, max_value):
        super().__init__()
        
        locale = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
        self.setLocale(locale)
        self.setBottom(min_value)
        self.setTop(max_value)
        
        