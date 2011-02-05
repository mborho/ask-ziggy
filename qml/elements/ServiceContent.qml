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

    function display_link(url, length) {
        if(url.length > length) return url.substring(0,length)+'...';
        else return url
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
                    gradient: Gradient {
                        GradientStop { id:fill1;position: 0.0; color: "#E9E9E9" }
                        GradientStop { id:fill2; position: 0.1; color: "#D7D7D7"}
                        GradientStop { id:fill3; position: 0.9; color: "#D7D7D7"}
                        GradientStop { id:fill4; position: 1.0; color: "#E9E9E9" }
                    }
                    Text {
                        id:resultText
                        anchors.top:  parent.top
                        anchors.topMargin: 10
                        text: '<b>'+title+'</b><br/><a href="'+url+'">'+display_link(url,40)+'</a><br/>'+content
                        width:parent.width-25
                        wrapMode:Text.WordWrap
                        x: 10
                    }
                    Rectangle {
                        anchors.top:  resultText.bottom
                        anchors.topMargin: 10
                        height: 2
                        width:parent.width
                        color:screen.gradientColorStart
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
//                            PropertyChanges { target: fill1; color:"#E0E0E0"}
                            PropertyChanges { target: fill1; color:"#D7D7D7"}
                            PropertyChanges { target: fill2; color:"#E9E9E9"}
                            PropertyChanges { target: fill3; color:"#E9E9E9"}
                            PropertyChanges { target: fill4; color:"#D7D7D7"}
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
