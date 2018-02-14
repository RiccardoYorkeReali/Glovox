import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QStackedLayout, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox, QSlider, QLabel, QListWidget, QListWidgetItem)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

np.seterr(divide='ignore', invalid='ignore')

# MY WIDGETS

class mySlider(QWidget):
	#Slider used to change effects' paramaters
	def __init__(self, label, value):
		super().__init__()

		self.layout = QVBoxLayout()

		self.parameter = QLabel(label)
		self.parameter.setAlignment(Qt.AlignHCenter)
		self.value = QLabel(str(value))
		self.value.setAlignment(Qt.AlignHCenter)

		self.layout.addWidget(self.parameter)
		self.layout.addWidget(self.value)

		self.slider = QSlider(Qt.Vertical)
		if label == 'Depth':
			self.slider.setMinimum(1)
			self.slider.setMaximum(1000)
			self.slider.setValue(value*200)
			self.slider.setTickInterval(1)
			self.layout.addWidget(self.slider)
		elif label == 'Harmonics':
			self.slider.setMinimum(1)
			self.slider.setMaximum(1000)
			self.slider.setValue(value*10)
			self.slider.setTickInterval(1)
			self.layout.addWidget(self.slider)
		elif label == 'Revtime':
			self.slider.setMinimum(1000)
			self.slider.setMaximum(5000)
			self.slider.setValue(value * 1000)
			self.slider.setTickInterval(1)
			self.layout.addWidget(self.slider)
		elif label == 'Cutoff':
			self.slider.setMinimum(1)
			self.slider.setMaximum(10000)
			self.slider.setValue(value)
			self.slider.setTickInterval(1)
			self.layout.addWidget(self.slider)
		elif label == 'Room':
			self.slider.setMinimum(250)
			self.slider.setMaximum(4000)
			self.slider.setValue(value*1000)
			self.slider.setTickInterval(1)
			self.layout.addWidget(self.slider)
		else:
			self.slider.setMinimum(1)
			self.slider.setMaximum(1000)
			self.slider.setValue(value*1000)
			self.slider.setTickInterval(1)
			self.layout.addWidget(self.slider)

		self.layout.setAlignment(self.slider, Qt.AlignHCenter)
		self.setLayout(self.layout)

	def getSlider(self):
		return self.slider

	def updateValue(self, newValue):
		self.value.setText(str(newValue))

class EffectWidget(QGroupBox):
	#Effect Box. In this Widget will be displayed the active effect and it's paramaters slider (or list of options)
	def __init__(self, title, effect): #Effect must be a Layout
		super().__init__()

		self.setTitle(title)

		self.effectLayout = effect

		self.setMaximumHeight(250)

		self.setLayout(self.effectLayout)

	def getLayout(self):
		return self.effectLayout

class MainEffectLayout(QStackedLayout):
	#Stacked layout to display one effect at a time in the EffectWidget group box
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.noEffWidget = NoEffectWidget(self.model)
		self.distWidget = DistortionWidget(self.model)
		self.wahWidget = WahWidget(self.model)
		self.chordsWidget = ChordsWidget(self.model)
		self.sineWidget = SineWidget(self.model)
		self.blitWidget = BlitWidget(self.model)
		self.superSawWidget = SuperSawWidget(self.model)
		self.phasorWidget = PhasorWidget(self.model)
		self.rcWidget = RCOscWidget(self.model)
		self.lfoWidget = LFOWidget(self.model)

		self.addWidget(self.noEffWidget)
		self.addWidget(self.distWidget)
		self.addWidget(self.wahWidget)
		self.addWidget(self.chordsWidget)
		self.addWidget(self.sineWidget)
		self.addWidget(self.blitWidget)
		self.addWidget(self.superSawWidget)
		self.addWidget(self.phasorWidget)
		self.addWidget(self.rcWidget)
		self.addWidget(self.lfoWidget)

		self.typeFont = QFont(".Lucida Grande UI", 18)
		self.chordsWidget.chordsList.setFont(self.typeFont)
		self.lfoWidget.lfoWf.setFont(self.typeFont)

	def changeEffect(self, effect):
		if effect == 'No Effect':
			self.setCurrentWidget(self.noEffWidget)
		elif effect == 'Distortion':
			self.setCurrentWidget(self.distWidget)
		elif effect == 'Auto-Wah':
			self.setCurrentWidget(self.wahWidget)
		elif effect == 'Harmonizer':
			self.setCurrentWidget(self.chordsWidget)
		elif effect == 'Sine Oscillator':
			self.setCurrentWidget(self.sineWidget)
		elif effect == 'BLIT':
			self.setCurrentWidget(self.blitWidget)
		elif effect == 'Super Saw':
			self.setCurrentWidget(self.superSawWidget)
		elif effect == 'Phasor':
			self.setCurrentWidget(self.phasorWidget)
		elif effect == 'RC Oscillator':
			self.setCurrentWidget(self.rcWidget)
		elif effect == 'LF Oscillator':
			self.setCurrentWidget(self.lfoWidget)

	def getEffect(self):
		return self.currentWidget()

