import Qt 4.7

Rectangle {
    id: serviceContent
    width: parent.width
    height: parent.height-50
    z:-1
    property variant apiResponse: ''
    color: screen.gradientColorStart
    Text {
        id:serviceContentText
        text: getStartText();
        height:parent.height
        width:parent.width
        wrapMode:Text.WrapAtWordBoundaryOrAnywhere
        color: "black"
        verticalAlignment: Text.AlignTop
        horizontalAlignment: Text.AlignLeft
    }

    function getStartText() {
//        if(apiResponse != '') {
//            return JSON.stringify(apiResponse);
//        }
        return ''
    }

    function renderResultText(result_txt) {
        serviceContentText.text = result_txt
        serviveContentListView.visible = false;
        serviceContentText.visible = true;
    }

    function renderResultList() {
        serviceContentText.visible = false;
        serviveContentListView.visible = true;
        serviceContentList.clear()
        for(var x in apiResponse) {
            var row = apiResponse[x]
            serviceContentList.append({
                "url": decodeURIComponent(row['url']),
                "title": row['title'],
                "content": row['content']
            })
        }
    }

    ListModel {
        id: serviceContentList
    }

    ListView {
        id: serviveContentListView
        anchors.fill: parent
        model: serviceContentList
        delegate: serviceContentDelegate
        focus: true
        height:parent.height
    }

    Component {
        id: serviceContentDelegate
        Item {
            width: parent.width
            height: childrenRect.height
            Rectangle {
                id: column

                border.color: "black"
                border.width:3

                radius: 5
                width: parent.width
                height: childrenRect.height
                color: screen.gradientColorStart
                Column {
                    id: delegatorColumn
                    x:10
                    y:10
                    anchors.rightMargin:10
                    width:parent.width
                    Text {
                        text: '<b>'+title+'</b>'
                        width:parent.width-15
                        wrapMode:Text.WordWrap
                    }
                    Text {
                        text: '<a href="'+url+'">'+url+'</a>'
                        width:parent.width-15
//                        elide:Text.ElideRight
                        wrapMode:Text.WrapAnywhere
//                        onLinkActivated: console.log(link + " link activated")
                    }
                    Text {
                        text:content
//                        style: Text.Normal
                        wrapMode:Text.WordWrap
                        width:parent.width-15
                    }
                }
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    onReleased: parent.entryClicked(url)
                }
//                gradient: Gradient {
//                    GradientStop {id:stop1;position: 0;color: screen.gradientColorStart}
//                    GradientStop {id:stop2;position: 1;color: screen.gradientColorEnd}
//                }
                states: [
                    State {
                        name: 'clicked'
                        when: mouseArea.pressed
                        PropertyChanges { target: column; color:screen.gradientColorEnd}
//                        PropertyChanges { target: stop2; position:0 }
                    }
                ]
                function entryClicked(url) {
                    console.log(url)
                }
            }
        }
    }
}
