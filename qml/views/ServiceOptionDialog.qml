import Qt 4.7
import "../elements"
import "../js/serviceOptions.js" as Options
import "../js/Appstate.js" as Appstate
import "../js/Ziggy.js" as Ziggy

Rectangle {
    id: serviceOptionDialog
    height: parent.height
    width: parent.width //dialogText.width + 20
    opacity: 1
    y:-800
    color: screen.gradientColorEnd
//    anchors.centerIn: parent

    property string selected_ident: ""

    function show(name) {
        serviceOptionDialog.selected_ident = name
        currentView = serviceView
        targetView = serviceOptionDialog
        add_option(name);
        screen.switchUp.start()
    }

    function showHistory(service, limit) {
        currentView = serviceView
        targetView = serviceOptionDialog
        serviceOptionModel.clear()
        var entries = Appstate.getHistoryEntries(service, limit);
        for(var opt in entries) {
            var parts = Ziggy.parseTerm(entries[opt].cmd);
            var name = parts[0]
            if(parts[1] != '') {
                var lang_name = Options.ServiceOptions.get(service, -1, parts[1]);
                if(lang_name != undefined) name += ' / '+ lang_name;
            }
            serviceOptionModel.append({
                "ident": entries[opt].cmd,
                "name": name,
                "type": 'history'
            })
        }
        screen.switchUp.start()
    }

    function hide() {
        targetView = serviceView
        currentView = serviceOptionDialog
        screen.switchDown.start()
    }

    function add_option(option_name) {
        var sOptions = Options.ServiceOptions.get(option_name,-1,'');
        serviceOptionModel.clear()
        for(var opt in sOptions) {
            serviceOptionModel.append({
                "ident": opt,
                "name": sOptions[opt],
                "type": "option"
            })
        }
    }

    RectangleButton {
        id:optionsDialogCancel
        width:parent.width
        height: screen.toolbarHeight
        clickAction: "serviceOptionDialog.hide"
        buttonText: "Cancel"
        anchors.bottom: parent.bottom
    }

    Rectangle {
        id:optionsListContainer
        color: screen.gradientColorStart
        height: parent.height-optionsDialogCancel.height-20
        width: parent.width-20
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: -25
        clip:true

        BorderShadow {}

        BorderShadow {
            y:parent.height
            transform: Rotation { origin.x: parent.width/2-10; origin.y: 0; angle: 180}
        }

        ListModel {
            id: serviceOptionModel
        }

        ListView {
            id: serviveOptionListView
            anchors.fill: parent
            anchors.topMargin: 10
            model: serviceOptionModel
            delegate: serviceOptionDelegate
            height:parent.height-screen.toolbarHeight
            boundsBehavior:Flickable.StopAtBounds
            flickDeceleration:screen.defaultFlickDeceleration
        }

        Component {
            id: serviceOptionDelegate
            Item {
                width: parent.width
                height: 60
                Rectangle {
                    id: column
                    width: parent.width/* - parent.width/8*/
                    height: parent.height
                    anchors.centerIn: parent
                    Column {
                        id: delegatorColumn
                        anchors.centerIn: parent
                        Text {
                            id: serviceOptionText
                            text: '<b>'+name+'</b> '
                        }
                    }
                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        onReleased: parent.optionClicked(ident, name, type)
                    }
                    gradient: Gradient {
                        GradientStop {id:stop1;position: 0;color: screen.gradientColorStart}
                        GradientStop {id:stop2;position: 1;color: screen.gradientColorEnd}
                    }
                    states: [
                        State {
                            name: 'clicked'
                            when: mouseArea.pressed
                            PropertyChanges { target: stop1; position:1}
                            PropertyChanges { target: stop2; position:0 }
                        }
                    ]
                    function optionClicked(ident, name, type) {
                        serviceOptionDialog.hide()
                        if(type == 'history') {
                            var parts = Ziggy.parseTerm(ident)
                            serviceView.serviceInput.inputText = parts[0]
                            if(parts[1] != '') {
                                screen.currentServiceOption1 = parts[1]
                                serviceView.optionText1 = Options.ServiceOptions.get(screen.currentService, -1, parts[1]);
                            } else {
                                screen.currentServiceOption1 = ""
                                serviceView.optionText1 = Options.ServiceOptions.getLabel(screen.currentService);
                            }
                            Ziggy.askZiggy();
                        } else {
                            if(serviceOptionDialog.selected_ident == "tlate_from") {
                                screen.currentServiceOption2 = ident
                                serviceView.optionText2 = name
                            } else {
                                screen.currentServiceOption1 = ident
                                serviceView.optionText1 = name
                            }
                        }
                    }
                }
            }
        }
    }
}
