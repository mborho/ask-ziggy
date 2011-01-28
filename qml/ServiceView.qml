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

        ServiceInput {
            id:serviceInput
            visible:false;
        }

        ServiceInputTlate {
            id:serviceInputTlate
            visible:false;
        }

        ServiceInputDeli {
            id:serviceInputDeli
            visible:false;
        }

        ServiceInputMetacritic {
            id:serviceInputMetacritic
            visible:false;
        }

        ServiceContent {
            id:serviceContent
        }

        ServiceToolbar {
            id:serviceToolbar
        }
    }

    function loadServiceView(command) {
        apiResponse = ''
        serviceInputText = ''
        serviceInput.visible = false;
        serviceInputTlate.visible = false;
        serviceInputMetacritic.visible = false;
        serviceInputDeli.visible = false;
        serviceContent.height = height-serviceInput.height-serviceToolbar.height
        if(command == "tlate") {
            optionText1 = 'To'
            optionText2 = 'From'
            serviceInputTlate.visible = true;
            serviceInputTlate.focus = true
            serviceContent.height = height-serviceInputTlate.height-serviceToolbar.height
        } else if(command == "deli") {
            serviceInputDeli.visible = true;
            serviceInputDeli.focus = true
        } else if(command=="metacritic"){
            serviceInputMetacritic.visible = true;
            serviceInputMetacritic.focus = true
        } else {
            optionText1 = 'Language'
            serviceInput.visible = true;
            serviceInput.focus = true
        }
    }
    function clearResult() {
        serviceContent.clearResultList()
        serviceContent.clearResultText()
    }
}
