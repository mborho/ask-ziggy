import Qt 4.7
import "elements"
import "views"
import "js/Ziggy.js" as Ziggy

Rectangle {
    id: screen;
    height: (runtime.orientation == Orientation.Portrait || runtime.orientation == Orientation.PortraitInverted) ? 800 : 424
    width: (runtime.orientation == Orientation.Portrait || runtime.orientation == Orientation.PortraitInverted) ? 424 : 800
    anchors.fill: parent

    property string apiUrl: 'http://ask-ziggy.appspot.com/api/query?&term=';
    property string gradientColorStart: "lightgrey"
    property string gradientColorEnd: "grey"
    property int toolbarHeight: 60
    property string currentService: ""
    property string currentServiceOption1: ""
    property string currentServiceOption2: ""
    property Item currentView
    property Item targetView

    function showServiceView(command, input) {
        screen.currentService = command;
        currentView = startView
        targetView = serviceView
        Ziggy.loadServiceView(command, input)
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
