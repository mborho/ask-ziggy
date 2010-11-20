import Qt 4.7

Item {
    id: screen;

    function loadServiceView(command) {
        console.log(command)
        startView.visible =  false
        serviceView.visible = true
    }

    StartView {
        id:startView
    }

    ServiceView {
        id:serviceView
    }  
}
