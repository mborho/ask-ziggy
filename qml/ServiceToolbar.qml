import Qt 4.7
import "elements"

Rectangle {
    id: serviceToolbar
    width: serviceView.width
    visible:true
    height: 70    
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
        }

        RectangleButton {
            clickAction: "Ziggy.showSettings"
            buttonText: "Settings"
        }

    }
}
