from pyo import *

#EFFECTS

class NoEFF():
	def __init__(self, cleanS):
		self.signal = cleanS

	def enable(self, output):
		self.signal.out()

	def disable(self):
		self.signal.stop()

	def isOutputting(self):
		return self.signal.isOutputting()

	def getSignal(self):
		return self.signal

class DistortionEFF():
	def __init__(self, cleanS):
		self.drive = 0.75
		self.slope = 0.5

		self.dist = Disto(cleanS, drive = self.drive, slope = self.slope)

	def setDrive(self, drive):
		self.dist.setDrive(drive)

	def setSlope(self, slope):
		self.dist.setSlope(slope)

	def reset(self):
		self.setDrive(0.75)
		self.setSlope(0.5)

	def enable(self, output):
		self.dist.out()

	def disable(self):
		self.dist.stop()

	def isOutputting(self):
		return self.dist.isOutputting()

	def getSignal(self):
		return self.dist

class AutoWahEFF():
	def __init__(self, cleanS):
		self.fol = Follower(cleanS, freq=30, mul=4000, add=40)
		self.wah = Biquad(cleanS, freq=self.fol, q=5, type=2)

	def enable(self, output):
		self.wah.out()

	def disable(self):
		self.wah.stop()

	def isOutputting(self):
		return self.wah.isOutputting()

	def getSignal(self):
		return self.wah

class ChordsEFF():
	def __init__(self, cleanS):
		self.first = cleanS

		self.third = Harmonizer(self.first, transpo = 4)
		self.fifth = Harmonizer(self.third, transpo = 3)
		self.lastNote = Harmonizer(self.fifth, transpo = 5) #Default major chords

		self.chords = self.first + self.third + self.fifth + self.lastNote

	def setMajor(self):
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 4)
		self.fifth = Harmonizer(self.third, transpo = 3)
		self.lastNote = Harmonizer(self.fifth, transpo = 5)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()


	def setMajor7th(self):
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 4)
		self.fifth = Harmonizer(self.third, transpo = 3)
		self.lastNote = Harmonizer(self.fifth, transpo = 3)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def setMajor7thMaj(self):
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 4)
		self.fifth = Harmonizer(self.third, transpo = 3)
		self.lastNote = Harmonizer(self.fifth, transpo = 4)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def setMinor(self):
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 3)
		self.fifth = Harmonizer(self.third, transpo = 4)
		self.lastNote = Harmonizer(self.fifth, transpo = 5)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()


	def setMinor7th(self):
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 3)
		self.fifth = Harmonizer(self.third, transpo = 4)
		self.lastNote = Harmonizer(self.fifth, transpo = 3)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def setMinor7thMaj(self):
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 3)
		self.fifth = Harmonizer(self.third, transpo = 4)
		self.lastNote = Harmonizer(self.fifth, transpo = 4)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def setDiminished(self):
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 3)
		self.fifth = Harmonizer(self.third, transpo = 3)
		self.lastNote = Harmonizer(self.fifth, transpo = 3)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def reset(self):
		self.setMajor()

	def enable(self):
		self.chords.out()
		
	def disable(self):
		self.chords.stop()

	def isOutputting(self):
		return self.chords.isOutputting()

	def getSignal(self):
		return self.chords

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

	def reset(self):
		self.setIntensity(0.5)
		self.setHFA(0.5)
		self.setDryWet(0.5)

	def enable(self, output):
		self.reverb.setInput(output)
		self.reverb.out()

	def disable(self):
		self.reverb.reset()
		self.reverb.stop()

	def setInput(self, x):
		self.reverb.setInput(x)

class DelayEFF():
	def __init__(self, cleanS):
		self.delayAmount = 0.25
		self.feedback = 0.0

		self.delay = Delay(cleanS, delay = self.delayAmount, feedback = self.feedback)

	def setDelay(self, delayAmount):
		self.delay.setDelay(delayAmount)

	def setFeedback(self, feedback):
		self.delay.setFeedback(feedback)

	def reset(self):
		self.setDelay(0.25)
		self.setFeedback(0.0)

	def enable(self, output):
		self.delay.setInput(output)
		self.delay.out()

	def disable(self):
		self.delay.reset()
		self.delay.stop()

	def setInput(self, x):
		self.delay.setInput(x)
