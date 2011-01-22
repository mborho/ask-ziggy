import Qt 4.7

Rectangle {
    id: serviceInputMetacritic
    parent: serviceView
    width: parent.width
    height: 70
    Row {
        id: serviceInputRow
        height: parent.height
        width:parent.width;

        TextInput {
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
