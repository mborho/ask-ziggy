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
            if(screen.currentService == "music") {
                myJSON = handle_music(myJSON);
            }
            serviceView.apiResponse = myJSON;
            serviceContent.renderResultList()
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
