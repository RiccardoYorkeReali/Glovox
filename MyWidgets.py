from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox, QSlider, QLabel)

class mySlider(QWidget):
	def __init__(self, label, value):
		super().__init__()

		self.layout = QVBoxLayout()

		self.parameter = QLabel(label)
		self.layout.addWidget(self.parameter)

		self.slider = QSlider(Qt.Vertical)
		self.slider.setMinimum(0)
		self.slider.setMaximum(1000)
		self.slider.setValue(value*1000)
		self.slider.setTickInterval(1) #prova a cambiare

		self.layout.addWidget(self.slider)

		self.setLayout(self.layout)

	def getSlider(self):
		return self.slider

class EffectWidget(QGroupBox):
	def __init__(self, title, effect): #Effect must be a Layout
		super().__init__()

		self.setTitle(title)
		self.setLayout(effect)
		self.setMaximumHeight(250)


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

	def setAmountDelay(self):
		self.model.getDelay().setDelay(self.delayAmount.getSlider().value()/1000)

	def setFeedback(self):
		self.model.getDelay().setFeedback(self.delayFeedback.getSlider().value()/1000)

