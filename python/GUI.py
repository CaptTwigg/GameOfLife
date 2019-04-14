import os
import sys

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from python.GOF import GOF


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Game of Life")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.mainWidget = mainWidget()
        self.setGeometry(0, 0, self.mainWidget.width * self.mainWidget.scaleMultiplier,
                         self.mainWidget.height * self.mainWidget.scaleMultiplier)
        FG = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        FG.moveCenter(cp)
        self.move(FG.topLeft())

        self.setCentralWidget(self.mainWidget)


class mainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.width, self.height = 100, 100
        self.scaleMultiplier = 7  # Scale image to better see whats going on ("Bigger" pixels)
        # Gen default canvas array (all false)
        self.cleanCanvas = [[False for i in range(self.width)] for j in range(self.height)]
        self.cellState = self.cleanCanvas

        # Rules
        self.overpopulation = 3
        self.underpopulation = 2
        self.reproduction = 3

        # Buttons and saved patterns layouts
        self.infoLayout = infoLayout()
        self.savePatternLayout = savedPatterLayout(self)

        # Auto play thread
        self.timer = QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.autoPlay)

        # Main layout
        layout = QVBoxLayout()

        # Canvas
        self.pixelmap = QLabel()
        self.updateCanvas()
        self.pixelmap.mousePressEvent = self.userDraw
        layout.addWidget(self.pixelmap)

        # pattern buttons
        self.infoLayout.randomBtn.clicked.connect(self.randomPattern)
        self.infoLayout.clearBtn.clicked.connect(self.clearCanvas)
        self.infoLayout.saveBtn.clicked.connect(self.savePattern)

        # game buttons
        self.infoLayout.playBtn.clicked.connect(self.play)
        self.infoLayout.pauseBtn.clicked.connect(self.pause)
        self.infoLayout.stepBtn.clicked.connect(self.step)

        # Rules fields
        self.infoLayout.overpopulation.valueChanged.connect(lambda newValue: self.setOverpopulation(newValue))
        self.infoLayout.overpopulation.setValue(self.overpopulation)

        self.infoLayout.underpopulation.valueChanged.connect(lambda newValue: self.setUnderpopulation(newValue))
        self.infoLayout.underpopulation.setValue(self.underpopulation)

        self.infoLayout.reproduction.valueChanged.connect(lambda newValue: self.setReproduction(newValue))
        self.infoLayout.reproduction.setValue(self.reproduction)

        # Slider
        self.infoLayout.timeSlider.valueChanged[int].connect(self.timerFunction)

        # Main layout
        hLayout = QHBoxLayout()
        hLayout.addLayout(layout)
        hLayout.addLayout(self.infoLayout)
        hLayout.addLayout(self.savePatternLayout)
        self.setLayout(hLayout)

    def userDraw(self, event):
        x = int(event.pos().x() / self.scaleMultiplier)
        y = int(event.pos().y() / self.scaleMultiplier)
        if self.cellState[y][x]:
            self.cellState[y][x] = False
        else:
            self.cellState[y][x] = True
        self.updateCanvas()

    def createImg(self):
        image = QImage(self.width, self.height, QImage.Format_ARGB32)
        for x in range(image.width()):
            for y in range(image.height()):
                if self.cellState[y][x]:
                    image.setPixel(x, y, QColor(Qt.black).rgb())
                else:
                    image.setPixel(x, y, QColor(Qt.white).rgb())

        return image

    def updateCanvas(self):
        self.image = self.createImg()
        canvas = QPixmap(self.image) \
            .scaled(self.width * self.scaleMultiplier, self.height * self.scaleMultiplier, QtCore.Qt.KeepAspectRatio)
        self.pixelmap.setPixmap(canvas)

    def step(self):
        gof = GOF(self.cellState, self.overpopulation, self.underpopulation, self.reproduction)
        self.cellState = gof.newCellState()
        self.updateCanvas()

    def play(self):
        self.timer.start()
        self.infoLayout.playBtn.hide()
        self.infoLayout.pauseBtn.show()

    def pause(self):
        self.timer.stop()
        self.infoLayout.playBtn.show()
        self.infoLayout.pauseBtn.hide()

    def autoPlay(self):
        self.step()

    def timerFunction(self):
        self.timer.setInterval(self.infoLayout.timeSlider.value())
        self.infoLayout.timeLabel.setText(str(self.infoLayout.timeSlider.value()) + " ms")

    def randomPattern(self):
        self.cellState = np.random.choice(a=[False, True], size=(self.width, self.height))
        self.updateCanvas()

    def clearCanvas(self):
        self.cellState = self.cleanCanvas
        self.updateCanvas()

    def savePattern(self):
        self.image.save(f"patterns/{self.infoLayout.filename.text()}.png")
        self.savePatternLayout.update()

    def setOverpopulation(self, value):
        self.overpopulation = value

    def setUnderpopulation(self, value):
        self.underpopulation = value

    def setReproduction(self, value):
        self.reproduction = value


class infoLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        spacing = 40

        #### Patternm, Random generator and save pattern
        patternLayout = QVBoxLayout()
        self.randomBtn = QPushButton("Random pattern")
        patternLayout.addWidget(self.randomBtn)

        self.clearBtn = QPushButton("Clear canvas")
        patternLayout.addWidget(self.clearBtn)

        patternLayout.addSpacing(20)

        self.filename = QLineEdit()
        self.filename.setPlaceholderText("File name")
        self.filename.setStyleSheet("color : black")
        patternLayout.addWidget(self.filename)

        self.saveBtn = QPushButton("Save pattern")
        patternLayout.addWidget(self.saveBtn)

        self.addLayout(patternLayout)
        #### end pattern layout

        self.addSpacing(spacing)

        #### Game buttons
        self.playBtn = QPushButton("play")
        self.pauseBtn = QPushButton("pause")
        self.pauseBtn.hide()
        self.stepBtn = QPushButton("step")

        gameBtnLayout = QHBoxLayout()
        gameBtnLayout.addWidget(self.playBtn)
        gameBtnLayout.addWidget(self.pauseBtn)
        gameBtnLayout.addWidget(self.stepBtn)
        self.addLayout(gameBtnLayout)
        ####

        self.addSpacing(spacing)

        #### Rules fields
        rulesLayout = QFormLayout()
        self.overpopulation = QSpinBox()
        self.underpopulation = QSpinBox()
        self.reproduction = QSpinBox()

        rulesLayout.addRow("Overpopulation   > ", self.overpopulation)
        rulesLayout.addRow("Underpopulation < ", self.underpopulation)
        rulesLayout.addRow("Reproduction      = ", self.reproduction)
        self.addLayout(rulesLayout)
        ####

        self.addSpacing(spacing)

        ####

        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setValue(20)
        self.timeSlider.setTickInterval(10)
        self.timeSlider.setSingleStep(10)
        self.timeSlider.setMinimum(10)
        self.timeSlider.setMaximum(500)

        self.timeLabel = QLabel()
        self.timeLabel.setMinimumWidth(50)
        self.timeLabel.setText(str(self.timeSlider.value()) + " ms")

        sliderlayout = QHBoxLayout()
        sliderlayout.addWidget(self.timeLabel)
        sliderlayout.addWidget(self.timeSlider)
        self.addLayout(sliderlayout)
        ####

        self.addSpacing(spacing)


class savedPatterLayout(QVBoxLayout):
    def __init__(self, mainWidget):
        super().__init__()
        self.mainWidget = mainWidget
        self.update()
        self.setAlignment(Qt.AlignTop)

    def update(self):
        for i in reversed(range(self.count())):
             self.itemAt(i).widget().setParent(None)
        patterns = {}
        for filename in os.listdir("patterns"):
            patterns[filename] = (QImage(f"patterns/{filename}"))
        tempLayout = QVBoxLayout()

        for filename, pattern in patterns.items():
            pixmap = QLabel()
            pixmap.setPixmap(QPixmap(pattern))
            pixmap.mousePressEvent = lambda checked, pattern=pattern: self.genArray(pattern)
            tempLayout.addWidget(QLabel(filename[0:-4]))
            tempLayout.addWidget(pixmap)
            tempLayout.addSpacerItem(QSpacerItem(0, 10))

        layoutWidget = QWidget()
        layoutWidget.setLayout(tempLayout)
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(False)
        scroll.setMinimumWidth(175)
        scroll.setWidget(layoutWidget)
        self.addWidget(scroll)

    def genArray(self, image):
        self.mainWidget.cellState = [
                [image.pixelColor(y, x).name() == "#000000" for y in range(image.height())]
                for x in range(image.width())
        ]
        self.mainWidget.updateCanvas()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec_())
