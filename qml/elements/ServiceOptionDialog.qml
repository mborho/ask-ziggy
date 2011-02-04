import Qt 4.7
import "../js/serviceOptions.js" as Options

Rectangle {
    id: serviceOptionDialog
    height: parent.height
    width: parent.width //dialogText.width + 20
    opacity: 0
    color: screen.gradientColorEnd
    anchors.centerIn: parent
    border.color: "black"
    border.width: 10

    property string selected_ident: ""

    function show(name) {        
        serviceOptionDialog.selected_ident = name
        serviceOptionDialog.opacity = 1;
        add_option(name);
    }

    function hide() {
        serviceOptionDialog.opacity = 0;
    }

    function add_option(option_name) {
        var sOptions = Options.ServiceOptions.get(option_name,-1,'');
        serviceOptionModel.clear()
        for(var opt in sOptions) {
            serviceOptionModel.append({
                "ident": opt,
                "name": sOptions[opt],
            })
        }
    }

    Rectangle {
        color: screen.gradientColorStart
        height: parent.height -30
        width: parent.width -30
        anchors.centerIn: parent
        clip:true

        BorderShadow {}

        BorderShadow {
            y:parent.height
            transform: Rotation { origin.x: parent.width/2-15; origin.y: 0; angle: 180}
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
            height:parent.height
            boundsBehavior:Flickable.DragOverBounds
        }

        Component {
            id: serviceOptionDelegate
            Item {
                width: parent.width
                height: 40
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
                        onReleased: parent.optionClicked(ident, name)
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
                    function optionClicked(ident, name) {
                        serviceOptionDialog.hide()
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