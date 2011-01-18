function showHistory() {
    serviceOptionDialog.show(screen.currentService)
}

function showSettings() {
    serviceOptionDialog.show(screen.currentService)
}

function toolbarFuncCaller(name) {
    console.log(name)
    eval(name)()
}

function selectInputOption() {
    serviceOptionDialog.show(screen.currentService)
}

function selectInputTlateFrom() {
    serviceOptionDialog.show('tlate_from')
}

function selectInputTlateTo() {
    serviceOptionDialog.show('tlate_to')
}

function askZiggy() {
    console.log("ask ziggy")
    console.log(screen.currentService)
    console.log(screen.currentServiceOption1)
}
