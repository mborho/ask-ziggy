import Qt 4.7
ListModel {
    id: serviceModel
    ListElement {
        command: 'tlate'
        name:'Translation'
        input:'ServiceInputTlate'
    }
    ListElement {
        command: 'weather'
        name:'Weather Forecast'
        input:'ServiceInput'
    }
    ListElement {
        command: 'music'
        name:'Yahoo Music'
        input:'ServiceInput'
    }
    ListElement {
        command: 'gnews'
        name:'Google News'
        input:'ServiceInput'
    }
    ListElement {
        command: 'gweb'
        name:'Google Search'
        input:'ServiceInput'
    }
    ListElement {
        command: 'deli'
        name:'Delicious.com'
        input:'ServiceInputDeli'
    }
    ListElement {
        command: 'metacritic'
        name:'Metacritic.com'
        input:'ServiceInputMetacritic'
    }
    ListElement {
        command: 'imdb'
        name:'IMDb.com'
        input:'ServiceInput'
    }
    ListElement {
        command: 'wikipedia'
        name:'Wikipedia'
        input:'ServiceInput'
    }
    ListElement {
        command: 'amazon'
        name:'Amazon'
        input:'ServiceInput'
    }
    ListElement {
        command: 'maemo'
        name:'Maemo.org'
        input:'ServiceInput'
    }
}
