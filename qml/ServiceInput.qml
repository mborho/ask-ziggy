import Qt 4.7

//Rectangle {
//    id: serviceInput
//    color: "red";
//    parent: serviceView
//    width: parent.width
//    height: 50

//}

Rectangle {
    id: serviceInput
    parent: serviceView
    width: parent.width
    height: 50
    Row {
        id: serviceInputRow
        height: parent.height
        width:parent.width;
        Rectangle { color: "lightgrey";width:parent.width/3;  height: parent.height}
        Rectangle { color: "grey"; width:parent.width/3; height: parent.height}
        Rectangle { color: "blue";width:parent.width/3; height: parent.height}

    }
}
