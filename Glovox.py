from pyo import *
from Effects import NoEFF, DistortionEFF, AutoWahEFF, ChordsEFF, ReverbEFF , DelayEFF

## The Model

class Glovox():
	def __init__(self):
		self.server = Server(buffersize = 512, nchnls = 1)
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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
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

		#NB in verità, quando cambio effetto, la variabile di input per rev e delay va in stop, e quindi, rev e delay, se erano attivati non si sentono,
		# ma non sono in stop. Tuttavia è pur vero che quando cambio effetto e poi riapplico al nuovo effetto o rev o delay, a questo viene cambiato
		#l'input e quindi, il costo non dovrebbe essere grande. In ogni caso, meglio eliminare il problema alla radice, che rischiare di fargli fare 
		#conti inutili
		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.distortion.reset()
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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
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

		#self.disableReverb()
		self.reverb.reset()
		#self.disableDelay()
		self.delay.reset()
		self.chords.reset()
		self.chords.enable()

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

	def disableDelay(self):
		self.delay.disable()