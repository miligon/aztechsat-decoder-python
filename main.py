import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from gui import Ui_MainWindow
from decoder import *

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        previo = 0;
        for col in self._data:
            if len(col) > previo:
                previo = len(col)
        return previo
 
class Decoder_Form(QtWidgets.QMainWindow, Ui_MainWindow):
    # Cuando se inicializa el Form
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        # Se conectan los eventos
        self.btnDecode.clicked.connect(self.decode)
        
    def decode(self):
        frame = self.txtFrame.text()
        if len(frame) > 157*2:
            byte_data = extract_frame(frame)
            decoder = Decoder(byte_data)
            
            self.tableEPS.setModel(TableModel(decoder.dumpEPSdata()))
            self.tableOBC.setModel(TableModel(decoder.dumpOBCdata()))
            self.tableADCS.setModel(TableModel(decoder.dumpADCSdata()))
            self.tableRADIO.setModel(TableModel(decoder.dumpRADIOdata()))
            self.tablePAYLOAD.setModel(TableModel(decoder.dumpPAYLOADdata()))
            
            self.lblStatus.setText("FRAME VALIDO!")
            self.lblFrameNumber.setText(str(decoder.get_frame_id()))
                                   
        else:
            print("Longitud de frame incorrecta")
 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = Decoder_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
    
    
    

#parser = argparse.ArgumentParser(description='Optional app description')
#parser.add_argument('opt_pos_arg', type=int, nargs='?',
#                   help='An optional integer positional argument')
        
#frame=read_file(2)
#print(decode(frame))
#read_file_csv()
