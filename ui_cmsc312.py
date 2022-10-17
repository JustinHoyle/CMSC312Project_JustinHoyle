
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
        MainWindow.resize(987, 598)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.loadButton = QPushButton(self.centralwidget)
        self.loadButton.setObjectName(u"loadButton")
        self.loadButton.setGeometry(QRect(40, 40, 75, 23))
        self.cycleCountInput = QLineEdit(self.centralwidget)
        self.cycleCountInput.setObjectName(u"cycleCountInput")
        self.cycleCountInput.setGeometry(QRect(40, 80, 75, 20))
        self.cycleCountInput.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.setCycleButton = QPushButton(self.centralwidget)
        self.setCycleButton.setObjectName(u"setCycleButton")
        self.setCycleButton.setGeometry(QRect(20, 110, 121, 23))
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(40, 160, 75, 23))
        self.resumeButton = QPushButton(self.centralwidget)
        self.resumeButton.setObjectName(u"resumeButton")
        self.resumeButton.setGeometry(QRect(40, 190, 75, 23))
        self.pauseButton = QPushButton(self.centralwidget)
        self.pauseButton.setObjectName(u"pauseButton")
        self.pauseButton.setGeometry(QRect(40, 220, 75, 23))
        self.proccessViewer = QTextBrowser(self.centralwidget)
        self.proccessViewer.setObjectName(u"proccessViewer")
        self.proccessViewer.setGeometry(QRect(170, 10, 441, 281))
        self.fileLoadedLabel = QLabel(self.centralwidget)
        self.fileLoadedLabel.setObjectName(u"fileLoadedLabel")
        self.fileLoadedLabel.setGeometry(QRect(10, 20, 131, 16))
        self.saveLogButton = QPushButton(self.centralwidget)
        self.saveLogButton.setObjectName(u"saveLogButton")
        self.saveLogButton.setGeometry(QRect(30, 270, 91, 23))
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(620, 190, 160, 101))
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

        self.cycleCountLabel = QLabel(self.verticalLayoutWidget_2)
        self.cycleCountLabel.setObjectName(u"cycleCountLabel")
        self.cycleCountLabel.setIndent(10)

        self.verticalLayout_2.addWidget(self.cycleCountLabel)

        self.processCountLabel = QLabel(self.verticalLayoutWidget_2)
        self.processCountLabel.setObjectName(u"processCountLabel")
        self.processCountLabel.setIndent(10)

        self.verticalLayout_2.addWidget(self.processCountLabel)

        self.resourcesLabel = QLabel(self.centralwidget)
        self.resourcesLabel.setObjectName(u"resourcesLabel")
        self.resourcesLabel.setGeometry(QRect(660, 170, 71, 16))
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(620, 30, 160, 131))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.newLabel = QLabel(self.verticalLayoutWidget)
        self.newLabel.setObjectName(u"newLabel")
        self.newLabel.setIndent(10)

        self.verticalLayout.addWidget(self.newLabel)

        self.readyLabel = QLabel(self.verticalLayoutWidget)
        self.readyLabel.setObjectName(u"readyLabel")
        self.readyLabel.setIndent(10)

        self.verticalLayout.addWidget(self.readyLabel)

        self.runLabel = QLabel(self.verticalLayoutWidget)
        self.runLabel.setObjectName(u"runLabel")
        self.runLabel.setIndent(10)

        self.verticalLayout.addWidget(self.runLabel)

        self.waitLabel = QLabel(self.verticalLayoutWidget)
        self.waitLabel.setObjectName(u"waitLabel")
        self.waitLabel.setIndent(10)

        self.verticalLayout.addWidget(self.waitLabel)

        self.exitLabel = QLabel(self.verticalLayoutWidget)
        self.exitLabel.setObjectName(u"exitLabel")
        self.exitLabel.setIndent(10)

        self.verticalLayout.addWidget(self.exitLabel)

        self.processStatesLabel = QLabel(self.centralwidget)
        self.processStatesLabel.setObjectName(u"processStatesLabel")
        self.processStatesLabel.setGeometry(QRect(650, 10, 91, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 987, 22))
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
        self.setCycleButton.setText(QCoreApplication.translate("MainWindow", u"Set Cycle Limit", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.resumeButton.setText(QCoreApplication.translate("MainWindow", u"Resume", None))
        self.pauseButton.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.fileLoadedLabel.setText(QCoreApplication.translate("MainWindow", u"File Loaded:", None))
        self.saveLogButton.setText(QCoreApplication.translate("MainWindow", u"Save Log", None))
        self.CPUpercent.setText(QCoreApplication.translate("MainWindow", u"CPU:", None))
        self.memoryUse.setText(QCoreApplication.translate("MainWindow", u"Memory:", None))
        self.cycleCountLabel.setText(QCoreApplication.translate("MainWindow", u"Cycle Count:", None))
        self.processCountLabel.setText(QCoreApplication.translate("MainWindow", u"Process Count:", None))
        self.resourcesLabel.setText(QCoreApplication.translate("MainWindow", u"Resources", None))
        self.newLabel.setText(QCoreApplication.translate("MainWindow", u"New: ", None))
        self.readyLabel.setText(QCoreApplication.translate("MainWindow", u"Ready: ", None))
        self.runLabel.setText(QCoreApplication.translate("MainWindow", u"Run: ", None))
        self.waitLabel.setText(QCoreApplication.translate("MainWindow", u"Wait: ", None))
        self.exitLabel.setText(QCoreApplication.translate("MainWindow", u"Exit: ", None))
        self.processStatesLabel.setText(QCoreApplication.translate("MainWindow", u"Process States", None))
    # retranslateUi