#The following classes implement the widgets related to each effect. Each class contains method to update model values and the view
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
		self.distDrive.updateValue(round(self.model.getDistortion().getDrive(),2))

	def setLPFSlope(self):
		self.model.getDistortion().setSlope(self.LPFSlope.getSlider().value()/1000)
		self.LPFSlope.updateValue(round(self.model.getDistortion().getSlope(),2))

	def reset(self):
		self.distDrive.getSlider().setValue(750)
		self.LPFSlope.getSlider().setValue(500)

		self.distDrive.updateValue(round(self.model.getDistortion().getDrive(),2))
		self.LPFSlope.updateValue(round(self.model.getDistortion().getSlope(),2))

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
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Major 7th':
			self.model.getChords().setMajor7th()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Major 7th-Maj':
			self.model.getChords().setMajor7thMaj()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Minor':
			self.model.getChords().setMinor()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Minor 7th':
			self.model.getChords().setMinor7th()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Minor 7th-Maj':
			self.model.getChords().setMinor7thMaj()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Diminished':
			self.model.getChords().setDiminished()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())
			
	def reset(self):
		self.chordsList.setCurrentItem(self.chordsList.item(0))

class SineWidget(QWidget):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.layout = QVBoxLayout()
		self.invisibleLabel = QLabel('')
		self.layout.addWidget(self.invisibleLabel)

		self.paramLayout = QHBoxLayout()

		self.sinePhase = mySlider('Phase', 0.0)
		self.paramLayout.addWidget(self.sinePhase)

		self.paramWidget = QWidget()
		self.paramWidget.setLayout(self.paramLayout)
		
		self.layout.addWidget(self.paramWidget)

		self.sinePhase.getSlider().valueChanged.connect(self.setPhase)

		self.setLayout(self.layout)

	def setPhase(self):
		self.model.getSine().setPhase(self.sinePhase.getSlider().value()/1000)
		self.sinePhase.updateValue(round(self.model.getSine().getPhase(),2))

	def reset(self):
		self.sinePhase.getSlider().setValue(0)
		self.sinePhase.updateValue(round(self.model.getSine().getPhase(), 2))

class BlitWidget(QWidget):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.layout = QVBoxLayout()
		self.invisibleLabel = QLabel('')
		self.layout.addWidget(self.invisibleLabel)

		self.paramLayout = QHBoxLayout()

		self.blitHarm = mySlider('Harmonics', 0.0)
		self.paramLayout.addWidget(self.blitHarm)

		self.paramWidget = QWidget()
		self.paramWidget.setLayout(self.paramLayout)
		
		self.layout.addWidget(self.paramWidget)

		self.blitHarm.getSlider().valueChanged.connect(self.setHarms)

		self.setLayout(self.layout)

	def setHarms(self):
		self.model.getBlit().setHarms(self.blitHarm.getSlider().value()/10)
		self.blitHarm.updateValue(round(self.model.getBlit().getHarms(),2))

	def reset(self):
		self.blitHarm.getSlider().setValue(400)
		self.blitHarm.updateValue(round(self.model.getBlit().getHarms(), 2))

class SuperSawWidget(QWidget):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.layout = QVBoxLayout()
		self.invisibleLabel = QLabel('')
		self.layout.addWidget(self.invisibleLabel)

		self.paramLayout = QHBoxLayout()

		self.ssDetune = mySlider('Detune', 0.5)
		self.ssBal = mySlider('Balance', 0.7)
		self.paramLayout.addWidget(self.ssDetune)
		self.paramLayout.addWidget(self.ssBal)

		self.paramWidget = QWidget()
		self.paramWidget.setLayout(self.paramLayout)
		
		self.layout.addWidget(self.paramWidget)

		self.ssDetune.getSlider().valueChanged.connect(self.setDetune)
		self.ssBal.getSlider().valueChanged.connect(self.setBal)

		self.setLayout(self.layout)

	def setDetune(self):
		self.model.getSuperSaw().setDetune(self.ssDetune.getSlider().value()/1000)
		self.ssDetune.updateValue(round(self.model.getSuperSaw().getDetune(),2))

	def setBal(self):
		self.model.getSuperSaw().setBal(self.ssBal.getSlider().value()/1000)
		self.ssBal.updateValue(round(self.model.getSuperSaw().getBal(),2))

	def reset(self):
		self.ssDetune.getSlider().setValue(500)
		self.ssBal.getSlider().setValue(700)
		self.ssDetune.updateValue(round(self.model.getSuperSaw().getDetune(), 2))
		self.ssBal.updateValue(round(self.model.getSuperSaw().getBal(), 2))

