import Qt 4.7

Rectangle {
    id: serviceInputMetacritic
    parent: serviceViewColumn
    width: parent.width
    height: 70
    property alias inputText: textInput.text

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
