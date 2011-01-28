import Qt 4.7

Rectangle {
    id: serviceInput
    parent: serviceViewColumn
    width: parent.width
    height: 70
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
            id:serviceOption1
            clickAction: "Ziggy.selectInputOption"
            width: parent.width/8*3
            buttonText: serviceView.optionText1
        }

        ServiceInputSubmit {

        }
    }

}
