from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt


class ConnectionWidget(QWidget):
    def __init__(self, *instruments):
        super().__init__()
        
        layout = QVBoxLayout(self)
        for instr in instruments: layout.addWidget(instr.widget)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        

class DelayLineWidget(QWidget):
    def __init__(self, *delaylines):
        super().__init__()
        
        layout = QVBoxLayout(self)
        for dl in delaylines: layout.addWidget(dl.control)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)