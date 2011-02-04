import Qt 4.7

Rectangle {
    id: serviceContent
    width: serviceView.width
    z:-1
    property variant apiResponse: ''
    color:screen.gradientColorStart

    height: serviceView.height-serviceView.serviceInput.height-serviceView.serviceToolbar.height
    anchors.top: serviceView.serviceInput.bottom
    anchors.topMargin: serviceView.serviceInput.height
    anchors.bottom: serviceView.serviceToolbar.top
    anchors.bottomMargin: serviceView.serviceToolbar.height
    anchors.fill: parent

    Text {
        id:serviceContentText
        text: getStartText();
        height:parent.height
        width:parent.width
        wrapMode:Text.WrapAtWordBoundaryOrAnywhere
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
        serviceContentList.visible = false;
        serviceContentText.visible = true;
    }

    function renderResultList() {
        serviceContentText.visible = false;
        serviceContentList.visible = true;
        serviceContentListModel.clear()
        for(var x in apiResponse) {
            var row = apiResponse[x]
            serviceContentListModel.append({
                "url": decodeURIComponent(row['url']),
                "title": row['title'],
                "content": row['content']
            })
        }
    }

    Rectangle {
        id:serviceContentList
        anchors.centerIn: parent
        height:parent.height
        width:parent.width
        visible: false
        color:screen.gradientColorStart

        ListModel {
            id: serviceContentListModel
        }

        ListView {
            id: serviveContentListView
            anchors.fill: parent
            model: serviceContentListModel
            delegate: serviceContentDelegate
            boundsBehavior:Flickable.DragOverBounds
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
                    states: [
                        State {
                            name: 'clicked'
                            when: mouseArea.pressed
                            PropertyChanges { target: column; color:screen.gradientColorEnd}
    //                        PropertyChanges { target: stop2; position:0 }
                        }
                    ]
                    function entryClicked(url) {
                        Qt.openUrlExternally ( url )
                        console.log(url)
                    }
                }
            }
        }
    }
}
