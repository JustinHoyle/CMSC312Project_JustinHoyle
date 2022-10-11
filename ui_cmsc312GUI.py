# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cmsc312GUIXesrlO.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTextBrowser, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(797, 344)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.loadButton = QPushButton(self.centralwidget)
        self.loadButton.setObjectName(u"loadButton")
        self.loadButton.setGeometry(QRect(40, 40, 75, 23))
        self.cycleCountInput = QLineEdit(self.centralwidget)
        self.cycleCountInput.setObjectName(u"cycleCountInput")
        self.cycleCountInput.setGeometry(QRect(40, 90, 75, 20))
        self.setCycleButton = QPushButton(self.centralwidget)
        self.setCycleButton.setObjectName(u"setCycleButton")
        self.setCycleButton.setGeometry(QRect(10, 110, 141, 23))
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(40, 160, 75, 23))
        self.pauseButton = QPushButton(self.centralwidget)
        self.pauseButton.setObjectName(u"pauseButton")
        self.pauseButton.setGeometry(QRect(40, 190, 75, 23))
        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setObjectName(u"stopButton")
        self.stopButton.setGeometry(QRect(40, 220, 75, 23))
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(620, 10, 160, 81))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.cycleCountLabel = QLabel(self.verticalLayoutWidget)
        self.cycleCountLabel.setObjectName(u"cycleCountLabel")
        self.cycleCountLabel.setIndent(10)

        self.verticalLayout.addWidget(self.cycleCountLabel)

        self.processCountLabel = QLabel(self.verticalLayoutWidget)
        self.processCountLabel.setObjectName(u"processCountLabel")
        self.processCountLabel.setIndent(10)

        self.verticalLayout.addWidget(self.processCountLabel)

        self.proccessViewer = QTextBrowser(self.centralwidget)
        self.proccessViewer.setObjectName(u"proccessViewer")
        self.proccessViewer.setGeometry(QRect(170, 10, 441, 281))
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(620, 130, 160, 161))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.CPUpercent = QLabel(self.verticalLayoutWidget_2)
        self.CPUpercent.setObjectName(u"CPUpercent")
        self.CPUpercent.setIndent(10)

        self.verticalLayout_2.addWidget(self.CPUpercent)

        self.memoryUse = QLabel(self.verticalLayoutWidget_2)
        self.memoryUse.setObjectName(u"memoryUse")
        self.memoryUse.setIndent(10)

        self.verticalLayout_2.addWidget(self.memoryUse)

        self.diskUse = QLabel(self.verticalLayoutWidget_2)
        self.diskUse.setObjectName(u"diskUse")
        self.diskUse.setIndent(10)

        self.verticalLayout_2.addWidget(self.diskUse)

        self.resourcesLLabel = QLabel(self.centralwidget)
        self.resourcesLLabel.setObjectName(u"resourcesLLabel")
        self.resourcesLLabel.setGeometry(QRect(670, 110, 71, 16))
        self.fileLoadedLabel = QLabel(self.centralwidget)
        self.fileLoadedLabel.setObjectName(u"fileLoadedLabel")
        self.fileLoadedLabel.setGeometry(QRect(10, 20, 121, 16))
        self.saveLogButton = QPushButton(self.centralwidget)
        self.saveLogButton.setObjectName(u"saveLogButton")
        self.saveLogButton.setGeometry(QRect(40, 270, 75, 23))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 797, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Operating System Simulator", None))
        self.loadButton.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.setCycleButton.setText(QCoreApplication.translate("MainWindow", u"Set Cycle Count", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pauseButton.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count:", None))
        self.processCountLabel.setText(QCoreApplication.translate("MainWindow", u"Processes Count:", None))
        self.CPUpercent.setText(QCoreApplication.translate("MainWindow", u"CPU:", None))
        self.memoryUse.setText(QCoreApplication.translate("MainWindow", u"Memory:", None))
        self.diskUse.setText(QCoreApplication.translate("MainWindow", u"Disk:", None))
        self.resourcesLLabel.setText(QCoreApplication.translate("MainWindow", u"Resources", None))
        self.fileLoadedLabel.setText(QCoreApplication.translate("MainWindow", u"File Loaded:", None))
        self.saveLogButton.setText(QCoreApplication.translate("MainWindow", u"Save Log", None))
    # retranslateUi

