from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QListWidgetItem, QFrame, QSlider, QListWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QGroupBox)
from MyWidgets import  EffectWidget, MainEffectLayout, ReverbLayout, DelayLayout, WaveformWidget
import json

### THE GUI

class MainWindow(QWidget):
    def __init__(self, model):
        super().__init__()

        self.model = model
        self.effects_file = json.load(open('effects.json'))

        self.init_ui()

    def init_ui(self):

        #Title
        self.setWindowTitle("Glovox")

        #GUI Elements
        self.effectList = QListWidget()

        noEff = QListWidgetItem('No Effect')
        noEff.setToolTip(self.effects_file["effects"][0]["NoEffects"])

        dist = QListWidgetItem('Distortion')
        dist.setToolTip(self.effects_file["effects"][1]["Distortion"])

        wah = QListWidgetItem('Auto-Wah')
        wah.setToolTip(self.effects_file["effects"][2]["Auto-Wah"])

        chords = QListWidgetItem('Harmonizer')
        chords.setToolTip(self.effects_file["effects"][3]["Chords"])

        sine = QListWidgetItem('Sine Oscillator')
        sine.setToolTip(self.effects_file["effects"][4]["Sine Oscillator"])

        blit = QListWidgetItem('BLIT')
        blit.setToolTip(self.effects_file["effects"][5]["BLIT"])

        superSaw = QListWidgetItem('Super Saw')
        superSaw.setToolTip(self.effects_file["effects"][6]["Super Saw"])

        phasor = QListWidgetItem('Phasor')
        phasor.setToolTip(self.effects_file["effects"][7]["Phasor"])

        rc = QListWidgetItem('RC Oscillator')
        rc.setToolTip(self.effects_file["effects"][8]["RC Oscillator"])

        lfo = QListWidgetItem('LF Oscillator')
        lfo.setToolTip(self.effects_file["effects"][9]["LF Oscillator"])

        self.effectList.addItem(noEff)
        self.effectList.addItem(dist)
        self.effectList.addItem(wah)
        self.effectList.addItem(chords)
        self.effectList.addItem(sine)
        self.effectList.addItem(blit)
        self.effectList.addItem(superSaw)
        self.effectList.addItem(phasor)
        self.effectList.addItem(rc)
        self.effectList.addItem(lfo)
        self.effectList.setCurrentItem(self.effectList.item(0))

        #Effects List
        effectListLayout = QVBoxLayout()
        effectListLayout.addWidget(self.effectList)

        effectListBox = QGroupBox('Effects')
        effectListBox.setMaximumWidth(300)
        effectListBox.setMinimumWidth(150)
        effectListBox.setLayout(effectListLayout)

        #Effects manager: analyzer and parameters

        self.waveform = WaveformWidget(self.model)
        
        analyzerLayout = QVBoxLayout()
        analyzerLayout.addWidget(self.waveform)
        
        analyzerBox = QGroupBox('Analyzer')
        analyzerBox.setMinimumHeight(370)
        analyzerBox.setMaximumHeight(400)
        analyzerBox.setLayout(analyzerLayout)

        effectParameterLayout = QHBoxLayout()

        self.effect = EffectWidget('Effect', MainEffectLayout(self.model))
        self.rev = EffectWidget('Reverb', ReverbLayout(self.model))
        self.delay = EffectWidget('Delay', DelayLayout(self.model))

        self.effect.setMinimumWidth(200)
        self.rev.setMinimumWidth(275)
        self.delay.setMinimumWidth(200)

        self.effect.setMaximumWidth(300)
        self.rev.setMaximumWidth(375)
        self.delay.setMaximumWidth(300)

        self.effect.setMinimumHeight(275)
        self.rev.setMinimumHeight(275)
        self.delay.setMinimumHeight(275)


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
        self.setMinimumSize(1350, 750)

        self.show()

        self.effectList.itemSelectionChanged.connect(self.changeEffect)

    def closeEvent(self, event):
        self.model.switchToNoEff() #così si dovrebbe chiudere senza problemi
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

        elif self.effectList.currentItem().text() == 'Sine Oscillator':
            self.effect.getLayout().changeEffect('Sine Oscillator')
            self.effect.getLayout().currentWidget().reset()
            self.model.switchToSine()
        elif self.effectList.currentItem().text() == 'BLIT':
            self.effect.getLayout().changeEffect('BLIT')
            self.effect.getLayout().currentWidget().reset()
            self.model.switchToBlit()
        elif self.effectList.currentItem().text() == 'Super Saw':
            self.effect.getLayout().changeEffect('Super Saw')
            self.effect.getLayout().currentWidget().reset()
            self.model.switchToSuperSaw()
        elif self.effectList.currentItem().text() == 'Phasor':
            self.effect.getLayout().changeEffect('Phasor')
            self.effect.getLayout().currentWidget().reset()
            self.model.switchToPhasor()
        elif self.effectList.currentItem().text() == 'RC Oscillator':
            self.effect.getLayout().changeEffect('RC Oscillator')
            self.effect.getLayout().currentWidget().reset()
            self.model.switchToRC()
        elif self.effectList.currentItem().text() == 'LF Oscillator':
            self.effect.getLayout().changeEffect('LF Oscillator')
            self.effect.getLayout().currentWidget().reset()
            self.model.switchToLFO()

        self.rev.getLayout().reset()
        self.delay.getLayout().reset()