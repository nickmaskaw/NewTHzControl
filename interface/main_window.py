from PyQt6.QtWidgets import QMainWindow, QDockWidget
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self._initUI()
        
    def _initUI(self):
        self.setWindowTitle("THz-TDS Control")
        self.setWindowIcon(QIcon("icon/icon.png"))
        
        menu_bar = self.menuBar()
        self.window_menu = menu_bar.addMenu("&Window")
        
    def setInstrumentWidget(self, widget):        
        instrument_widget = LeftDockWidget(self, "Instruments", widget)
        
    def setParametersWidget(self, widget):
        parameters_widget = LeftDockWidget(self, "Measurement Parameters", widget)
    
    def setLivePlot(self, live_plot):
        self.setCentralWidget(live_plot)
        
        
class DockWidget(QDockWidget):
    def __init__(self, parent, name, widget):
        super().__init__(name, parent)
        
        self.parent = parent
        
        self.setWidget(widget)
        self.setFloating(False)

        self.parent.window_menu.addAction(self.toggleViewAction())            
            
            
class LeftDockWidget(DockWidget):
    def __init__(self, parent, name, widget):
        super().__init__(parent, name, widget)
        
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.parent.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)