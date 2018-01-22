from pyo import *

#EFFECTS

class ReverbEFF():
	def __init__(self, cleanS):
		self.intensity = 0.5
		self.HFA = 0.5
		self.dryWet = 0.5

		self.reverb = Freeverb(cleanS, size = self.intensity, damp = self.HFA, bal = self.dryWet)

	def setIntensity(self, intensity):
		self.reverb.setSize(intensity)

	def setHFA(self, HFA):
		self.reverb.setDamp(HFA)

	def setDryWet(self, dryWet):
		self.reverb.setBal(dryWet)	

	def enable(self):
		self.reverb.out()

	def disable(self):
		self.reverb.stop()

class DelayEFF():
	def __init__(self, cleanS):
		self.delayAmount = 0.25
		self.feedback = 0.0

		self.delay = Delay(cleanS, delay = self.delayAmount, feedback = self.feedback)

	def setDelay(self, delayAmount):
		self.delay.setDelay(delayAmount)

	def setFeedback(self, feedback):
		self.delay.setFeedback(feedback)

	def enable(self):
		self.delay.out()

	def disable(self):
		self.delay.stop()
	