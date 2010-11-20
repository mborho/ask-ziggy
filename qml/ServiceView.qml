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

}
