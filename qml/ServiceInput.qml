import Qt 4.7

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

        RectangleButton {
            clickAction: "serviceView.selectInputOption"
            width: parent.width/8*3
            buttonText: "Option"
        }

        RectangleButton {
            clickAction: "serviceView.askZiggy"
            width: parent.width/4
            buttonText: "go"
        }
    }

}
