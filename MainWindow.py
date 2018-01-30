from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QListWidgetItem, QFrame, QSlider, QListWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QGroupBox)
from MyWidgets import  EffectWidget, MainEffectLayout, ReverbLayout, DelayLayout
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
        self.effectList.addItem(QListWidgetItem('Distortion'))
        self.effectList.addItem(QListWidgetItem('Auto-Wah'))
        self.effectList.addItem(QListWidgetItem('Harmonizer'))
        self.effectList.setCurrentItem(self.effectList.item(0))


        #Effects List
        effectListLayout = QVBoxLayout()
        effectListLayout.addWidget(self.effectList)

        effectListBox = QGroupBox('Effects')
        effectListBox.setMaximumWidth(300)
        effectListBox.setMinimumWidth(150)
        effectListBox.setLayout(effectListLayout)

        #Effects management: analyzer and parameters

        analyzerLayout = QVBoxLayout()
        analyzerBox = QGroupBox('Analyzer')
        analyzerBox.setLayout(analyzerLayout)

        effectParameterLayout = QHBoxLayout()

        self.effect = EffectWidget('Effect', MainEffectLayout(self.model))
        self.rev = EffectWidget('Reverb', ReverbLayout(self.model))
        self.delay = EffectWidget('Delay', DelayLayout(self.model))

        effectParameterLayout.addWidget(self.effect)
        effectParameterLayout.addWidget(self.rev)
        effectParameterLayout.addWidget(self.delay)

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
        self.setMinimumSize(950, 600)

        self.show()

        self.effectList.itemSelectionChanged.connect(self.changeEffect)

    def closeEvent(self, event):
        self.model.stop()

    def changeEffect(self):
        if self.effectList.currentItem().text() == 'No Effect':
            self.effect.getLayout().changeEffect('No Effect')
            self.model.switchToNoEff()

        elif self.effectList.currentItem().text() == 'Distortion':
            self.effect.getLayout().changeEffect('Distortion')
            self.effect.getLayout().currentWidget().reset()
            self.model.switchToDistortion()

        elif self.effectList.currentItem().text() == 'Auto-Wah':
            self.effect.getLayout().changeEffect('Auto-Wah')
            self.model.switchToWah()

        elif self.effectList.currentItem().text() == 'Harmonizer':
            self.effect.getLayout().changeEffect('Harmonizer')
            self.effect.getLayout().currentWidget().reset()
            self.model.switchToChords()

        self.rev.getLayout().reset()
        self.delay.getLayout().reset()