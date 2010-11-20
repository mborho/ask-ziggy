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
        console.log("show history")
    }

    function showSettings() {
        console.log("show settings")
    }
}
