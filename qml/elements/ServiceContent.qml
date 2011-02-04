import Qt 4.7

Rectangle {
    id: serviceContent
    width: serviceView.width
    z:-1
    property variant apiResponse: ''
    color:screen.gradientColorStart
    height: serviceView.height-serviceView.serviceInput.height-serviceView.serviceToolbar.height
    anchors.topMargin: serviceView.serviceInput.height
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


    BorderShadow {}

    BorderShadow {
        y:parent.height
        transform: Rotation { origin.x: serviceContentList.width/2; origin.y: 0; angle: 180}
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
                    width: parent.width
                    height: childrenRect.height
                    color: screen.gradientColorStart
                    Column {
                        id: delegatorColumn
                        height: childrenRect.height
                        width:parent.width
                        Text {
                            text: '<b>'+title+'</b>'
                            width:parent.width-25
                            wrapMode:Text.WordWrap
                            x:10
                        }
                        Text {
                            text: '<a href="'+url+'">'+url+'</a>'
                            width:parent.width-15
                            x:10
                            elide:Text.ElideLeft
//                            wrapMode:Text.WrapAnywhere
                        }
                        Text {
                            text:content
                            x:10
                            wrapMode:Text.WordWrap
                            width:parent.width-15
                            visible: (content) ? true : false
                        }

                        Rectangle {
                            height: 2
                            width:parent.width
                            color:"black"
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
