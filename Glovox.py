from pyo import *
from Effects import NoEFF, DistortionEFF, AutoWahEFF, ChordsEFF, ReverbEFF , DelayEFF

## The Model

class Glovox():
	def __init__(self):
		self.server = Server(nchnls = 1)
		self.server.boot()

		#setting microphone as input
		#it is necessary usign two input because of the references of python. If we used just one input, some effects won't be listened to,
		#because the use of stop() for stopping the normal signal output
		# Find a logic with less number of inputs
		self.input = Input(chnl = 0)

		self.input2 = Input(chnl = 0)

		self.input3 = Input(chnl = 0)

		self.input4 = Input(chnl = 0)

		self.output = Input(chnl = 0)

		self.createPedals()

		self.start()

	def start(self):
		self.server.start()
		self.switchToNoEff()

	def stop(self):
		self.server.stop()

	def createPedals(self):
		self.noEffect = NoEFF(self.input)
		self.distortion = DistortionEFF(self.input2)
		self.wah = AutoWahEFF(self.input3)
		self.chords = ChordsEFF(self.input4)
		self.reverb = ReverbEFF(self.output)
		self.delay = DelayEFF(self.output)

	def getNoEffect(self):
		return self.noEffect

	def switchToNoEff(self):
		if self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()

		self.reverb.reset()
		self.delay.reset()
		self.noEffect.enable(self.output)

	def getDistortion(self):
		return self.distortion

	def switchToDistortion(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()

		self.distortion.reset()
		self.reverb.reset()
		self.delay.reset()
		self.distortion.enable(self.output)

	def getChorus(self):
		return self.chorus

	def switchToWah(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.chords.isOutputting():
			self.chords.disable()

		self.reverb.reset()
		self.delay.reset()
		self.wah.enable(self.output)

	def getChords(self):
		return self.chords

	def switchToChords(self):
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()

		self.reverb.reset()
		self.delay.reset()
		self.chords.reset()
		self.chords.enable(self.output)


	def getReverb(self):
		return self.reverb

	def enableReverb(self):
		self.reverb.enable(self.output)

	def disableReverb(self):
		self.reverb.disable()

	def getDelay(self):
		return self.delay

	def enableDelay(self):
		self.delay.enable(self.output)

	def disableDelay(self):
		self.delay.disable()