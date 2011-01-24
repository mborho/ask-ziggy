function showHistory() {
    serviceOptionDialog.show(screen.currentService)
}

function showSettings() {
    serviceOptionDialog.show(screen.currentService)
}

function toolbarFuncCaller(name) {
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

function getTextInput() {
    var text = ''
    if(screen.currentService == "metacritic") {
        text = serviceView.serviceMetacriticText
    } else if(screen.currentService == "deli") {
        text = serviceView.serviceDeliText
    } else if(screen.currentService == "tlate") {
        text = serviceView.serviceTlateText
    } else {
        text = serviceView.serviceInputText
    }
    return text
}

function build_term() {
    var inputText = getTextInput()
    if(inputText == '') return ''
    var term = ''
    term += screen.currentService+':'
    term += inputText
    if(screen.currentServiceOption1 != '') {
        term += ' #'+screen.currentServiceOption1
    }
    if(screen.currentServiceOption2 != '') {
        term += ' @'+screen.currentServiceOption2
    }
    return term
}

function doApiCall(term) {
    var doc = new XMLHttpRequest();
    var url = screen.apiUrl+encodeURIComponent(term)
    console.log(url)
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            var responseText = doc.responseText.replace(/^\ ?\(/, '').replace(/\)$/, '');
            console.log(responseText)
            var myJSON = JSON.parse(responseText);
            serviceView.apiResponse = myJSON;
            serviceContent.renderResultList()
            //console.log(myJSON);
        }
    }
    doc.open("GET", url);
    doc.send();
}

function askZiggy() {
    var term = build_term()
    if(term != '') {
        console.log(term)
        doApiCall(term)
    }
}
