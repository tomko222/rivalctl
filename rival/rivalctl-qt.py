from PySide.QtGui import QApplication, QPushButton, QColorDialog, QWidget, QLabel, QColor, QGridLayout, QSpinBox, \
    QComboBox
import sys
import PySide.QtCore
from rival import *
from rivalctl import send_reports


class ColorArea(QLabel):
    clicked = PySide.QtCore.Signal()
    color = QColor(255, 24, 0)

    def __init__(self):
        super(ColorArea, self).__init__()
        self.setStyleSheet("border: 1px solid black; background: "+self.color.name())
        self.setAutoFillBackground(True)
        self.setFixedHeight(40)
        self.setFixedWidth(60)

    def mousePressEvent(self, event):
        self.clicked.emit()

    def choose_color(self):
        color = QColorDialog().getColor()
        if color.isValid():
            self.color = color
            self.setStyleSheet("border: 1px solid black; background: "+color.name())

    def get_color(self):
        return self.color


def reset_slot():
    reset_report = []
    reset_report = FACTORY_PROFILE.to_report_list()
    send_reports(reset_report)


def save_slot():
    reports = []
    reports.append(set_logo_color(logo_color_area.get_color().name()))
    reports.append(set_logo_style(logo_style_combo_box.currentIndex()+1))
    reports.append(set_wheel_color(wheel_color_area.get_color().name()))
    reports.append(set_wheel_style(wheel_style_combo_box.currentIndex()+1))
    reports.append(set_cpi_1(int(cpi_one_spin_box.value())))
    reports.append(set_cpi_2(int(cpi_two_spin_box.value())))
    reports.append(set_polling_rate(int(polling_rate_combo_box.currentText())))
    reports.append(commit())
    send_reports(reports)


app = QApplication(sys.argv)
layout = QGridLayout()

# wheel_color
wheel_color_label = QLabel("Wheel color:")
layout.addWidget(wheel_color_label, 0, 0)
wheel_color_area = ColorArea()
layout.addWidget(wheel_color_area, 0, 1)
wheel_color_area.clicked.connect(wheel_color_area.choose_color)

# wheel_style
wheel_style_label = QLabel("Wheel style:")
layout.addWidget(wheel_style_label, 0, 2)
wheel_style_combo_box = QComboBox()  # Value+1 !!! 0 - turned off?
wheel_style_combo_box.addItem("Steady")
wheel_style_combo_box.addItem("Slow breath")
wheel_style_combo_box.addItem("Middle breath")
wheel_style_combo_box.addItem("Fast breath")
layout.addWidget(wheel_style_combo_box, 0, 3)

# logo_color
logo_color_label = QLabel("Logo color:")
layout.addWidget(logo_color_label, 1, 0)
logo_color_area = ColorArea()
layout.addWidget(logo_color_area, 1, 1)
logo_color_area.clicked.connect(logo_color_area.choose_color)

# logo_style
logo_style_label = QLabel("Logo style:")
layout.addWidget(logo_style_label, 1, 2)
logo_style_combo_box = QComboBox()  # Value+1 !!! 0 - turned off?
logo_style_combo_box.addItem("Steady")
logo_style_combo_box.addItem("Slow breath")
logo_style_combo_box.addItem("Middle breath")
logo_style_combo_box.addItem("Fast breath")
layout.addWidget(logo_style_combo_box, 1, 3)

# cpi1
cpi_one_label = QLabel("CPI1 (800):")
layout.addWidget(cpi_one_label, 2, 0)
cpi_one_spin_box = QSpinBox()
cpi_one_spin_box.setRange(50, 6500)
cpi_one_spin_box.setValue(800)
cpi_one_spin_box.setSingleStep(50)
layout.addWidget(cpi_one_spin_box, 2, 1)

# cpi2
cpi_two_label = QLabel("CPI2 (1600):")
layout.addWidget(cpi_two_label, 2, 2)
cpi_two_spin_box = QSpinBox()
cpi_two_spin_box.setRange(50, 6500)
cpi_two_spin_box.setValue(1600)
cpi_two_spin_box.setSingleStep(50)
layout.addWidget(cpi_two_spin_box, 2, 3)

# polling_rate
polling_rate_label = QLabel("Polling rate (1000):")
layout.addWidget(polling_rate_label, 3, 0)
polling_rate_combo_box = QComboBox()
polling_rate_combo_box.addItem("1000")
polling_rate_combo_box.addItem("500")
polling_rate_combo_box.addItem("250")
polling_rate_combo_box.addItem("125")
layout.addWidget(polling_rate_combo_box, 3, 1)

save_push_button = QPushButton("Save settings")
save_push_button.clicked.connect(save_slot)
layout.addWidget(save_push_button, 4, 0)

reset_push_button = QPushButton("Reset to factory defaults")
# button_one.clicked.connect(color_area_one.choose_color)
layout.addWidget(reset_push_button, 4, 1)

central_widget = QWidget()
central_widget.setWindowTitle("Rivalctl-Qt")
central_widget.setLayout(layout)
central_widget.show()

app.exec_()