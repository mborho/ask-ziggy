import Qt 4.7

Rectangle {
    id: serviceInputDeli
    parent: serviceViewColumn
    width: parent.width
    height: 70
    property bool deliPopState: false
    property alias inputText: textInput.text
    Keys.onPressed: {
        if(textInput.activeFocus == false) {
            textInput.focus = true
            textInput.text = event.text
        }
    }
    Row {
        id: serviceInputRow
        height: parent.height
        width:parent.width;

        ServiceTextInput {
            id:textInput
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
                source: "content/icons/ok.png"
                visible:false
            }
        }

        ServiceInputSubmit {

        }
    }

    function toggleDeliPopState() {
        if(deliPopState == false) {
            deliPopIcon.visible = true
            deliPopState = true
        } else {
            deliPopIcon.visible = false
            deliPopState = false
        }
    }

}
