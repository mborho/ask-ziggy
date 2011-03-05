import Qt 4.7
import "elements"
import "views"
import "js/Ziggy.js" as Ziggy
import "js/Appstate.js" as Appstate

Rectangle {
    id: screen;
//    height: (runtime.orientation == Orientation.Portrait || runtime.orientation == Orientation.PortraitInverted) ? 800 : 424
//    width: (runtime.orientation == Orientation.Portrait || runtime.orientation == Orientation.PortraitInverted) ? 424 : 800
    anchors.fill: parent
    property string apiUrl: 'http://ask-ziggy.appspot.com/api/query?&term=';
    property string gradientColorStart: "lightgrey"
    property string gradientColorEnd: "grey"
    property int toolbarHeight: 60
    property string currentService: ""
    property string currentTerm: ""
    property int currentPage: 1
    property int currentHistoryLimit: 20
    property string lastInput: ""
    property string currentServiceOption1: ""
    property string currentServiceOption2: ""
    property Item currentView
    property Item targetView
    Component.onCompleted: Appstate.init()

    function showServiceView(command, input) {
        screen.currentService = command;
        screen.currentPage = 1;
        screen.lastInput = '';
        currentView = startView
        targetView = serviceView
        Ziggy.loadServiceView(command, input)
        switchOut.start()
    }

    function showServicesList() {
        currentView = serviceView
        targetView = startView
        screen.currentService = ""
        screen.currentServiceOption1 = ""
        screen.currentServiceOption2 = ""
        switchIn.start()
    }

    StartView {
        id:startView
    }

    ServiceView {
        id:serviceView
    }

    ServiceOptionDialog {
            id: serviceOptionDialog
//            z: 10
    }

    property variant switchOut :
        ParallelAnimation {
            NumberAnimation {
                    target: currentView;
                    property: "x";
                    easing.type: Easing.Linear
                    to: -800
                    duration: 300
            }
            NumberAnimation {
                    target: currentView;
                    property: "opacity";
                    easing.type: Easing.Linear
                    from:1
                    to: 0
                    duration: 300
            }
    }

    property variant switchIn :
        ParallelAnimation {
            NumberAnimation {
                    target: targetView;
                    property: "x";
                    easing.type: Easing.Linear
                    to: 0
                    duration: 300
            }
            NumberAnimation {
                    target: targetView;
                    property: "opacity";
                    easing.type: Easing.Linear
                    from:0
                    to: 1
                    duration: 300
            }
    }

    property variant switchUp :
        ParallelAnimation {
            NumberAnimation {
                    target: targetView;
                    property: "y";
                    easing.type: Easing.Linear
                    from: -800
                    to: 0
                    duration: 300
            }
            NumberAnimation {
                    target: targetView;
                    property: "opacity";
                    easing.type: Easing.Linear
                    from:0
                    to: 1
                    duration: 300
            }
    }

    property variant switchDown :
        ParallelAnimation {
            NumberAnimation {
                    target: currentView;
                    property: "y";
                    easing.type: Easing.Linear
                    from:0
                    to: -800
                    duration: 300
            }
            NumberAnimation {
                    target: currentView;
                    property: "opacity";
                    easing.type: Easing.Linear
                    from:1
                    to: 0
                    duration: 300
            }
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
