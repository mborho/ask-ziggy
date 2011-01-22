import Qt 4.7

Column {
    id: serviceView
    parent: screen
    width: screen.width
    height: screen.height
    visible: false

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

    function loadServiceView(command) {
        serviceInput.visible = false;
        serviceInputTlate.visible = false;
        serviceInputMetacritic.visible = false;
        serviceInputDeli.visible = false;
        if(command == "tlate") {
            serviceInputTlate.visible = true;
        } else if(command == "deli") {
            serviceInputDeli.visible = true;
        } else if(command=="metacritic"){
            serviceInputMetacritic.visible = true;
        } else {
            serviceInput.visible = true;
        }
        serviceView.visible = true;
    }

}
