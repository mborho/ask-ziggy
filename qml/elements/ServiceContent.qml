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
        hideShadows()
        serviceContentList.visible = false;
        serviceContentText.visible = true;
    }

    function renderResultList() {
        serviceContentText.visible = false;
        serviceContentList.visible = true;
        serviceContentListModel.clear()
        hideShadows()
        for(var x in apiResponse) {
            var row = apiResponse[x]
            serviceContentListModel.append({
                "url": decodeURIComponent(row['url']),
                "title": row['title'],
                "content": row['content']
            })
        }
    }

    function hideShadows() {
        borderShadowTop.opacity = 0
        borderShadowBottom.opacity = 0
    }

    function showShadows() {
        if(borderShadowTop.opacity == 0) {
            showShadowsAnimation.start()
        }
    }

    property variant showShadowsAnimation :
        ParallelAnimation {
            NumberAnimation {
                    target: borderShadowTop
                    property: "opacity";
                    easing.type: Easing.OutQuad
                    to: 1
                    duration: 200
            }
            NumberAnimation {
                target: borderShadowBottom
                property: "opacity";
                easing.type: Easing.OutQuad
                to: 1
                duration: 200
            }
        }

    BorderShadow {
        id:borderShadowTop
    }

    BorderShadow {
        id:borderShadowBottom
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
            onMovementStarted:showShadows()
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
//                    color: screen.gradientColorStart
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: "#EDEDED" }
                        GradientStop { position: 0.04; color: "#E0E0E0"}
                        GradientStop { position: 0.96; color: "#E0E0E0"}
                        GradientStop { position: 1.0; color: "#EDEDED" }
                    }
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
                            height: 1
                            width:parent.width
                            color:screen.gradientColorEnd
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
