from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QListWidgetItem, QFrame, QSlider, QListWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QGroupBox)
from MyWidgets import  EffectWidget, ReverbLayout, DelayLayout
### THE GUI

class MainWindow(QWidget):
    def __init__(self, model):
        super().__init__()

        self.model = model

        self.init_ui()

    def init_ui(self):

        #Title
        self.setWindowTitle("Glovox")

        #GUI Elements
        self.effectList = QListWidget()
        self.effectList.addItem(QListWidgetItem('No Effect'))
        self.effectList.addItem(QListWidgetItem('Distorsion'))
        self.effectList.addItem(QListWidgetItem('Chorus'))
        self.effectList.addItem(QListWidgetItem('Auto-Wah'))
        self.effectList.setCurrentItem(self.effectList.item(0))


        #Effects List
        effectListLayout = QVBoxLayout()
        effectListLayout.addWidget(self.effectList)

        effectListBox = QGroupBox('Effects')
        effectListBox.setMinimumWidth(200)
        effectListBox.setLayout(effectListLayout)

        #Effects management: analyzer and parameters

        analyzerLayout = QVBoxLayout()
        analyzerBox = QGroupBox('Analyzer')
        analyzerBox.setLayout(analyzerLayout)

        effectParameterLayout = QHBoxLayout()

        effect = EffectWidget('Effect',ReverbLayout(self.model))
        rev = EffectWidget('Reverb',ReverbLayout(self.model))
        delay = EffectWidget('Delay',DelayLayout(self.model))

        effectParameterLayout.addWidget(effect)
        effectParameterLayout.addWidget(rev)
        effectParameterLayout.addWidget(delay)

        effectParameterBox = QWidget()
        effectParameterBox.setLayout(effectParameterLayout)


        effectManagementLayout = QVBoxLayout()
        effectManagementLayout.addWidget(analyzerBox)
        effectManagementLayout.addWidget(effectParameterBox)
       
        effectManagementWidget = QWidget()
        effectManagementWidget.setLayout(effectManagementLayout)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(effectListBox)
        mainLayout.addWidget(effectManagementWidget)
        self.setLayout(mainLayout)
        self.setMinimumSize(900, 600)

        self.show()


    def closeEvent(self, event):
        self.model.stop()

