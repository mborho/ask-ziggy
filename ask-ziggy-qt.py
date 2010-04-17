import sys
import socket
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ziggy.languages import Languages
from ziggy.state import AppState
from baas.core.plugins import PluginLoader
from baas.core.helpers import strip_tags, htmlentities_decode, xmlify


# set timeout to 10 seconds
timeout = 10
socket.setdefaulttimeout(timeout)

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
    }


about_txt = """
Ask Ziggy - Search for news, weather, translations, reviews,\t\t
 movies, wikipedia entries and more...\n
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

class StackedWindow(QMainWindow):
    def __init__(self, *args):
        apply(QMainWindow.__init__, (self, ) + args)
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

class ZiggyWindow(QMainWindow):#QtGui.QWidget):
    def __init__(self):
        services = sorted(wording.items(), key=lambda(k,v):(v,k))        
        self.services = services
        self.state = AppState([a[0] for a in services])
        self.lang = Languages()
        self.inputCommand = None
        self.inputBuffer = None
        self.inputLang = None
        self.historyButton = None
        self.langButton = None
        self.resultData = None

        QMainWindow.__init__(self)
        self.main = QWidget(self)
        self.setCentralWidget(self.main)
        self.getServicesMain()

    def getServicesMain(self):
        grid = QGridLayout(self.main)

        j = 0
        pos = [(0, 0), (0, 1), 
                (1, 0), (1, 1),
                (2, 0), (2, 1),
                (3, 0), (3, 1),
                (4, 0), (4, 1),]

        for short in self.state.services_active:
            button = QPushButton(wording[short])
            self.connect(button, SIGNAL("clicked()"), self.__getattribute__('service%s' % short.capitalize()))
            grid.addWidget(button, pos[j][0], pos[j][1])
            j = j + 1
    
    def serviceGnews(self):
        self.serviceChoosen('gnews')

    def serviceGweb(self):
        self.serviceChoosen('gweb')

    def serviceTlate(self):
        self.serviceChoosen('tlate')

    def serviceWeb(self):
        self.serviceChoosen('web')

    def serviceNews(self):
        self.serviceChoosen('news')

    def serviceWikipedia(self):
        self.serviceChoosen('wikipedia')

    def serviceImdb(self):
        self.serviceChoosen('imdb')

    def serviceMetacritic(self):
        self.serviceChoosen('metacritic')

    def serviceWeather(self):
        self.serviceChoosen('weather')

    def serviceDeli(self):
        self.serviceChoosen('deli')

    def serviceChoosen(self, service):
        self.inputCommand = service
        stackwindow = StackedWindow(self.main)
        stackwindow.setWindowTitle(wording[service])

        self.goButton = QPushButton("go")
        self.connect(self.goButton, SIGNAL("clicked()"), self.askBuddy)

        self.inputField = QLineEdit()

        frame = QFrame(stackwindow.widget)
        self.grid = QGridLayout(stackwindow.widget)
        #grid.setSpacing(10)

        self.grid.addWidget(self.inputField, 1, 0)
        self.grid.addWidget(self.goButton, 1, 1)
        
        self.resultWidget = QWidget(self)
        self.grid.addWidget(self.resultWidget, 2, 0, 2 ,2)

        stackwindow.show()

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
        self.grid.addWidget(self.resultWidget, 2, 0, 2 ,2)
        if self.resultData and type(self.resultData) == list:
            for entry in self.resultData:
                listData.append(xmlify(htmlentities_decode(entry.get('title','#'))))
        lm = ResultListModel(listData, self)
        lv = QListView()
        lv.setModel(lm)
        layout = QVBoxLayout(self.resultWidget)
        layout.addWidget(lv) 
        self.resultWidget.show()

    def buttonPushed(self):
        d = QDialog(self)
        vbox = QVBoxLayout()
        l = QLabel("Hi there. You clicked a button!")
        vbox.addWidget(l)
        b = QPushButton("Close window")
        self.connect(b, SIGNAL("clicked()"), d.close)
        vbox.addWidget(b)
        d.setLayout(vbox)
        d.show()


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    w = ZiggyWindow()
    w.show()
    app.exec_()
    sys.exit()

'''

'''