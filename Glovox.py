from pyo import *
from Effects import (NoEFF, DistortionEFF, AutoWahEFF, ChordsEFF, SineEFF, BlitEFF, SuperSawEFF, PhasorEFF, RCOscEFF, LFOEff, ReverbEFF, DelayEFF)
import numpy as np
import threading
import atexit

# The Model

class Glovox():
	def __init__(self):
		self.server = Server(nchnls=1)
		self.server.boot()

		# setting microphones as input
		# more inputs are used because calling stop() on just a single input disables all the pedals' output 
		self.input = Input(chnl=0)

		self.input2 = Input(chnl=0)

		self.input3 = Input(chnl=0)

		self.input4 = Input(chnl=0)

		self.gated = Gate(self.input4, thresh=-40, outputAmp=True)
		self.freq = Yin(self.input4, cutoff=3000)

		self.input5 = Input(chnl=0)

		self.createPedals()

		#TO COMMENT
		# Create a table of length `buffer size` and read it in loop.
		self.t = DataTable(size=self.server.getBufferSize())
		# Share the table's memory with a numpy array.
		self.arr = np.asarray(self.t.getBuffer())
		# callback necessary for waveform
		self.server.setCallback(self.process)

		self.lock = threading.Lock()
		self.stop = False
		"""This class runs in a thread. 
		So to make sure it stops correctly, a call to atexit is registered at startup"""
		atexit.register(self.close)


		self.start()

	def close(self):
		with self.lock:
			self.stop = True
		self.t.reset()
		self.server.stop()

	def getServer(self):
		return self.server

	def start(self):
		self.server.start()
		self.switchToNoEff()

	def createPedals(self):
		#creating all the effects
		self.noEffect = NoEFF(self.input)
		self.distortion = DistortionEFF(self.input2)
		self.wah = AutoWahEFF(self.input2)
		self.chords = ChordsEFF(self.input3)
		self.sine = SineEFF(self.gated, self.freq)
		self.blit = BlitEFF(self.gated, self.freq)
		self.superSaw = SuperSawEFF(self.gated, self.freq)
		self.phasor = PhasorEFF(self.gated, self.freq)
		self.rc = RCOscEFF(self.gated, self.freq)
		self.lfo = LFOEff(self.gated, self.freq)
		self.reverb = ReverbEFF(self.input5)
		self.delay = DelayEFF(self.input5)

	def getNoEffect(self):
		return self.noEffect

	def switchToNoEff(self):
		if self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.noEffect.enable()
		self.rec = TableFill(self.noEffect.getSignal(), self.t)

	def getDistortion(self):
		return self.distortion

	def switchToDistortion(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.distortion.reset()
		self.distortion.enable()
		self.rec = TableFill(self.distortion.getSignal(), self.t)

	def getWah(self):
		return self.wah

	def switchToWah(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.wah.enable()
		self.rec = TableFill(self.wah.getSignal(), self.t)

	def getChords(self):
		return self.chords

	def switchToChords(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.chords.reset()
		self.chords.enable()
		self.rec = TableFill(self.chords.getSignal(), self.t)

	def updateTableChords(self):
		self.rec = TableFill(self.chords.getSignal(), self.t)

	def getSine(self):
		return self.sine

	def switchToSine(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.sine.enable()
		self.rec = TableFill(self.sine.getSignal(), self.t)

	def getBlit(self):
		return self.blit

	def switchToBlit(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.blit.enable()
		self.rec = TableFill(self.blit.getSignal(), self.t)

	def getSuperSaw(self):
		return self.superSaw

	def switchToSuperSaw(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.superSaw.enable()
		self.rec = TableFill(self.superSaw.getSignal(), self.t)

	def getPhasor(self):
		return self.phasor

	def switchToPhasor(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.phasor.enable()
		self.rec = TableFill(self.phasor.getSignal(), self.t)

	def getRC(self):
		return self.rc

	def switchToRC(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.rc.enable()
		self.rec = TableFill(self.rc.getSignal(), self.t)

	def getLFO(self):
		return self.lfo

	def switchToLFO(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.lfo.enable()
		self.rec = TableFill(self.lfo.getSignal(), self.t)

	def getReverb(self):
		return self.reverb

	def enableReverb(self):
		if self.noEffect.isOutputting():
			self.reverb.enable(self.noEffect.getSignal())
		elif self.distortion.isOutputting():
			self.reverb.enable(self.distortion.getSignal())
		elif self.wah.isOutputting():
			self.reverb.enable(self.wah.getSignal())
		elif self.chords.isOutputting():
			self.reverb.enable(self.chords.getSignal())
		elif self.sine.isOutputting():
			self.reverb.enable(self.sine.getSignal())
		elif self.blit.isOutputting():
			self.reverb.enable(self.blit.getSignal())
		elif self.superSaw.isOutputting():
			self.reverb.enable(self.superSaw.getSignal())
		elif self.phasor.isOutputting():
			self.reverb.enable(self.phasor.getSignal())
		elif self.rc.isOutputting():
			self.reverb.enable(self.rc.getSignal())

	def disableReverb(self):
		self.reverb.disable()

	def getDelay(self):
		return self.delay

	def enableDelay(self):
		if self.noEffect.isOutputting():
			self.delay.enable(self.noEffect.getSignal())
		elif self.distortion.isOutputting():
			self.delay.enable(self.distortion.getSignal())
		elif self.wah.isOutputting():
			self.delay.enable(self.wah.getSignal())
		elif self.chords.isOutputting():
			self.delay.enable(self.chords.getSignal())
		elif self.sine.isOutputting():
			self.delay.enable(self.sine.getSignal())
		elif self.blit.isOutputting():
			self.delay.enable(self.blit.getSignal())
		elif self.superSaw.isOutputting():
			self.delay.enable(self.superSaw.getSignal())
		elif self.phasor.isOutputting():
			self.delay.enable(self.phasor.getSignal())
		elif self.rc.isOutputting():
			self.delay.enable(self.rc.getSignal())

	def disableDelay(self):
		self.delay.disable()

#TO COMMENT
	def process(self):
		"""Fill the array (so the table) with value of current input."""
		self.samples = self.t.getTable()
		with self.lock:
			self.arr[1:] = self.arr[:-1]
			self.arr[0] = self.samples[-1]
			if self.stop:
				return None
		return None

	def getFrames(self):
		with self.lock:
			return self.arr
