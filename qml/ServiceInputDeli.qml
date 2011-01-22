import Qt 4.7

Rectangle {
    id: serviceInputDeli
    parent: serviceView
    width: parent.width
    height: 70
    property bool deliPopState: false

    Row {
        id: serviceInputRow
        height: parent.height
        width:parent.width;

        TextInput {
            width:parent.width/4*2
            height: parent.height
        }

        RectangleButton {
            width: parent.width/8*3
            id: deliPopButton
            clickAction: "toggleDeliPopState"
            buttonText: "Popular"
            Image {
                id:deliPopIcon
                anchors.verticalCenter: parent.verticalCenter
                x: parent.width/8
//                anchors.fill: parent
                source: "content/icons/ok.png"
                visible:false
            }
        }

        RectangleButton {
            clickAction: "Ziggy.askZiggy"
            width: parent.width/8*1
            buttonText: "go"
        }
    }
    function toggleDeliPopState() {
        if(deliPopState == false) {
            console.log('togglePopState activate')
            deliPopIcon.visible = true
            deliPopState = true
        } else {
            console.log('togglePopState deactivate')
            deliPopIcon.visible = false
            deliPopState = false
        }
    }

}
