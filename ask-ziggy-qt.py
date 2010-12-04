# -*- coding: utf-8 -*-
import sys
import socket
import os.path
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ziggy.languages import Languages
from ziggy.state import AppState
from ziggy import styles
from baas.core.plugins import PluginLoader
from baas.core.helpers import strip_tags, htmlentities_decode, xmlify


# set timeout to 10 seconds
timeout = 10
socket.setdefaulttimeout(timeout)

APP_WIDTH = 800
APP_HEIGHT = 480
DIALOG_HEIGHT = 350

CSS_FILE = os.path.dirname(os.path.abspath(__file__))+'/ziggy.css'

pluginHnd = PluginLoader(config=False,format="raw")
pluginHnd.load_plugins()
pluginHnd.load_map()
pluginHnd.load_help()

wording = {
    'tlate':'Translation',
    'weather':'Weather Forecast',
    'news':'Yahoo News Search',
    'web':'Yahoo Web Search',
    'gnews':'Google News Search',
    'gweb':'Google Web Search',
    'deli':'Bookmarks on delicious.com',
    'metacritic':'Reviews on metacritic.com',
    'imdb':'Movies on IMDb.com',
    'wikipedia':'Wikipedia',
    'wiktionary':'Wiktionary',
    }


about_txt = """
Ask Ziggy - Search for news, weather, translations, reviews,\t\t
 movies, wikipedia or wiktionary entries and more...\n
<small>&#169; 2010 Martin Borho &lt;martin@borho.net&gt;\t\t\t\n
License: GNU General Public License (GPL) Version 3
Source: <span color="orange">http://github.com/mborho/ask-ziggy</span></small>
"""   
class ResultListModel(QAbstractListModel): 
    def __init__(self, datain, parent=None, *args): 
        """ datain: a list where each item is a row
        """
        QAbstractListModel.__init__(self, parent, *args) 
        self.listdata = datain
 
    def rowCount(self, parent=QModelIndex()): 
        return len(self.listdata) 
 
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else: 
            return QVariant()

