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
    }

    ServiceContent {
        id:serviceContent
    }

    function showHistory() {
        serviceOptionDialog.show("show history")
    }

    function showSettings() {
        serviceOptionDialog.show("show settings")
    }

    function toolbarFuncCaller(name) {
        eval(name)()
    }

    function selectInputOption() {
        serviceOptionDialog.show("service_option")
    }

    function askZiggy() {
        console.log("ask ziggy")
        console.log(screen.currentService)
        console.log(screen.currentServiceOption1)
    }

}
