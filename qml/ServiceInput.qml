import Qt 4.7

Rectangle {
    id: serviceInput
    parent: serviceView
    width: parent.width
    height: 70
    Row {
        id: serviceInputRow
        height: parent.height
        width:parent.width;

        TextInput {
            width:parent.width/8*3
            height: parent.height
        }

        RectangleButton {
            clickAction: "serviceInput.selectOption"
            width: parent.width/8*3
            buttonText: "Option"
        }

        RectangleButton {
            clickAction: "serviceInput.askZiggy"
            width: parent.width/4
            buttonText: "go"
        }
    }

    function askZiggy() {
        console.log("ask ziggy")
        console.log(screen.currentService)
        console.log(screen.currentServiceOption1)
    }

    function selectOption() {
        serviceOptionDialog.show("service_option")
    }
}
