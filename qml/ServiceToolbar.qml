import Qt 4.7

Rectangle {
    id: serviceToolbar
    parent: serviceViewColumn
    width: parent.width
    visible:true
    height: 70

    Row {
        id: serviceToolbarRow
        height: parent.height
        width: parent.width;


        RectangleButton {
            clickAction: "screen.showServicesList"
            buttonText: "<- Back"
        }


        RectangleButton {
            clickAction: "Ziggy.showHistory"
            buttonText: "History"
        }


        RectangleButton {
            clickAction: "Ziggy.showSettings"
            buttonText: "Settings"
        }

    }
}