class PhasorWidget(QWidget):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.layout = QVBoxLayout()
		self.invisibleLabel = QLabel('')
		self.layout.addWidget(self.invisibleLabel)

		self.paramLayout = QHBoxLayout()

		self.phase = mySlider('Phase', 0.0)
		self.paramLayout.addWidget(self.phase)

		self.paramWidget = QWidget()
		self.paramWidget.setLayout(self.paramLayout)
		
		self.layout.addWidget(self.paramWidget)

		self.phase.getSlider().valueChanged.connect(self.setPhase)

		self.setLayout(self.layout)

	def setPhase(self):
		self.model.getPhasor().setPhase(self.phase.getSlider().value()/1000)
		self.phase.updateValue(round(self.model.getPhasor().getPhase(),2))

	def reset(self):
		self.phase.getSlider().setValue(0)
		self.phase.updateValue(round(self.model.getPhasor().getPhase(), 2))

class RCOscWidget(QWidget):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.layout = QVBoxLayout()
		self.invisibleLabel = QLabel('')
		self.layout.addWidget(self.invisibleLabel)

		self.paramLayout = QHBoxLayout()

		self.rcSharp = mySlider('Sharpness', 0.25)
		self.paramLayout.addWidget(self.rcSharp)

		self.paramWidget = QWidget()
		self.paramWidget.setLayout(self.paramLayout)
		
		self.layout.addWidget(self.paramWidget)

		self.rcSharp.getSlider().valueChanged.connect(self.setSharp)

		self.setLayout(self.layout)

	def setSharp(self):
		self.model.getRC().setSharp(self.rcSharp.getSlider().value()/1000)
		self.rcSharp.updateValue(round(self.model.getRC().getSharp(),2))

	def reset(self):
		self.rcSharp.getSlider().setValue(250)
		self.rcSharp.updateValue(round(self.model.getRC().getSharp(), 2))

class LFOWidget(QWidget):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.layout = QVBoxLayout()

		self.lfoWf = QListWidget()
		self.lfoWf.addItem(QListWidgetItem('Saw Up'))
		self.lfoWf.addItem(QListWidgetItem('Saw Down'))
		self.lfoWf.addItem(QListWidgetItem('Square'))
		self.lfoWf.addItem(QListWidgetItem('Triangle'))
		self.lfoWf.addItem(QListWidgetItem('Pulse'))
		self.lfoWf.addItem(QListWidgetItem('Bipolar Pulse'))
		self.lfoWf.addItem(QListWidgetItem('Sample & Hold'))
		self.lfoWf.addItem(QListWidgetItem('Modulated Sine'))
		self.lfoWf.setCurrentItem(self.lfoWf.item(0))
		self.layout.addWidget(self.lfoWf)

		self.setLayout(self.layout)

		self.lfoWf.itemSelectionChanged.connect(self.changeWaveform)

	def changeWaveform(self):
		if self.lfoWf.currentItem().text() == 'Saw Up':
			self.model.getLFO().setSawUp()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Saw Down':
			self.model.getLFO().setSawDown()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Square':
			self.model.getLFO().setSquare()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Triangle':
			self.model.getLFO().setTriangle()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Pulse':
			self.model.getLFO().setPulse()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Bipolar Pulse':
			self.model.getLFO().setBipolarPulse()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Sample & Hold':
			self.model.getLFO().setSnH()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Modulated Sine':
			self.model.getLFO().setModSine()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())
			
	def reset(self):
		self.lfoWf.setCurrentItem(self.lfoWf.item(0))

