import os
import sys
import traceback

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from GOF import GOF


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Game of Life")
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
        self.scaleMultiplier = 7
        # Gen default canvas array (all false)
        self.cellState = [[False for i in range(self.width)] for j in range(self.height)]
        self.overpopulation = 3
        self.underpopulation = 2
        self.reproduction = 3
        self.infoLayout = infoLayout()
        self.savePatternLayout = savedPatterLayout(self)

        # Auto play thread
        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.autoPlay)

        # Main layout
        layout = QVBoxLayout()

        # pattern buttons
        self.infoLayout.randomBtn.clicked.connect(self.randomPattern)
        self.infoLayout.clearBtn.clicked.connect(self.clearCanvas)
        self.infoLayout.saveBtn.clicked.connect(self.savePattern)

        # Canvas
        self.pixelmap = QLabel()
        self.image = self.createImg()
        canvas = QPixmap(self.image).scaled(self.width * self.scaleMultiplier, self.height * self.scaleMultiplier,
                                            QtCore.Qt.KeepAspectRatio)

        self.pixelmap.setPixmap(canvas)
        self.pixelmap.mousePressEvent = self.userDraw
        layout.addWidget(self.pixelmap)

        # game buttons
        self.infoLayout.playBtn.clicked.connect(self.play)
        self.infoLayout.pauseBtn.clicked.connect(self.pause)
        self.infoLayout.stepBtn.clicked.connect(self.step)

        # Slider
        self.infoLayout.timeSlider.valueChanged[int].connect(self.timerFunction)

        #Main layout
        hLayout = QHBoxLayout()
        hLayout.addLayout(layout)
        hLayout.addLayout(self.infoLayout)
        hLayout.addLayout(self.savePatternLayout)
        self.setLayout(hLayout)

    def createImg(self):
        image = QImage(self.width, self.height, QImage.Format_ARGB32)
        for x in range(image.width()):
            for y in range(image.height()):
                if self.cellState[y][x]:
                    image.setPixel(x, y, QColor(Qt.black).rgb())
                else:
                    image.setPixel(x, y, QColor(Qt.white).rgb())

        return image

    def userDraw(self, event):
        x = int(event.pos().x() / self.scaleMultiplier)
        y = int(event.pos().y() / self.scaleMultiplier)
        if self.cellState[y][x]:
            self.cellState[y][x] = False
        else:
            self.cellState[y][x] = True
        self.updateCanvas()

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
        gof = GOF(self.cellState, self.overpopulation, self.underpopulation, self.reproduction)
        self.cellState = gof.newCellState()
        self.updateCanvas()

    def timerFunction(self):
        self.timer.setInterval(self.infoLayout.timeSlider.value())
        self.infoLayout.timeLabel.setText(str(self.infoLayout.timeSlider.value()))

    def randomPattern(self):
        self.cellState = np.random.choice(a=[False, True], size=(self.width, self.height))
        self.updateCanvas()

    def clearCanvas(self):
        self.cellState = [[False for i in range(self.width)] for j in range(self.height)]
        self.updateCanvas()

    def savePattern(self):
        self.image.save(f"patterns/{self.infoLayout.filename.text()}.png")
        self.savePatternLayout.update()


class infoLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        ####
        patternLayout = QVBoxLayout()
        self.randomBtn = QPushButton("Random pattern")
        patternLayout.addWidget(self.randomBtn)

        self.clearBtn = QPushButton("Clear canvas")
        patternLayout.addWidget(self.clearBtn)

        self.filename = QLineEdit()
        self.filename.setPlaceholderText("File name")
        self.filename.setStyleSheet("color : black")
        patternLayout.addWidget(self.filename)

        self.saveBtn = QPushButton("Save pattern")
        patternLayout.addWidget(self.saveBtn)

        self.addLayout(patternLayout)
        #### end pattern layout

        ####
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

        ####

        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setValue(200)
        self.timeSlider.setTickInterval(10)
        self.timeSlider.setSingleStep(10)
        self.timeSlider.setMinimum(1)
        self.timeSlider.setMaximum(500)

        self.timeLabel = QLabel()
        self.timeLabel.setText(str(self.timeSlider.value()))

        sliderlayout = QVBoxLayout()
        sliderlayout.addWidget(self.timeLabel)
        sliderlayout.addWidget(self.timeSlider)
        self.addLayout(sliderlayout)
        ####


class savedPatterLayout(QVBoxLayout):
    def __init__(self, mainWidget):
        super().__init__()
        self.mainWidget = mainWidget
        self.update()
        self.setAlignment(Qt.AlignTop)

    def update(self):
        # for i in reversed(range(self.count())):
        #     self.itemAt(i).widget().setParent(None)
        patterns = {}
        for filename in os.listdir("patterns"):
            patterns[filename] = (QImage(f"patterns/{filename}"))
        tempLayout = QVBoxLayout()

        for filename, pattern in patterns.items():
            pixmap = QLabel()
            pixmap.setPixmap(QPixmap(pattern))
            pixmap.mousePressEvent = lambda checked, pattern=pattern: self.genArray(pattern)
            tempLayout.addWidget(QLabel(filename))
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
        cellState = []
        for x in range(image.width()):
            cellX = []
            for y in range(image.height()):
                color = image.pixelColor(y, x).name()
                if color == "#ffffff":
                    cellX.append(False)
                else:
                    cellX.append(True)
            cellState.append(cellX)
        self.mainWidget.cellState = cellState
        self.mainWidget.updateCanvas()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec_())
