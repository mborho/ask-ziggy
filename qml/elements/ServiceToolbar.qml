import Qt 4.7

Rectangle {
    id: serviceToolbar
    width: serviceView.width
    visible:true
    height: screen.toolbarHeight
    parent: serviceView
    anchors.bottom: parent.bottom

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
            visible: (screen.currentService != 'tlate') ? 1 : 0;
        }

        DummyButton {
            visible: (screen.currentService != 'tlate') ? 0 : 1;
        }

        RectangleButton {
            clickAction: "Ziggy.showSettings"
            buttonText: "Settings"
        }

    }
}
