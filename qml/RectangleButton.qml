import Qt 4.7

Rectangle {
//    signal clicked
    width:parent.width/3
    height: parent.height
    property string clickAction
    property string buttonText

    Text {
        anchors.centerIn: parent
        text:buttonText
    }
    MouseArea {
        id: mouse
        anchors.fill: parent
        onClicked: serviceView.toolbarFuncCaller(clickAction)
    }
    gradient: Gradient {
        GradientStop {id:settings1;position: 0;color: screen.gradientColorStart}
        GradientStop {id:settings2;position: 1;color: screen.gradientColorEnd}
    }
    states: [
        State {
            name: 'clicked'
            when: mouse.pressed
            PropertyChanges { target: settings1; position:1}
            PropertyChanges { target: settings2; position:0 }
        }
    ]
}
