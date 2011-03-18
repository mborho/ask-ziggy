#!/usr/bin/env python
from PySide import QtCore, QtGui, QtDeclarative

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    view.setSource(QtCore.QUrl('ask-ziggy.qml'))
    root = view.rootObject()
    #view.showFullScreen()
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    view.show()

    sys.exit(app.exec_())