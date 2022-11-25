from PyQt6.QtWidgets import QMainWindow, QDockWidget
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setUpUI()
        self.setUpMenuBar()
        
    def setUpUI(self):
        self.setWindowTitle("THz-TDS Control")
        self.setWindowIcon(QIcon("icon/icon.png"))
    
    def setUpMenuBar(self):
        menu_bar = self.menuBar()
        self.window_menu = menu_bar.addMenu("&Window")
        

class DockWidget(QDockWidget):
    def __init__(self, name, parent, widget):
        super().__init__(name, parent)
        
        self._name   = name
        self._parent = parent
        self._action = QAction(self.name, parent)
        
        self._setUpWidget(widget)
        self._setUpAction()        
        
    @property
    def name(self): return self._name
    @property
    def parent(self): return self._parent
    @property
    def action(self): return self._action
    
    def _setUpWidget(self, widget):
        self.setWidget(widget)
        self.setFloating(False)
        
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
            
            
class LeftDockWidget(DockWidget):
    def __init__(self, name, parent, widget):
        super().__init__(name, parent, widget)
        
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        self.parent.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self)