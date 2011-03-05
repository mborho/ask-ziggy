import Qt 4.7

Rectangle {
    width:parent.width/3
    height: parent.height

    gradient: Gradient {
        GradientStop {id:settings1;position: 0;color: screen.gradientColorStart}
        GradientStop {id:settings2;position: 1;color: screen.gradientColorEnd}
    }
}
