import Qt 4.7

Rectangle {
    id: serviceToolbar
    parent: serviceViewColumn
    width: parent.width
    visible:true
    height: 45

    Row {
        id: serviceToolbarRow
        height: parent.height
        width: parent.width;

        RectangleButton {
            clickAction: "Ziggy.showSettings"
            buttonText: "Settings"
        }

        RectangleButton {
            clickAction: "Ziggy.showHistory"
            buttonText: "History"
        }

        RectangleButton {
            clickAction: "screen.showServicesList"
            buttonText: "<- Back"
        }

    }
}
