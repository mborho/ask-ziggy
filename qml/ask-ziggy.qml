import Qt 4.7

Item {
    id: screen;
    property string gradientColorStart: "lightgrey"
    property string gradientColorEnd: "grey"
    property string currentService: ""

    function showServiceView(command) {
        console.log(command)
        startView.visible =  false
        serviceView.visible = true
        screen.currentService = command
    }

    function showServicesList() {
        startView.visible =  true
        serviceView.visible = false
    }

    function dummy() {
        console.log('dummy')
    }

    StartView {
        id:startView
    }

    ServiceView {
        id:serviceView
    }  

    ServiceOptionDialog {
            id: serviceOptionDialog
//            anchors.centerIn: serviceView
            z: 100
    }

    transitions: Transition {
        ColorAnimation {duration: 1000 }
    }

}