class ReverbLayout(QVBoxLayout):
	def __init__(self, model):
		super().__init__()

		self.model = model

		self.enableReverb = QCheckBox('Enable')
		self.addWidget(self.enableReverb)

		self.paramLayout = QHBoxLayout()

		self.revTime = mySlider('Revtime', 1.00)
		self.paramLayout.addWidget(self.revTime)

		self.revCutoff = mySlider('Cutoff', 5000)
		self.paramLayout.addWidget(self.revCutoff)

		self.roomSize = mySlider('Room', 0.25)
		self.paramLayout.addWidget(self.roomSize)

		self.revBalance = mySlider('Balance', 0.5)
		self.paramLayout.addWidget(self.revBalance)

		self.paramWidget = QWidget()
		self.paramWidget.setLayout(self.paramLayout)
		
		self.addWidget(self.paramWidget)

		self.enableReverb.stateChanged.connect(self.toggleReverbMode)
		self.revTime.getSlider().valueChanged.connect(self.setRevtime)
		self.revCutoff.getSlider().valueChanged.connect(self.setCutoff)
		self.roomSize.getSlider().valueChanged.connect(self.setRoomSize)
		self.revBalance.getSlider().valueChanged.connect(self.setRevBalance)

	def toggleReverbMode(self, activate):
		if activate == Qt.Checked:
			self.enableReverb.setText('Disable')
			self.model.enableReverb()
		else:
			self.enableReverb.setText('Enable')
			self.model.disableReverb()

	def reset(self):
		self.revTime.getSlider().setValue(1000)
		self.revCutoff.getSlider().setValue(5000)
		self.roomSize.getSlider().setValue(250)
		self.revBalance.getSlider().setValue(500)
		self.enableReverb.setText('Enable')
		self.enableReverb.setCheckState(Qt.Unchecked)

	def setRevtime(self):
		self.model.getReverb().setRevTime(self.revTime.getSlider().value()/1000)
		self.revTime.updateValue(round(self.model.getReverb().getRevTime(),2))

	def setCutoff(self):
		self.model.getReverb().setCutoff(self.revCutoff.getSlider().value())
		self.revCutoff.updateValue(round(self.model.getReverb().getCutoff(),2))

	def setRoomSize(self):
		self.model.getReverb().setRoomSize(4.25 - self.roomSize.getSlider().value()/1000)
		print(self.model.getReverb().getRoomSize())
		self.roomSize.updateValue(round(4.25 - self.model.getReverb().getRoomSize(),2))

	def setRevBalance(self):
		self.model.getReverb().setBal(self.revBalance.getSlider().value()/1000)
		self.revBalance.updateValue(round(self.model.getReverb().getBal(),2))


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
		self.enableDelay.setText('Enable')
		self.enableDelay.setCheckState(Qt.Unchecked)

	def setAmountDelay(self):
		self.model.getDelay().setDelayAmount(self.delayAmount.getSlider().value()/1000)
		self.delayAmount.updateValue(round(self.model.getDelay().getDelayAmount(),2))

	def setFeedback(self):
		self.model.getDelay().setFeedback(self.delayFeedback.getSlider().value()/1000)
		self.delayFeedback.updateValue(round(self.model.getDelay().getFeedback(),2))

# TO COMMENT
class MplFigure(object):
	def __init__(self, parent):
		self.figure = plt.figure(figsize=(6, 9), dpi=100, facecolor='#31363B')
		self.canvas = FigureCanvas(self.figure)
		
class WaveformWidget(QWidget):
	def __init__(self, model):
		super().__init__()

		#customize the UI
		self.initUI()

		self.initData(model)

		self.initWaveform()

	def initUI(self):
		vbox = QVBoxLayout()

		# mpl figure
		self.mainFigure = MplFigure(self)
		vbox.addWidget(self.mainFigure.canvas)

		self.setLayout(vbox)

		"""The refreshing part of the app is handled with a QTimer that gets called 10 times a second and 
		refreshes the gui at that time by calling the handleNewData function. 
		That function gets the latest frame from the microphone, plots the time series, 
		computes the Fourier transform and plots its modulus."""
		timer = QTimer()
		timer.timeout.connect(self.handleNewData)
		timer.start(100)
        
		self.timer = timer

	def initData(self, model):
		self.model = model

		# computes the parameters that will be used during plotting
		self.freqVect = np.fft.rfftfreq(self.model.server.getBufferSize(), 1./ (self.model.server.getSamplingRate()/10))  #input.getBufferSize() input.getSamplingRate()
		self.timeVect = np.arange(self.model.server.getBufferSize(), dtype=np.float32) / self.model.server.getSamplingRate() * 100

	def initWaveform(self):
		"""creates initial matplotlib plots in the main window and keeps 
		references for further use"""

		self.axTop = self.mainFigure.figure.add_subplot(111)
		self.axTop.set_ylim(-2000, 2000)
		self.axTop.set_xlim(0, self.timeVect.max())
		self.axTop.set_xlabel(u'time (ms)', fontsize=8, color='white')
		self.axTop.set_facecolor('#18465d')
		self.axTop.tick_params(axis='x', colors='white')
		self.axTop.tick_params(axis='y', colors='white')

		# line objects        
		self.lineTop, = self.axTop.plot(self.timeVect, np.ones_like(self.timeVect), color='white')

	def handleNewData(self):
		""" handles the asynchroneously collected sound chunks """

		# gets the latest frames        
		streams = self.model.getFrames()
		
		if len(streams) > 0:
			
			# plots the time signal
			self.lineTop.set_data(self.timeVect, streams*1000)

			# refreshes the plots
			self.mainFigure.canvas.draw()