class ZiggyWindow(QMainWindow):
    def __init__(self):
        services = sorted(wording.items(), key=lambda(k,v):(v,k))
        self.services = services
        self.state = AppState([a[0] for a in services])
        self.lang = Languages()
        self.term = None
        self.inputCommand = None
        self.inputBuffer = None
        self.inputLang = None
        self.inputPage = 1
        self.reload_results = None
        self.history_button = None
        self.langButton = None
        self.langDialog = None
        self.service_dialog = None
        
        QMainWindow.__init__(self)
        self.setStyleSheet(styles.main_style)
        self.setAttribute(Qt.WA_Maemo5StackedWindow)
        self.main = QWidget(self)
        #self.main.setStyleSheet(styles.main_style)

        self.setCentralWidget(self.main)
        self.getServicesMain()

    def getServicesMain(self):        
        #main = QWidget(self.main)
        self.main.setMinimumSize(APP_WIDTH,0)         
        vbox = QVBoxLayout(self.main)    
        signalMapper = QSignalMapper(self)  
        for service in self.state.services:
            if service not in self.state.services_active:
                continue
            button = QPushButton(wording[service])
            button.setStyleSheet(styles.service_list_button)
            signalMapper.setMapping(button, self.state.services_active.index(service)) 
            button.clicked.connect(signalMapper.map)
            vbox.addWidget(button)
        signalMapper.mapped.connect(self.serviceChoosen) 
        
        self.sa = QScrollArea(self)
        self.sa.setWidget(self.main)
        self.setCentralWidget(self.sa) 
        
    def serviceChoosen(self, service):
        self.inputCommand = self.state.services_active[service]

        stackwindow = QMainWindow(self.main)
        stackwindow.setAttribute(Qt.WA_Maemo5StackedWindow)
        stackwindow.setWindowTitle(wording[self.inputCommand])

        widget = QWidget(self)
        stackwindow.setCentralWidget(widget)

        self.goButton = QPushButton("go")
        self.connect(self.goButton, SIGNAL("clicked()"), self.askBuddy)

        self.inputField = QLineEdit()
        self.inputField.setStyleSheet(styles.qline_edit);
        frame = QFrame(widget)
        self.grid = QGridLayout(widget)
        self.grid.addWidget(self.inputField, 1, 0)
        if self.inputCommand not in ['tlate','metacritic']:
            if self.state.langs.get(self.inputCommand):
                lButtonLabel = self.state.langs.get(self.inputCommand)[1].decode('utf-8')
            else:
                lButtonLabel = self.labelWhat()
            self.langButton = QPushButton(lButtonLabel)
            x = lambda: self.getLangButton(self.inputCommand)
            self.connect(self.langButton, SIGNAL("clicked()"), x)
            self.grid.addWidget(self.langButton, 1, 1)
            self.grid.addWidget(self.goButton, 1, 2)
        else:
            self.grid.addWidget(self.goButton, 1, 1)
        
        
        
        self.resultWidget = QWidget(self)        
        self.grid.addWidget(self.resultWidget, 2, 0, 2 ,2)

        stackwindow.show()
    
    def getLangButton(self, service):
        self.langDialog = QDialog(self.main)        
        self.langDialog.setWindowTitle('Choose your %s' % self.labelWhat())
        self.langDialog.setModal(True)
        lw = QListWidget(self.langDialog)
        lw.setMinimumSize(APP_WIDTH,DIALOG_HEIGHT)     
        scrollTo = None
        for (short, name) in self.lang.get(service):
            le = QListWidgetItem(lw, type=lw.count())
            if self.state.langs.get(self.inputCommand) \
                and short == self.state.langs.get(self.inputCommand)[0]:
                    le.setSelected(True)
                    scrollTo = le
            le.setText(name.decode('utf-8'))
            le.setTextAlignment(Qt.AlignCenter)
        if scrollTo:
            lw.scrollToItem(scrollTo)
        self.connect(lw, SIGNAL("itemClicked(QListWidgetItem *)"), self.getLangSelected)
        self.langDialog.show()

    def getLangSelected(self, button):
        clicked = button.type()
        self.inputLang = self.lang.get(self.inputCommand)[clicked]
        self.state.langs[self.inputCommand] = self.inputLang
        self.langButton.setText(self.inputLang[1].decode('utf-8'))
        self.langDialog.close()
        
    def askBuddy(self):
        
        print self.inputCommand
        #self.waiting_start('msg')   
        self.resultData = None
        commandoFunc = pluginHnd.commands.get(self.inputCommand)

        if self.inputCommand != 'tlate':
            self.inputBuffer = unicode(self.inputField.text())

        if self.inputBuffer == '':
            #self.waiting_stop()
            return None

        if commandoFunc:
            self.term = self.prepareTerm()
            print self.term
            resultMsg = ''
            try:
                resultMsg = commandoFunc(self.term)                
            except URLError, e:
                #hildon.hildon_banner_show_information(self.window, "",
                    #"Request failed, timed out.")
                print "Request failed, timed out."
            except IOError, e:
                #hildon.hildon_banner_show_information(self.window, "",
                #    "No network, please check your connection.")
                print "No network, please check your connection."
            except EnvironmentError, e:
                #hildon.hildon_banner_show_information(self.window, "", str(e))
                print "EnvironmentError"
            except Exception, e:
                #hildon.hildon_banner_show_information(self.window, "", "Error occured.")
                print "Exception"
            self.resultData = resultMsg
            #if self.term:
                #self.update_state()
        else:
            self.resultData = [{'title':'Uups, commando not known\n'}]
        
        #if hasattr(self, 'resultOutput'):
            #self.resultOutput.destroy()
        if self.inputCommand not in ['tlate','weather']:
            #self.resultOutput = self.createResultSelector(self.resultData)
            self.createResultSelector()
        #else:
            #resultMarkup = self.getResultMarkup()
            #self.createResultText(resultMarkup)

        #self.result_area.add(self.result_output)
        #self.result_output.show()   
        #self.waiting_stop()   

    def prepareTerm(self):
        ''' prepares statement for ape request '''
        inputBuffer = self.inputBuffer.strip()
        if self.inputCommand == 'deli' and self.state.deli_pop:
            term = inputBuffer + ' #pop'
        elif self.inputCommand == "tlate":
            term = inputBuffer
            for token in [t for t in ['@','#'] if self.state.tlate.get(t)]:
                term = "%s %s%s" % (term, token, self.state.tlate.get(token)[0])

        elif self.state.langs.get(self.inputCommand):
            term = inputBuffer + ' #'+self.state.langs[self.inputCommand][0]
        else:
            term = inputBuffer

        print "term %s" % term
        return term.strip()
        
    def createResultSelector(self):
        listData = []
        self.grid.removeWidget(self.resultWidget)
        self.resultWidget = QWidget(self)
        self.resultWidget.setMinimumSize(APP_WIDTH,0)
        self.resultWidget.setStyleSheet(styles.main_style)
        self.grid.addWidget(self.resultWidget, 2, 0, 2,3)
        if self.resultData and type(self.resultData) == list:
            for entry in self.resultData:
                listData.append(xmlify(htmlentities_decode(entry.get('title','#'))))
        lm = ResultListModel(listData, self)
        lv = QListView()        
        lv.setModel(lm)
        layout = QVBoxLayout(self.resultWidget)
        layout.addWidget(lv) 
        self.resultWidget.show()
        
    def labelWhat(self):
        return 'language' if self.inputCommand != "gnews" else 'edition'
        
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    w = ZiggyWindow()
    w.show()
    app.exec_()
    sys.exit()

'''

'''
