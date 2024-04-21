# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QHBoxLayout,
    QHeaderView, QLayout, QPushButton, QSizePolicy,
    QTableView, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Main")
        Dialog.resize(700, 557)
        Dialog.setLayoutDirection(Qt.LeftToRight)
        Dialog.setAutoFillBackground(False)
        Dialog.setSizeGripEnabled(False)
        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 681, 541))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.table = QTableView(self.verticalLayoutWidget)
        self.table.setObjectName(u"table")

        self.verticalLayout.addWidget(self.table)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.selectDB = QComboBox(self.verticalLayoutWidget)
        self.selectDB.setObjectName(u"selectDB")

        self.horizontalLayout.addWidget(self.selectDB)

        self.selectTable = QComboBox(self.verticalLayoutWidget)
        self.selectTable.setObjectName(u"selectTable")

        self.horizontalLayout.addWidget(self.selectTable)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.show = QPushButton(self.verticalLayoutWidget)
        self.show.setObjectName(u"show")

        self.verticalLayout.addWidget(self.show)

        self.new_entry = QPushButton(self.verticalLayoutWidget)
        self.new_entry.setObjectName(u"new_entry")

        self.verticalLayout.addWidget(self.new_entry)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.show.setText(QCoreApplication.translate("Dialog", u"Load table", None))
        self.new_entry.setText(QCoreApplication.translate("Dialog", u"Create the new entry", None))
    # retranslateUi

