import Qt 4.7
import "options/serviceOptions.js" as Options

Rectangle {
    id: serviceOptionDialog
    height: parent.height
    width: parent.width //dialogText.width + 20
    opacity: 0
    color: screen.gradientColorStart
    anchors.centerIn: parent

    function show(option_name) {
        serviceOptionDialog.opacity = 0.7;
        add_option(option_name);
    }

    function hide() {
        serviceOptionDialog.opacity = 0;
    }


    function add_option(option_name) {
        var sOptions = Options.ServiceOptions.get(option_name,-1,'');
        console.log(sOptions);
        serviceOptionModel.clear()
        for(var opt in sOptions) {
            serviceOptionModel.append({
                "ident": opt,
                "name": sOptions[opt],
            })
        }
    }

//    Text {
//        id: dialogText
//        anchors.centerIn: parent
//        text: ""
//    }

//    MouseArea {
//        anchors.fill: parent
//        onClicked: hide();
//    }

    ListModel {
        id: serviceOptionModel
//        ListElement {
//            ident: 'option1'
//            name:'Option 1'
//        }
    }

    ListView {
        id: serviveOptionListView
        anchors.fill: parent
        model: serviceOptionModel
        delegate: serviceOptionDelegate
        focus: true

    }

    Component {
        id: serviceOptionDelegate
        Item {
            width: parent.width
            height: 40
            Rectangle {
                id: column
                width: parent.width - parent.width/8
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
                    onReleased: parent.optionClicked(ident)
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
                function optionClicked(ident) {
                    serviceOptionDialog.hide()
                    screen.currentServiceOption1 = ident
                }
            }

        }

    }    
}
