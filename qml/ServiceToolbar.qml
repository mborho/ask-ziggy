import Qt 4.7

Rectangle {
    id: serviceToolbar
    parent: serviceView
    width: parent.width
    height: 50

    Row {
        id: serviceToolbarRow
//            spacing: 2
        height: parent.height
        width: parent.width;
        Rectangle { color: "orange"; width:parent.width/3; height: parent.height}
        Rectangle { color: "green";width:parent.width/3; height: parent.height}
        Rectangle { color: "yellow";width:parent.width/3;  height: parent.height}
    }
}
