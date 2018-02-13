from pyo import *
from Effects import NoEFF, DistortionEFF, AutoWahEFF, ChordsEFF, SineEFF, BlitEFF, SuperSawEFF, PhasorEFF, RCOscEFF, LFOEff, ReverbEFF , DelayEFF
#from waveform import Waveform
import numpy as np

# The Model


class Glovox():
	def __init__(self):
		self.server = Server(nchnls = 1, buffersize=1024)
		self.server.boot()

		#setting microphone as input
		#it is necessary usign two input because of the references of python. If we used just one input, some effects won't be listened to,
		#because the use of stop() for stopping the normal signal output
		# Find a logic with less number of inputs
		self.input = Input(chnl = 0)

		self.input2 = Input(chnl = 0)

		self.input3 = Input(chnl = 0)

		self.input4 = Input(chnl = 0)
		self.gated = Gate(self.input4, thresh = -40, outputAmp = True)
		self.freq = Yin(self.input4, cutoff = 3000)

		self.output = Input(chnl = 0)

		self.createPedals()


		##TO Create waveform

		# Create a table of length `buffer size` and read it in loop.
		self.t = DataTable(size=self.server.getBufferSize())
		#self.osc = TableRead(self.t, freq=self.t.getRate(), loop=True, mul=0.1).out()
		# Share the table's memory with a numpy array.
		self.frames = []
		self.arr = np.asarray(self.t.getBuffer(), dtype=np.float64)
		self.server.setCallback(self.process)

		self.start()

	def getServer(self):
		return self.server

	def start(self):
		self.server.start()
		self.switchToNoEff()

	def stop(self):
		self.server.stop()

	def createPedals(self):
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
		self.reverb = ReverbEFF(self.output)
		self.delay = DelayEFF(self.output)

	def getInput(self):
		if self.noEffect.isOutputting():
			return self.noEffect
		elif self.distortion.isOutputting():
			return self.distortion
		elif self.wah.isOutputting():
			return self.wah
		elif self.chords.isOutputting():
			return self.chords
		elif self.sine.isOutputting():
			return self.sine
		elif self.blit.isOutputting():
			return self.blit
		elif self.superSaw.isOutputting():
			return self.superSaw
		elif self.phasor.isOutputting():
			return self.phasor
		elif self.rc.isOutputting():
			return self.rc
		elif self.lfo.isOutputting():
			return self.lfo

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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.noEffect.enable()

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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.distortion.reset()
		self.distortion.enable()

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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.wah.enable()

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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.chords.reset()
		self.chords.enable()

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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.sine.enable()

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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.blit.enable()

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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.superSaw.enable()

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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.phasor.enable()

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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.rc.enable()

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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.lfo.enable()

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
		elif self.lfo.isOutputting():
			self.reverb.enable(self.lfo.getSignal())

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
		elif self.lfo.isOutputting():
			self.delay.enable(self.lfo.getSignal())


	def disableDelay(self):
		self.delay.disable()

	def process(self):
		"Fill the array (so the table) with value of current input."
		self.samples = self.t.getTable()
		self.arr[1:] = self.arr[:-1]
		self.arr[0] = self.samples[-1]

	def getFrames(self):
		"""frames = self.frames
		self.frames = []"""
		return self.arr

	def getWaveform(self):
		return self.waveform