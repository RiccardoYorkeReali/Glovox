from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QFrame, QWidget, QStackedLayout, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox, QSlider, QLabel, QListWidget, QListWidgetItem)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import matplotlib.pyplot as plt

class mySlider(QWidget):
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
		print('siamo in update')
		self.value.setText(str(newValue))

class EffectWidget(QGroupBox):
	def __init__(self, title, effect): #Effect must be a Layout
		super().__init__()

		self.setTitle(title)

		self.effectLayout = effect

		self.setMaximumHeight(250)

		self.setLayout(self.effectLayout)

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
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Major 7th':
			self.model.getChords().setMajor7th()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Major 7th-Maj':
			self.model.getChords().setMajor7thMaj()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Minor':
			self.model.getChords().setMinor()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Minor 7th':
			self.model.getChords().setMinor7th()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Minor 7th-Maj':
			self.model.getChords().setMinor7thMaj()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Diminished':
			self.model.getChords().setDiminished()
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

		self.reverbSize = mySlider('Intensity', 0.5)
		self.paramLayout.addWidget(self.reverbSize)

		self.reverbHFA = mySlider('HFA', 0.5)
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
		self.enableReverb.setText('Enable')
		self.enableReverb.setCheckState(Qt.Unchecked)

	def setSize(self):
		self.model.getReverb().setIntensity(self.reverbSize.getSlider().value()/1000)
		self.reverbSize.updateValue(round(self.model.getReverb().getIntensity(),2))

	def setHFA(self):
		self.model.getReverb().setHFA(self.reverbHFA.getSlider().value()/1000)
		self.reverbHFA.updateValue(round(self.model.getReverb().getHFA(),2))

	def setBal(self):
		self.model.getReverb().setDryWet(self.reverbBal.getSlider().value()/1000)
		self.reverbBal.updateValue(round(self.model.getReverb().getDryWet(),2))

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

class MplFigure(object):
	def __init__(self, parent):
		self.figure = plt.figure(facecolor='#31363B')
		self.canvas = FigureCanvas(self.figure)

class WaveformWidget(QWidget):
	def __init__(self, model):
		super().__init__()

		#customize the UI
		self.initUI()

		self.initData(model)

		#self.waveform.view(title='Scope', wxnoserver=True)

		self.initWaveform()

	def initUI(self):
		vbox = QVBoxLayout()

		# mpl figure
		self.mainFigure = MplFigure(self)
		#vbox.addWidget(self.main_figure.toolbar)
		vbox.addWidget(self.mainFigure.canvas)

		self.setLayout(vbox)

		timer = QTimer()
		timer.timeout.connect(self.handleNewData)
		timer.start(100)

		# keep reference to timer        
		self.timer = timer

	def initData(self, model):

		# keeps reference to model
		self.model = model

		input = self.model.getInput()

		# computes the parameters that will be used during plotting
		chunksize = 1024
		rate = 4000
		self.freqVect = np.fft.rfftfreq(chunksize,1./rate)#input.getBufferSize() input.getSamplingRate()
		self.timeVect = np.arange(chunksize, dtype=np.float32) / rate * 1000

	def initWaveform(self):
		"""creates initial matplotlib plots in the main window and keeps 
		references for further use"""

		# top plot
		self.axTop = self.mainFigure.figure.add_subplot(211)
		self.axTop.set_ylim(-500, 500) #-32768, 32768
		self.axTop.set_xlim(0, self.timeVect.max())
#		self.axTop.set_xlabel(u'time (ms)', fontsize=6, color='white')
		
		self.axTop.set_facecolor('#76797c')
		self.axTop.tick_params(axis='x', colors='white')
		self.axTop.tick_params(axis='y', colors='white')

		# bottom plot
		self.axBottom = self.mainFigure.figure.add_subplot(212)
		self.axBottom.set_ylim(0, 1)
		self.axBottom.set_xlim(0, self.freqVect.max())
		self.axBottom.set_xlabel(u'frequency (Hz)', fontsize=6, color='white')
		self.axBottom.set_facecolor('#76797c')
		self.axBottom.tick_params(axis='x', colors='white')
		self.axBottom.tick_params(axis='y', colors='white')

		# line objects        
		self.lineTop, = self.axTop.plot(self.timeVect, np.ones_like(self.timeVect), color='white')
		self.lineBottom, = self.axBottom.plot(self.freqVect, np.ones_like(self.freqVect), color='white')

	def handleNewData(self):
		""" handles the asynchroneously collected sound chunks """

		# gets the latest frames        
		streams = self.model.getFrames()
		
		if len(streams) > 0:
			# keeps only the last frame
			currentStream = streams[-1]
			# plots the time signal
			self.lineTop.set_data(self.timeVect, streams*1000)
			# computes and plots the fft signal            
			fftFrame = np.fft.rfft(streams*1000)
			
			fftFrame /= np.abs(fftFrame).max()
			
			#print(np.abs(fft_frame).max())

			self.lineBottom.set_data(self.freqVect, np.abs(fftFrame))            
			
			# refreshes the plots
			self.mainFigure.canvas.draw()
