import Qt 4.7

Rectangle {
    id: serviceInputTlate
    parent: serviceView
    width: parent.width
    height: 70
    Row {
        id: serviceInputRow
        height: parent.height;
        width:parent.width;

        TextInput {
           width:parent.width/8*4
           height: parent.height
        }
        Column {
            height: parent.height/2;
            width:parent.width/16*5;
            RectangleButton {
                clickAction: "Ziggy.selectInputTlateFrom"
                width: parent.width
                buttonText: "From"
            }

            RectangleButton {
                clickAction: "Ziggy.selectInputTlateTo"
                width: parent.width
                buttonText: "To"
            }
        }
        RectangleButton {
            width:parent.width/16*3
            clickAction: "Ziggy.askZiggy"
            height: parent.height
            buttonText: "go"
        }
    }
}
