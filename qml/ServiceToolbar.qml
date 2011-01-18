import Qt 4.7

Rectangle {
    id: serviceToolbar
    parent: serviceView
    width: parent.width
    height: 45

    Row {
        id: serviceToolbarRow
//            spacing: 2
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
