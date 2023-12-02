from PyQt5.QtWidgets import (QPushButton, QGroupBox,
        QVBoxLayout, QWidget, QLayout, QGridLayout)

def btn_factory(name, func):
    btn = QPushButton(name)
    btn.clicked.connect(func)
    return btn


def group_box_factory(group_name, *buttons):
    groupBox = QGroupBox(group_name)
    layout = QVBoxLayout()
    for button in buttons:
        if isinstance(button, QWidget):
            layout.addWidget(button)
        if isinstance(button, QLayout):
            layout.addLayout(button)
    groupBox.setLayout(layout)
    return groupBox


def couple_layout(widget1, widget2):
    layout = QGridLayout()
    layout.addWidget(widget1, 0, 0)
    layout.addWidget(widget2, 0, 1)
    return layout