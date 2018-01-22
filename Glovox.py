from pyo import *
from Effects import ReverbEFF , DelayEFF

## The Model

class Glovox():
	def __init__(self):
		self.server = Server(nchnls = 1)
		self.server.boot()

		#setting microphone as input
		self.signal = Input(chnl = 0)

		self.start()

		self.createPedals()

	def start(self):
		self.server.start()
		self.signal.out() #da spostare in modo che out venga chiamato sper ogni effetto. così posso cambiarli felicemente.

	def stop(self):
		self.server.stop()

	def createPedals(self):
		self.reverb = ReverbEFF(self.signal)
		self.delay = DelayEFF(self.signal)

	def getReverb(self):
		return self.reverb

	def enableReverb(self):
		self.reverb.enable()

	def disableReverb(self):
		self.reverb.disable()

	def getDelay(self):
		return self.delay

	def enableDelay(self):
		self.delay.enable()

	def disableDelay(self):
		self.delay.disable()




