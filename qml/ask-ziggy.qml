import Qt 4.7
import "Ziggy.js" as Ziggy

Rectangle {
    id: screen;
    width: 800
    height: 424
//    width: (runtime.orientation == Orientation.Landscape) ? 800 : 424
//    height: (runtime.orientation == Orientation.Landscape) ? 800 : 424

    property string apiUrl: 'http://ask-ziggy.appspot.com/api/query?&term=';
    property string gradientColorStart: "lightgrey"
    property string gradientColorEnd: "grey"
    property string currentService: ""
    property string currentServiceOption1: ""
    property string currentServiceOption2: ""
    property Item currentView
    property Item targetView

    states: [State {
        name: "landscape"
        PropertyChanges { target: screen; width: 424; height: 8000 }
        }
//        State {
//            name: "portrait"
//            PropertyChanges { target: screen; width: 480; height: 800 }
//        }
    ]
    state: (runtime.orientation == Orientation.Landscape) ? 'landscape' : ''

    function showServiceView(command, input) {
        screen.currentService = command;
        currentView = startView
        targetView = serviceView
        Ziggy.loadServiceView(command, input)
        switchAnimation.start()
        console.log(screen.state)
        console.log(Orientation.Landscape)
        console.log(screen.width)
        console.log(screen.height)
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
