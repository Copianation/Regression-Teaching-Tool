from PyQt5.QtWidgets import (QPushButton, QGroupBox,
        QVBoxLayout)

def btn_factory(name, func):
    btn = QPushButton(name)
    btn.clicked.connect(func)
    return btn


def group_box_factory(group_name, *buttons):
    groupBox = QGroupBox(group_name)
    layout = QVBoxLayout()
    for button in buttons:
        layout.addWidget(button)
    groupBox.setLayout(layout)
    return groupBox