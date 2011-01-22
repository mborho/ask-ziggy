import Qt 4.7

Rectangle {
    id: serviceInputMetacritic
    parent: serviceView
    width: parent.width
    height: 70
    property alias inputText: textInput.text

    Row {
        id: serviceInputRow
        height: parent.height
        width:parent.width;

        TextInput {
            id:textInput
            width:parent.width/8*6
            height: parent.height
        }

        RectangleButton {
            clickAction: "Ziggy.askZiggy"
            width: parent.width/4
            buttonText: "go"
        }
    }

}
