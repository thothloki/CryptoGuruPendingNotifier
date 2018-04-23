import grpc
import api_pb2
import api_pb2_grpc
from decimal import Decimal
import time
import datetime
import requests
import sys
import os.path
import configparser
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QComboBox, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QTimer, Qt

class App (QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'CryptoGuru Pending Notifier'
        self.width = 360
        self.height = 100
        self.initUI()

    def closeEvent(self, event):
        saveSettings(self)
        event.accept()
        sys.exit(0)
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('cryptoguru.png'))

        self.poolSelect = QComboBox(self)
        self.poolSelect.addItem("0-100-pool.burst.cryptoguru.org:8008")
        self.poolSelect.addItem("50-50-pool.burst.cryptoguru.org:8008")
        self.poolSelect.addItem("100-0-pool.burst.cryptoguru.org:8008")
        
        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("Enter Burst Address or Numeric ID")

        self.pendingLabel = QLabel('Pending:')
        self.pendingAmount = QLabel('')

        self.effectiveCapacityLabel = QLabel('Effective Capacity:')
        self.effectiveCapacity = QLabel('')

        self.historicalShareLabel = QLabel('Historical Share:')
        self.historicalShare = QLabel('')

        self.validDlLabel = QLabel('Valid Deadlines Last 360 Blocks:')
        self.validDl = QLabel('')

        self.refreshTime = QLineEdit(self)
        self.refreshTime.setPlaceholderText('Refresh Time (Minutes)')

        file = 'settings.ini'
        if os.path.isfile(file):
            loadSettings(self)
               
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.textbox, 0,0,1,2)
        grid.addWidget(self.pendingLabel,1,0) 
        grid.addWidget(self.pendingAmount,1,1)
        grid.addWidget(self.effectiveCapacityLabel, 2, 0)
        grid.addWidget(self.effectiveCapacity, 2, 1)
        grid.addWidget(self.historicalShareLabel, 3, 0)
        grid.addWidget(self.historicalShare, 3, 1)
        grid.addWidget(self.validDlLabel, 4, 0)
        grid.addWidget(self.validDl, 4, 1)
        grid.addWidget(self.poolSelect, 5, 0)
        grid.addWidget(self.refreshTime, 5, 1)

        self.center()
        self.show()
        self.update()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


    def update(self):
        self.delay = 10000
        try:
            addy = (self.textbox.text())
            if addy == '':
                self.pendingAmount.setText('0')
                self.effectiveCapacity.setText('0')
                self.delay = 5000
            else:
                self.channel = grpc.insecure_channel(str(self.poolSelect.currentText()))
                self.stub = api_pb2_grpc.ApiStub(self.channel)

                addy = convert(addy)
                addy2 = int(addy)
                       
                self.miner1 = (self.stub.GetMinerInfo(api_pb2.MinerRequest(ID=addy2)))
        
                self.pend = (int(self.miner1.pending)/float(100000000))

                self.cap = Decimal(self.miner1.effectiveCapacity)
                self.cap = round(self.cap, 4)

                self.historic = (self.miner1.historicalShare)
                self.historic = round((self.historic * 100),3)

                self.blocks = (self.miner1.nConf)

                self.pendingAmount.setText(str(self.pend) + ' Burst')
                self.effectiveCapacity.setText(str(self.cap) + ' TB')
                self.historicalShare.setText(str(self.historic) + '%')
                self.validDl.setText(str(self.blocks))

                self.timeD = (self.refreshTime.text())
                if self.timeD != '' and self.timeD.isdigit():
                    customerDelayTime = delayTime(self.timeD)
                    self.delay = customerDelayTime
                else:
                    self.delay = 360000
        except:
            QTimer.singleShot(self.delay, self.update)
            print('error')
        finally:
            QTimer.singleShot(self.delay, self.update)


        
def convert(addy):
    burst = addy
    try:
        URL = ("https://wallet1.burstnation.com:8125/burst?requestType=rsConvert&account=" + burst)
        r = requests.get(url = URL)
        data = r.json()
        numeric = data['account']
        return numeric
    except:
        numeric = ''
        return numeric

def delayTime(minutes):
    timeA = str(minutes)
    timeB = int(timeA)
    seconds = (timeB*60)
    raw = (seconds * 1000)
    return raw

def saveSettings(self):
    address = self.textbox.text()
    pool = self.poolSelect.currentText()
    refreshTime = self.refreshTime.text()
    settingsFile = 'settings.ini'
    config = configparser.ConfigParser()
    config['settings'] = {'address': address, 'pool': pool, 'refresh-time': refreshTime}
    with open(settingsFile, 'w') as configfile:
        config.write(configfile)

def loadSettings(self):
    config = configparser.ConfigParser()
    config.read('settings.ini')
    address = config['settings']['address']
    pool = config['settings']['pool']
    refreshTime = config['settings']['refresh-time']
    self.textbox.setText(str(address))
    index = self.poolSelect.findText(str(pool), Qt.MatchFixedString)
    if index >= 0:
        self.poolSelect.setCurrentIndex(index)
    self.refreshTime.setText(refreshTime)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
