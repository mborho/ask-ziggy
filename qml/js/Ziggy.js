/**
 BaaS wrapper
 */
function getTextInput() {
    var text = serviceView.serviceInput.inputText
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

function handle_tlate(data) {
    var content = data['text']+' ('+data['detected_lang']+' => '+data['lang']+')';
    return content;
}

function handle_weather(data) {
    var content = '<img src="http://google.com'+data['current']['icon']+'" alt="" class="weather_icon" />';
    content += '<div>'+data['info']['city']+'</div>';
    if(data['current']['condition'])
        content += '<div>'+data['current']['condition']+'</div>';
    content += '<div>'+data['current']['temp_c']+'°C/'+data['current']['temp_f']+'°F</div>';
    content += '<div>'+data['current']['humidity']+'<br/>'+data['current']['wind_condition']+'</div><br/>';
    var fore = data['forecast'];
    for(var f in fore) {
          var fcast = '<div class="weather_fcast">';
          fcast += '<img src="http://google.com'+fore[f]['icon']+'" alt="" />';
          fcast += '<span>'+fore[f]['day_of_week']+': '+fore[f]['condition']+
          ' ('+fore[f]['low']+'°/'+fore[f]['high']+'°)</span>'
          content += fcast;
    }
    return content;
}

function handle_music(data) {
    var _extract_hits = function(res) {
      if(res['name']) return [res];
      else return res;
    }
    var _get_artist = function(row) {
      if(row['Artist'][0]) return row['Artist'][0];
      else return row['Artist'];
    }
    var list = Array();
    if(data['Artist']) {
        var artists = _extract_hits(data['Artist']);
        for(var a in artists) {
            var entry = Object();
            entry['url'] = decodeURIComponent(artists[a]['url']);
            entry['title'] = artists[a]['name'];
            entry['content'] = '';
            list[a] = entry;
      }
    } else if (data['Release']) {
        var releases = _extract_hits(data['Release']);
        for(var r in releases) {
            var entry = Object();
            entry['url'] = decodeURIComponent(releases[r]['url']);
            var artist = _get_artist(releases[r])
            entry['title'] = '"'+releases[r]['title']+'" by '+artist['name'];
            entry['content'] = 'Year: '+releases[r]['releaseYear']+'<br/>Label: '+releases[r]['label'];
            list[r] = entry;
        }
        console.log(list);
    } else if (data['Track']) {
        var tracks = _extract_hits(data['Track']);
        for(var t in tracks) {
            var entry = Object();
            entry['url'] = decodeURIComponent(tracks[t]['url']);
            var artist = _get_artist(tracks[t])
            entry['title'] = '"'+tracks[t]['title']+'" ('+tracks[t]['releaseYear']+') by '+artist['name'];
            var content = ''
            try {
                var album = tracks[t]['Album']['Release'];
                if(album['title']) content += 'Album: '+album['title'];
                if(album['label']) content += '<br/>Label: '+ album['label'];
            } catch(err) {};
            entry['content'] = content;
            list[t] = entry;
        }
    }
    return list;
}


function doApiCall(term) {
    var doc = new XMLHttpRequest();
    var url = screen.apiUrl+encodeURIComponent(term)
    console.log(url)
    doc.onreadystatechange = function() {
        if (doc.readyState == XMLHttpRequest.DONE) {
            var responseText = doc.responseText.replace(/^\ ?\(/, '').replace(/\)$/, '');
            var myJSON = JSON.parse(responseText);
            if(screen.currentService == "tlate") {
                var text =  handle_tlate(myJSON);
                serviceView.serviceContent.renderResultText(text)
            } else if(screen.currentService == "weather") {
                var text =  handle_weather(myJSON);
                serviceView.serviceContent.renderResultText(text)
            } else {
                if(screen.currentService == "music") {
                    myJSON = handle_music(myJSON);
                }
                serviceView.serviceContent.apiResponse = myJSON;
                serviceView.serviceContent.renderResultList();
           }
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

var serviceViewColumn;
var serviceInput;
var serviceContent;
var serviceToolbar;

function loadServiceView(command, input) {

    if(serviceInput) {
        serviceInput.destroy()
        serviceContent.destroy()
        serviceToolbar.destroy()
        serviceViewColumn.destroy()
    }

    serviceViewColumn = Qt.createQmlObject('import Qt 4.7; Column {id:serviceViewColumn;parent:serviceView; width: parent.width;height: parent.height}', serviceView, 'serviceViewColumn');

    if(command == "tlate") {
        serviceView.optionText1 = 'To'
        serviceView.optionText2 = 'From'
    } else {
        serviceView.optionText1 = 'Language'
    }

    var inputComponent = Qt.createComponent('elements/'+input+'.qml')
    serviceInput = inputComponent.createObject(serviceViewColumn)
    serviceView.serviceInput = serviceInput

    var toolbarComponent = Qt.createComponent('elements/ServiceToolbar.qml');
    serviceToolbar = toolbarComponent.createObject(serviceViewColumn)
    serviceView.serviceToolbar = serviceToolbar


    var contentComponent = Qt.createComponent('elements/ServiceContent.qml');
    serviceContent = contentComponent.createObject(serviceViewColumn)
    serviceView.serviceContent = serviceContent

}

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

