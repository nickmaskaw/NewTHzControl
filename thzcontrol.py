import sys
from PyQt6.QtWidgets import QApplication
from interface import MainWindow, LeftDockWidget, ConnectionWidget, DelayLineWidget
from instruments import VISAInstrument, KBD101


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
    
    sys.exit(app.exec())