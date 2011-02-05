import Qt 4.7
import "../js/Ziggy.js" as Ziggy

Rectangle {
    id: serviceView
    parent: screen
    width: screen.width
    height: screen.height
    color: "lightgrey"
//    opacity:1
//    z:2
//    x:800
    property string optionText1: "option 1"
    property string optionText2: "option 2"
    property Item serviceViewColumn
    property Item serviceInput
    property Item serviceContent
    property Item serviceToolbar

}
