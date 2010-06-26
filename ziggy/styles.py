# -*- coding: utf-8 -*-
#background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #dadbde);
main_style = '''    
    background-color:gray;
'''
service_list_area = '''
    QScrollArea {margin-top:4px;margin-bottom:0px;}
}'''

service_list_button = '''
QPushButton {
    border: 2px solid #48485A;
    border-radius: 10px;
    min-height:60px;
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #dadbde, stop: 1 #202028);    
}
QPushButton:pressed {
    background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #202028, stop: 1 #dadbde);
}
'''

qline_edit = '''
QLineEdit {
    background:white;
    border: 5px solid gray;
    border-radius:10px;
    padding:10px;
}
'''