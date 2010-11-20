import Qt 4.7

Rectangle {
    id: serviceToolbar
    parent: serviceView
    width: parent.width
    height: 45

    Row {
        id: serviceToolbarRow
//            spacing: 2
        height: parent.height
        width: parent.width;

        Rectangle {
            id: serviceToolbarSettings
            width:parent.width/3
            height: parent.height
            Text {
                anchors.centerIn: parent
                text:'Settings'
            }
            MouseArea {
                id: mouseAreaSettings
                anchors.fill: parent
                onClicked: serviceView.showSettings()
            }
            gradient: Gradient {
                GradientStop {id:settings1;position: 0;color: screen.gradientColorStart}
                GradientStop {id:settings2;position: 1;color: screen.gradientColorEnd}
            }
            states: [
                State {
                    name: 'clicked'
                    when: mouseAreaSettings.pressed
                    PropertyChanges { target: settings1; position:1}
                    PropertyChanges { target: settings2; position:0 }
                }
            ]
        }

        Rectangle {
            id: serviceToolbarHistory
            width:parent.width/3
            height: parent.height
            Text {
                anchors.centerIn: parent
                text:'History'
            }
            MouseArea {
                id: mouseAreaHistory
                anchors.fill: parent
                onClicked: serviceView.showHistory()
            }
            gradient: Gradient {
                GradientStop {id:history1;position: 0;color: screen.gradientColorStart}
                GradientStop {id:history2;position: 1;color: screen.gradientColorEnd}
            }
            states: [
                State {
                    name: 'clicked'
                    when: mouseAreaHistory.pressed
                    PropertyChanges { target: history1; position:1}
                    PropertyChanges { target: history2; position:0 }
                }
            ]
        }

        Rectangle {
            id: serviceToolbarBack
            width:parent.width/3
            height: parent.height
            Text {
                anchors.centerIn: parent
                text:'<- Back'
            }
            MouseArea {
                id: mouseAreaBack
                anchors.fill: parent
                onClicked: screen.showServicesList()
            }
            gradient: Gradient {
                GradientStop {id:back1;position: 0;color: screen.gradientColorStart}
                GradientStop {id:back2;position: 1;color: screen.gradientColorEnd}
            }
            states: [
                State {
                    name: 'clicked'
                    when: mouseAreaBack.pressed
                    PropertyChanges { target: back1; position:1}
                    PropertyChanges { target: back2; position:0 }
                }
            ]
        }

    }
}
