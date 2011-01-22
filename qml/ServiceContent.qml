import Qt 4.7

Rectangle {
    id: serviceContent
    width: parent.width
    height: parent.height-50
    property variant apiResponse: ''

    Text {
        text: getStartText();
        wrapMode:Text.WrapAtWordBoundaryOrAnywhere
    }

    function getStartText() {
        if(apiResponse != '') {
            return JSON.stringify(apiResponse);
        }
        return ''
    }
}
