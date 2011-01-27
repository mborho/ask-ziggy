import Qt 4.7

Rectangle {
    id: serviceView
    parent: screen
    width: screen.width
    height: screen.height
    color: "lightgrey"
    opacity:0
    property string optionText1: "option 1"
    property string optionText2: "option 2"
    property alias serviceInputText: serviceInput.inputText
    property alias serviceTlateText: serviceInputTlate.inputText
    property alias serviceMetacriticText: serviceInputMetacritic.inputText
    property alias serviceDeliText: serviceInputDeli.inputText
    property alias apiResponse: serviceContent.apiResponse

    Column {
        id: serviceViewColumn
        width: parent.width
        height: parent.height

        ServiceToolbar {
            id:serviceToolbar
        }

        ServiceInput {
            id:serviceInput
            visible:false;
        }

        ServiceInputTlate {
            id:serviceInputTlate
            visible:false;
        }

        ServiceInputMetacritic {
            id:serviceInputMetacritic
            visible:false;
        }

        ServiceInputDeli {
            id:serviceInputDeli
            visible:false;
        }

        ServiceContent {
            id:serviceContent
        }

    }
    function loadServiceView(command) {
        apiResponse = ''
        serviceInputText = ''
        serviceInput.visible = false;
        serviceInputTlate.visible = false;
        serviceInputMetacritic.visible = false;
        serviceInputDeli.visible = false;
        if(command == "tlate") {
            optionText1 = 'To'
            optionText2 = 'From'
            serviceInputTlate.visible = true;
        } else if(command == "deli") {
            serviceInputDeli.visible = true;
        } else if(command=="metacritic"){
            serviceInputMetacritic.visible = true;
        } else {
            optionText1 = 'Language'
            serviceInput.visible = true;
        }
    }
}
