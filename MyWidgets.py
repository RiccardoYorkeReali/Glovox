from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QWidget, QStackedLayout, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox, QSlider, QLabel, QListWidget, QListWidgetItem)

class mySlider(QWidget):
	def __init__(self, label, value):
		super().__init__()

		self.layout = QVBoxLayout()

		self.parameter = QLabel(label)
		self.layout.addWidget(self.parameter)

		self.slider = QSlider(Qt.Vertical)
		if label == 'Depth':
			self.slider.setMinimum(1)
			self.slider.setMaximum(1000)
			self.slider.setValue(value*200)
			self.slider.setTickInterval(1)
			self.layout.addWidget(self.slider)
		else:
			self.slider.setMinimum(1)
			self.slider.setMaximum(1000)
			self.slider.setValue(value*1000)
			self.slider.setTickInterval(1)
			self.layout.addWidget(self.slider)

		self.setLayout(self.layout)

	def getSlider(self):
		return self.slider

class EffectWidget(QGroupBox):
	def __init__(self, title, effect): #Effect must be a Layout
		super().__init__()

		self.setTitle(title)

		self.effectLayout = effect

		self.setLayout(self.effectLayout)
		self.setMaximumHeight(250)
		self.setMinimumWidth(220)
		self.setMaximumWidth(400)

	def getLayout(self):
		return self.effectLayout

class MainEffectLayout(QStackedLayout):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.noEffWidget = NoEffectWidget(self.model)
		self.distWidget = DistortionWidget(self.model)
		self.wahWidget = WahWidget(self.model)
		self.chordsWidget = ChordsWidget(self.model)

		self.addWidget(self.noEffWidget)
		self.addWidget(self.distWidget)
		self.addWidget(self.wahWidget)
		self.addWidget(self.chordsWidget)

	def changeEffect(self, effect):
		if effect == 'No Effect':
			self.setCurrentWidget(self.noEffWidget)
		elif effect == 'Distortion':
			self.setCurrentWidget(self.distWidget)
		elif effect == 'Auto-Wah':
			self.setCurrentWidget(self.wahWidget)
		elif effect == 'Harmonizer':
			self.setCurrentWidget(self.chordsWidget)

	def getEffect(self):
		return self.currentWidget()

class NoEffectWidget(QWidget):
	def __init__(self, model):
		super().__init__()

class DistortionWidget(QWidget):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.layout = QVBoxLayout()
		self.invisibleLabel = QLabel('')
		self.layout.addWidget(self.invisibleLabel)

		self.paramLayout = QHBoxLayout()

		self.distDrive = mySlider('Drive', 0.75)
		self.paramLayout.addWidget(self.distDrive)

		self.LPFSlope = mySlider('LPF Slope', 0.5)
		self.paramLayout.addWidget(self.LPFSlope)

		self.paramWidget = QWidget()
		self.paramWidget.setLayout(self.paramLayout)
		
		self.layout.addWidget(self.paramWidget)

		self.distDrive.getSlider().valueChanged.connect(self.setDrive)
		self.LPFSlope.getSlider().valueChanged.connect(self.setLPFSlope)

		self.setLayout(self.layout)


	def setDrive(self):
		self.model.getDistortion().setDrive(self.distDrive.getSlider().value()/1000)

	def setLPFSlope(self):
		self.model.getDistortion().setSlope(self.LPFSlope.getSlider().value()/1000)

	def reset(self):
		self.distDrive.getSlider().setValue(750)
		self.LPFSlope.getSlider().setValue(500)


class WahWidget(QWidget):
	def __init__(self, model):
		super().__init__()

	def setDepth(self):
		self.model.getChorus().setDepth(self.chorusDepth.getSlider().value()/200)

	def setFeedback(self):
		self.model.getChorus().setFeedback(self.chorusFB.getSlider().value()/1000)

	def setBal(self):
		self.model.getChorus().setDryWet(self.chorusDryWet.getSlider().value()/1000)

