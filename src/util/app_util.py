from PyQt5.QtWidgets import (QPushButton, QGroupBox,
        QVBoxLayout, QWidget, QLayout)

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