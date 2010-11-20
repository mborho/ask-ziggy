import Qt 4.7

Item {
    id: screen;
    property string gradientColorStart: "lightgrey"
    property string gradientColorEnd: "grey"

    function showServiceView(command) {
        console.log(command)
        startView.visible =  false
        serviceView.visible = true
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

    transitions: Transition {
        ColorAnimation {duration: 1000 }
    }

}
