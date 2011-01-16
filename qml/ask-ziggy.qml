import Qt 4.7

Item {
    id: screen;
    property string gradientColorStart: "lightgrey"
    property string gradientColorEnd: "grey"
    property string currentService: ""
    property string currentServiceOption1: ""
    property string currentServiceOption2: ""

    function showServiceView(command) {
        console.log(command)
        screen.currentService = command
        startView.visible =  false
        serviceView.visible = true
    }

    function showServicesList() {
        startView.visible =  true
        serviceView.visible = false
        screen.currentService = ""
        screen.currentServiceOption1 = ""
        screen.currentServiceOption2 = ""
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


