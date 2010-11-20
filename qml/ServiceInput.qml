import Qt 4.7

//Rectangle {
//    id: serviceInput
//    color: "red";
//    parent: serviceView
//    width: parent.width
//    height: 50

//}

Rectangle {
    id: serviceInput
    parent: serviceView
    width: parent.width
    height: 70
    Row {
        id: serviceInputRow
        height: parent.height
        width:parent.width;
        TextInput {
            width:parent.width/8*3
            height: parent.height
        }
        Rectangle {
            id: serviceInputOption
            width:parent.width/8*3
            height: parent.height
            Text {
                anchors.centerIn: parent
                text:'Option'
            }
            MouseArea {
                id: mouseAreaOption
                anchors.fill: parent
                onClicked: serviceInput.selectOption()
            }
            gradient: Gradient {
                GradientStop {id:option1; position: 0;color: screen.gradientColorStart}
                GradientStop {id:option2; position: 1;color: screen.gradientColorEnd}
            }
            states: [
                State {
                    name: 'clicked'
                    when: mouseAreaOption.pressed
                    PropertyChanges { target: option1; position:1}
                    PropertyChanges { target: option2; position:0 }
                }
            ]
        }

        Rectangle {
            id: serviceInputGo
            width:parent.width/4
            height: parent.height
            Text {
                anchors.centerIn: parent
                text:'go'
            }
            MouseArea {
                id: mouseAreaGo
                anchors.fill: parent
                onClicked: serviceInput.askZiggy()
            }
            gradient: Gradient {
                GradientStop {id:go1;position: 0;color: screen.gradientColorStart}
                GradientStop {id:go2;position: 1;color: screen.gradientColorEnd}
            }
            states: [
                State {
                    name: 'clicked'
                    when: mouseAreaGo.pressed
                    PropertyChanges { target: go1; position:1}
                    PropertyChanges { target: go2; position:0 }
                }
            ]
        }
    }
    function askZiggy() {
        console.log("ask ziggy")
    }

    function selectOption() {
        console.log("service_option")

    }
}
