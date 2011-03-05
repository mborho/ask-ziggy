import Qt 4.7

Rectangle {
    id: startView
    color: "lightgrey";
    width: parent.width
    height: parent.height
    z:3

    ListView {
        id: serviveListView
        anchors.fill: parent
        model: ServiceModel {}
        delegate: serviceDelegate
        boundsBehavior:Flickable.DragOverBounds
        flickDeceleration:screen.defaultFlickDeceleration
    }

    Component {
        id: serviceDelegate
        Item {
            width: parent.width
            height: 80
            Rectangle {
                id: column
                width: parent.width
                height: parent.height
                Column {
                    id: delegatorColumn
                    anchors.centerIn: parent
                    Text {
                        id: serviceText
                        text: '<b>'+name+'</b> '
                    }
                }
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    onReleased: parent.serviceClicked(command, input)
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
                function serviceClicked(command, input) {
                    screen.showServiceView(command, input)
                }
            }
        }
    }
}
