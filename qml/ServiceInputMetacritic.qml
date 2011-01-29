import Qt 4.7

Rectangle {
    id: serviceInputMetacritic
    width: serviceView.width
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
            width:parent.width/4*3
        }

        ServiceInputSubmit {
            width:parent.width/4
        }
    }

}
