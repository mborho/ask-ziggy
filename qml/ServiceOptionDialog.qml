import Qt 4.7
import "options" as Options

Rectangle {
    id: serviceOptionDialog
    height: parent.height
    width: parent.width //dialogText.width + 20
    opacity: 0
    color: screen.gradientColorStart
    anchors.centerIn: parent

    function show(text) {
//        dialogText.text = text;
        serviceOptionDialog.opacity = 0.7;
    }

    function hide() {
        serviceOptionDialog.opacity = 0;
    }

//    Text {
//        id: dialogText
//        anchors.centerIn: parent
//        text: ""
//    }

//    MouseArea {
//        anchors.fill: parent
//        onClicked: hide();
//    }

    ListView {
        id: serviveOptionListView
        anchors.fill: parent
        model: Options.ServiceOptionModel {}
        delegate: serviceOptionDelegate
        focus: true

    }

    Component {
        id: serviceOptionDelegate
        Item {
            width: parent.width
            height: 40
            Rectangle {
                id: column
                width: parent.width - parent.width/8
                height: parent.height
                anchors.centerIn: parent
                Column {
                    id: delegatorColumn
                    anchors.centerIn: parent
                    Text {
                        id: serviceOptionText
                        text: '<b>'+name+'</b> '
                    }
                }
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    onReleased: parent.optionClicked(ident)
                }
                gradient: Gradient {
                    GradientStop {id:stop1;position: 0;color: screen.gradientColorStart}
                    GradientStop {id:stop2;position: 1;color: screen.gradientColorEnd}
                }
                states: [
                    State {
                        name: 'clicked'
                        when: mouseArea.pressed
                        PropertyChanges { target: stop1; position:1}
                        PropertyChanges { target: stop2; position:0 }
                    }
                ]
                function optionClicked(ident) {
                    serviceOptionDialog.hide()
                    console.log('option '+ident+' selected')
                }
            }

        }

    }
}