class ChordsWidget(QWidget):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.layout = QVBoxLayout()

		self.chordsList = QListWidget()
		self.chordsList.addItem(QListWidgetItem('Major'))
		self.chordsList.addItem(QListWidgetItem('Major 7th'))
		self.chordsList.addItem(QListWidgetItem('Major 7th-Maj'))
		self.chordsList.addItem(QListWidgetItem('Minor'))
		self.chordsList.addItem(QListWidgetItem('Minor 7th'))
		self.chordsList.addItem(QListWidgetItem('Minor 7th-Maj'))
		self.chordsList.addItem(QListWidgetItem('Diminished'))
		self.chordsList.setCurrentItem(self.chordsList.item(0))
		self.layout.addWidget(self.chordsList)

		self.setLayout(self.layout)

		self.chordsList.itemSelectionChanged.connect(self.changeChords)

	def changeChords(self):
		if self.chordsList.currentItem().text() == 'Major':
			self.model.getChords().setMajor()

		elif self.chordsList.currentItem().text() == 'Major 7th':
			self.model.getChords().setMajor7th()

		elif self.chordsList.currentItem().text() == 'Major 7th-Maj':
			self.model.getChords().setMajor7thMaj()

		elif self.chordsList.currentItem().text() == 'Minor':
			self.model.getChords().setMinor()

		elif self.chordsList.currentItem().text() == 'Minor 7th':
			self.model.getChords().setMinor7th()

		elif self.chordsList.currentItem().text() == 'Minor 7th-Maj':
			self.model.getChords().setMinor7thMaj()

		elif self.chordsList.currentItem().text() == 'Diminished':
			self.model.getChords().setDiminished()

	def reset(self):
		self.chordsList.setCurrentItem(self.chordsList.item(0))

class ReverbLayout(QVBoxLayout):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.enableReverb = QCheckBox('Enable')
		self.addWidget(self.enableReverb)

		self.paramLayout = QHBoxLayout()

		self.reverbSize = mySlider('Intensity', 0.5)
		self.paramLayout.addWidget(self.reverbSize)

		self.reverbHFA = mySlider('High Freq. Attenuation', 0.5)
		self.paramLayout.addWidget(self.reverbHFA)

		self.reverbBal = mySlider('Dry/Wet', 0.5)
		self.paramLayout.addWidget(self.reverbBal)

		self.paramWidget = QWidget()
		self.paramWidget.setLayout(self.paramLayout)
		
		self.addWidget(self.paramWidget)

		self.enableReverb.stateChanged.connect(self.toggleReverbMode)
		self.reverbSize.getSlider().valueChanged.connect(self.setSize)
		self.reverbHFA.getSlider().valueChanged.connect(self.setHFA)
		self.reverbBal.getSlider().valueChanged.connect(self.setBal)

	def toggleReverbMode(self, activate):
		if activate == Qt.Checked:
			self.enableReverb.setText('Disable')
			self.model.enableReverb()
		else:
			self.enableReverb.setText('Enable')
			self.model.disableReverb()

	def reset(self):
		self.reverbSize.getSlider().setValue(500)
		self.reverbHFA.getSlider().setValue(500)
		self.reverbBal.getSlider().setValue(500)

	def setSize(self):
		self.model.getReverb().setIntensity(self.reverbSize.getSlider().value()/1000)

	def setHFA(self):
		self.model.getReverb().setHFA(self.reverbHFA.getSlider().value()/1000)

	def setBal(self):
		self.model.getReverb().setDryWet(self.reverbBal.getSlider().value()/1000)

class DelayLayout(QVBoxLayout):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.enableDelay = QCheckBox('Enable')
		self.addWidget(self.enableDelay)

		self.paramLayout = QHBoxLayout()

		self.delayAmount = mySlider('Delay', 0.25)
		self.paramLayout.addWidget(self.delayAmount)

		self.delayFeedback = mySlider('Feedback', 0.0)
		self.paramLayout.addWidget(self.delayFeedback)

		self.paramWidget = QWidget()
		self.paramWidget.setLayout(self.paramLayout)
		
		self.addWidget(self.paramWidget)

		self.enableDelay.stateChanged.connect(self.toggleDelayMode)
		self.delayAmount.getSlider().valueChanged.connect(self.setAmountDelay)
		self.delayFeedback.getSlider().valueChanged.connect(self.setFeedback)

	def toggleDelayMode(self, activate):
		if activate == Qt.Checked:
			self.enableDelay.setText('Disable')
			self.model.enableDelay()
		else:
			self.enableDelay.setText('Enable')
			self.model.disableDelay()

	def reset(self):
		self.delayAmount.getSlider().setValue(250)
		self.delayFeedback.getSlider().setValue(0)

	def setAmountDelay(self):
		self.model.getDelay().setDelay(self.delayAmount.getSlider().value()/1000)

	def setFeedback(self):
		self.model.getDelay().setFeedback(self.delayFeedback.getSlider().value()/1000)