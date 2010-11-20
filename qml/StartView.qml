import Qt 4.7

Rectangle {
    id: startView
    color: "lightgrey";
    width: parent.width
    height: parent.height

    ListView {
        id: serviveListView
        anchors.fill: parent
        model: ServiceModel {}
        delegate: serviceDelegate
//            highlight: Rectangle { color: "blue"; radius: 5;  opacity: 0.1; width: parent.width }
//            highlightFollowsCurrentItem: true
        focus: true

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
//                    property bool isSelected: false
                Column {
                    id: delegatorColumn
                    anchors.centerIn: parent
                    Text {
                        id: serviceText
                        color:"darkblue"
                        text: '<b>'+name+'</b> '
                    }
                }
                MouseArea { anchors.fill: parent; onClicked: parent.serviceClicked(parent) }
                gradient: Gradient {
                    GradientStop {id:stop1;position: 0;color: "lightgrey"}
                    GradientStop {id:stop2;position: 1;color: "grey"}

                }
                states: [
                    State {
                        name: 'clicked'
                        //when: column.isSelected == true
                        PropertyChanges { target: stop1; position:1}
                        PropertyChanges { target: stop2; position:0 }
                    }
                ]
                function serviceClicked(parent) {
//                        parent.height = 100'
                    parent.state = "clicked"
                    serviceText.text = 'Loading....'+command
                    screen.loadServiceView(command)
                }
            }

        }

    }
}
