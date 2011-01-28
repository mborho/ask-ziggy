import Qt 4.7

TextInput {
    id:textInput
    font.pixelSize:parent.height/5*2
    y: (parent.height - parent.height/5*2)/2
    width:parent.width/8*4
    height: parent.height
    cursorVisible:true
    focus: false
}
