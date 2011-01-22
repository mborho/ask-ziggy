import Qt 4.7

Rectangle {
    id: serviceInputTlate
    parent: serviceView
    width: parent.width
    height: 100
    property alias inputText: textInput.text

    Row {
        id: serviceInputRow
        height: parent.height;
        width:parent.width;

        TextEdit {
           id:textInput
           width:parent.width/8*4
           height: parent.height
           wrapMode:TextEdit.WordWrap
        }

        Column {
            height: parent.height/2;
            width:parent.width/16*5;
            RectangleButton {
                id:serviceOption1
                clickAction: "Ziggy.selectInputTlateFrom"
                width: parent.width
                buttonText: serviceView.optionText1
            }
            RectangleButton {
                id:serviceOption2
                clickAction: "Ziggy.selectInputTlateTo"
                width: parent.width
                buttonText: serviceView.optionText2
            }
        }

        ServiceInputSubmit {
            width:parent.width/16*3
        }
    }
}
