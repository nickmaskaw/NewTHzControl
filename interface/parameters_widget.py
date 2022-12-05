from PyQt6.QtWidgets import QWidget, QTabWidget, QLabel, QLineEdit, QTextEdit, QCheckBox, QPushButton, QGroupBox
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QSizePolicy
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
        
        self.set_button.toggled.connect(lambda state: self.setPagesEnabled(not state))
        self.set_button.toggled.connect(lambda state: self._setParameters(state, parameters))
    
    @property
    def set_button(self): return self.control_page.control_widget.set_button
    @property
    def start_button(self): return self.control_page.control_widget.start_button
    @property
    def stop_button(self): return self.control_page.control_widget.stop_button
    @property
    def text(self): return self.control_page.text
    
    @pyqtSlot()
    def setPagesEnabled(self, state):
        self.info_page.setEnabled(state)
        self.scan_page.setEnabled(state)
    @pyqtSlot()
    def _setParameters(self, state, parameters):
        if state:
            self.text.clear()
            parameters.retrieveHiddenParams()
            
            if parameters.are_valid:
                self.text.append("Parameters are set:")
                self.text.append(repr(parameters.table))
                parameters.savePreset()
            else:
                self.text.append("Missing some mandatory parameters. Re-check the parameters definitions and/or " +
                                 "if the instruments are properly connected to retrieve hidden parameters")
                self.start_button.setEnabled(False)
                
        
        
class MeasurementControlPage(QWidget):
    def __init__(self, parameters):
        super().__init__()
        
        self.control_widget = MeasurementControlWidget(parameters)
        
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setCurrentFont(QFont("Consolas", 10))
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.control_widget)
        layout.addWidget(self.text)

        
        
class ParametersInfoPage(QWidget):
    def __init__(self, parameters):
        super().__init__()
        
        p = parameters.info
        
        user   = EntryWidget(p.user, ALIGN_RIGHT=False)
        setup  = EntryWidget(p.setup, ALIGN_RIGHT=False)
        rh     = EntryWidget(p.rh)
        emit   = EntryWidget(p.emit, ALIGN_RIGHT=False)
        detec  = EntryWidget(p.detec, ALIGN_RIGHT=False)
        pcapow = EntryWidget(p.pcapow)
        vbias  = EntryWidget(p.vbias)
        pmppow = EntryWidget(p.pmppow)
        pmppol = EntryWidget(p.pmppol)
        pols   = EntryWidget(p.pols, ENTRY_WIDTH=340, ALIGN_RIGHT=False)
        sample = EntryWidget(p.sample, ENTRY_WIDTH=340, ALIGN_RIGHT=False)
        obs    = EntryWidget(p.obs, ENTRY_WIDTH=340, ALIGN_RIGHT=False)
        
        layout = QGridLayout(self)
        layout.addWidget(user, 0, 0)
        layout.addWidget(setup, 1, 0)
        layout.addWidget(rh, 1, 1)
        layout.addWidget(emit, 2, 0)
        layout.addWidget(detec, 2, 1)
        layout.addWidget(vbias, 3, 0)
        layout.addWidget(pcapow, 3, 1)
        layout.addWidget(pmppol, 4, 0)
        layout.addWidget(pmppow, 4, 1)
        layout.addWidget(pols, 5, 0, 1, 2)
        layout.addWidget(sample, 6, 0, 1, 2)
        layout.addWidget(obs, 7, 0, 1, 2)
        
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
        wait      = EntryWidget(p.wait, DoubleValidator, self.ENTRY_WIDTH)
        plot_rate = EntryWidget(p.plot_rate, IntValidator, self.ENTRY_WIDTH)
        
        thz_fix_button = QPushButton("Fix at start position")
        pmp_fix_button = QPushButton("Fix at start position")
        
        thz_group   = self._createVGroup("THz delay-line", thz_start, thz_end, thz_vel, thz_step, thz_fix_button)
        pmp_group   = self._createVGroup("Pump delay-line", pmp_start, pmp_end, pmp_vel, pmp_step, pmp_fix_button)
        other_group = self._createHGroup("Other configs", wait, plot_rate)
        
        thz_fix_button.clicked.connect(lambda: self._fixCommand(thz_start, thz_end))
        pmp_fix_button.clicked.connect(lambda: self._fixCommand(pmp_start, pmp_end))
        
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
    def _fixCommand(self, start_param, end_param):
        end_param.entry.setText(start_param.entry.text())


class MeasurementControlWidget(QWidget):
    LABEL_WIDTH      = 50
    ENTRY_WIDTH      = 50
    BUTTON_WIDTH     = 100
    CONTENTS_MARGINS = 0, 5, 0, 0
    
    def __init__(self, parameters):
        super().__init__()
        
        self.repeat       = EntryWidget(parameters.unsavable.repeat, IntValidator, self.ENTRY_WIDTH, self.LABEL_WIDTH)
        self.set_button   = QPushButton("Set")
        self.start_button = QPushButton("Start")
        self.stop_button  = QPushButton("Stop")
        
        self.set_button.setCheckable(True)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        
        layout = QHBoxLayout(self)
        for item in (self.repeat, self.set_button, self.start_button, self.stop_button):
            layout.addWidget(item)
        
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(*self.CONTENTS_MARGINS)
        
        self._connectSlots()
        
    def _connectSlots(self):
        self.set_button.toggled.connect(lambda state: self._setButtonToggled(state))
        self.start_button.clicked.connect(self._startButtonClicked)
        self.stop_button.clicked.connect(self._stopButtonClicked)
        
    @pyqtSlot()
    def _setButtonToggled(self, state):
        self.set_button.setEnabled(True)
        self.set_button.setText("Unset" if state else "Set")
        self.repeat.setEnabled(not state)
        self.stop_button.setEnabled(False)
        self.start_button.setEnabled(state)
    @pyqtSlot()
    def _startButtonClicked(self):
        self.start_button.setEnabled(False)
        self.set_button.setEnabled(False)
        self.stop_button.setEnabled(True)
    @pyqtSlot()
    def _stopButtonClicked(self):
        self.set_button.setChecked(False)


class EntryWidget(QWidget):
    UNIT_WIDTH       = 40
    CONTENTS_MARGINS = 0, 5, 0, 0
    
    def __init__(self, param, Validator=None, ENTRY_WIDTH=100, LABEL_WIDTH=80, ALIGN_RIGHT=True):
        super().__init__()
        
        self.LABEL_WIDTH = LABEL_WIDTH
        self.ENTRY_WIDTH = ENTRY_WIDTH
        
        self.param = param
        self.label = QLabel(f"{self.param.name}:")
        self.entry = QLineEdit()
        self.unit  = QLabel(self.param.unit)
        
        self.label.setFixedWidth(self.LABEL_WIDTH)
        self.entry.setFixedWidth(self.ENTRY_WIDTH)
        self.unit.setFixedWidth(self.UNIT_WIDTH)
        
        self.entry.setText(self.param.value)
        
        if ALIGN_RIGHT: self.entry.setAlignment(Qt.AlignmentFlag.AlignRight)
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
        
        