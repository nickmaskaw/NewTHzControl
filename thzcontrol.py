import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QDockWidget, QStatusBar, QLayout
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
import pyqtgraph as pg
from interface import MainWindow, LeftDockWidget, ConnectionWidget, DelayLineWidget
from instruments import VISAInstrument, KBD101


class VBoxDockWidget(QDockWidget):
    def __init__(self, name, parent, *instruments):
        super().__init__(name, parent)
        
        self._name   = name
        self._parent = parent
        self._action = QAction(f"&{self.name}", parent)
        
        self._setUpWidget(*instruments)
        self._setUpAction()
        
    @property
    def name(self): return self._name
    @property
    def parent(self): return self._parent
    @property
    def action(self): return self._action
    
    def _setUpWidget(self, *instruments):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        for instr in instruments: layout.addWidget(instr.widget)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(widget)
        self.setFloating(False)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.parent.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)
        
    def _setUpAction(self):
        self.action.setCheckable(True)
        self.action.setChecked(True)
        self.action.triggered.connect(self._actionTriggered)
        self.parent.window_menu.addAction(self.action)
        self.visibilityChanged.connect(lambda visible: self.action.setChecked(visible))
        
    def _actionTriggered(self):
        if self.action.isChecked():
            self.show()
        else:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    lockin = VISAInstrument("Lock-in")
    cernox = VISAInstrument("Cernox")
    pmp_dl = VISAInstrument("Pump delay-line")
    thz_dl = KBD101("THz delay-line")
    
    main_window = MainWindow()
    
    connection_widget = LeftDockWidget("Connection", main_window, ConnectionWidget(lockin, cernox, pmp_dl, thz_dl))
    delayline_widget  = LeftDockWidget("Delay-line control", main_window, DelayLineWidget(thz_dl))
    
    main_window.show()
    
    #window.plot_widget.plot([1, 2, 3, 4], [10, 20, 30, 40])
    
    sys.exit(app.exec())