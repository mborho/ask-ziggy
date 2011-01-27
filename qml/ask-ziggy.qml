import Qt 4.7
import "Ziggy.js" as Ziggy

Item {
    id: screen;
    property string apiUrl: 'http://ask-ziggy.appspot.com/api/query?&term=';
    property string gradientColorStart: "lightgrey"
    property string gradientColorEnd: "grey"
    property string currentService: ""
    property string currentServiceOption1: ""
    property string currentServiceOption2: ""
    property Item currentView
    property Item targetView
//    property bool root
    property bool direction

    function showServiceView(command) {
        console.log(command);
        screen.currentService = command;
        currentView = startView
        targetView = serviceView
        serviceView.loadServiceView(command)
        switchAnimation.start()
    }

    function showServicesList() {
        currentView = serviceView
        targetView = startView
        screen.currentService = ""
        screen.currentServiceOption1 = ""
        screen.currentServiceOption2 = ""
        switchAnimation.start()
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
            z: 100
    }
    property variant switchAnimation :
        ParallelAnimation {
//            SequentialAnimation {
            NumberAnimation {
                    target: currentView;
                    property: "opacity";
                    easing.type: Easing.InOutSine
                    to: 0
                    duration: 300
            }
            NumberAnimation {
                target: targetView;
                property: "opacity";
                easing.type: Easing.InOutSine
                to: 1
                duration: 300
            }
    }
}
