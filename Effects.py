from pyo import *

#EFFECTS
"""Each effect has the related signal as attributes, getter and setter methods for each effect's parameters, 
enabling, disabling and resetting method. A description of each effect can be found in effects.json file."""

class NoEFF():
	def __init__(self, cleanS):
		self.signal = cleanS

	def enable(self):
		self.signal.out()

	def disable(self):
		self.signal.stop()

	def isOutputting(self):
		return self.signal.isOutputting()

	def getSignal(self):
		return self.signal

class DistortionEFF():
	def __init__(self, cleanS):
		self.dist = Disto(cleanS, drive = 0.75, slope = 0.5)

	def setDrive(self, drive):
		self.dist.setDrive(drive)

	def getDrive(self):
		return self.dist.drive

	def setSlope(self, slope):
		self.dist.setSlope(slope)

	def getSlope(self):
		return self.dist.slope

	def reset(self):
		self.setDrive(0.75)
		self.setSlope(0.5)

	def enable(self):
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

	def enable(self):
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

class SineEFF():
	def __init__(self, gatedS, freqS):
		self.sine = Sine(freqS, phase = 0, mul = 0.2*gatedS)

	def setPhase(self, phase): # valutare se metterlo questo parametro tanto non cambia nulla
		self.sine.setPhase(phase)

	def getPhase(self):
		return self.sine.phase

	def reset(self):
		self.setPhase(0)

	def enable(self):
		self.sine.out()

	def disable(self):
		self.sine.stop()

	def isOutputting(self):
		return self.sine.isOutputting()

	def getSignal(self):
		return self.sine

class BlitEFF():
	def __init__(self, gatedS, freqS):
		self.blit = Blit(freqS, harms=40, mul=0.2*gatedS)

	def setHarms(self, harms):
		self.blit.setHarms(harms)

	def getHarms(self):
		return self.blit.harms

	def reset(self):
		self.setHarms(40)

	def enable(self):
		self.blit.out()

	def disable(self):
		self.blit.stop()

	def isOutputting(self):
		return self.blit.isOutputting()

	def getSignal(self):
		return self.blit

class SuperSawEFF():
	def __init__(self, gatedS, freqS):
		self.superSaw = SuperSaw(freqS, detune = 0.5, bal = 0.7, mul = 0.2*gatedS)

	def setDetune(self, detune):
		self.superSaw.setDetune(detune)

	def getDetune(self):
		return self.superSaw.detune

	def setBal(self, bal):
		self.superSaw.setBal(bal)

	def getBal(self):
		return self.superSaw.bal

	def reset(self):
		self.setDetune(0.5)
		self.setBal(0.7)

	def enable(self):
		self.superSaw.out()

	def disable(self):
		self.superSaw.stop()

	def isOutputting(self):
		return self.superSaw.isOutputting()

	def getSignal(self):
		return self.superSaw

class PhasorEFF():
	def __init__(self, gatedS, freqS):
		self.phasor = Phasor(freqS, phase = 0, mul = 0.2*gatedS)

	def setPhase(self, phase):
		self.phasor.setPhase(phase)

	def getPhase(self):
		return self.phasor.phase

	def reset(self):
		self.setPhase(0.0)

	def enable(self):
		self.phasor.out()

	def disable(self):
		self.phasor.stop()

	def isOutputting(self):
		return self.phasor.isOutputting()

	def getSignal(self):
		return self.phasor

class RCOscEFF():
	def __init__(self, gatedS, freqS):
		self.rc = RCOsc(freqS, sharp = 0.25, mul = 0.2*gatedS)

	def setSharp(self, sharp):
		self.rc.setSharp(sharp)

	def getSharp(self):
		return self.rc.sharp

	def reset(self):
		self.setSharp(0.25)

	def enable(self):
		self.rc.out()

	def disable(self):
		self.rc.stop()

	def isOutputting(self):
		return self.rc.isOutputting()

	def getSignal(self):
		return self.rc

class LFOEff():
	def __init__(self, gatedS, freqS):
		self.lfo = LFO(freqS, type = 0, mul = 0.2*gatedS)

	def setSawUp(self):
		self.lfo.setType(0)

	def setSawDown(self):
		self.lfo.setType(1)

	def setSquare(self):
		self.lfo.setType(2)

	def setTriangle(self):
		self.lfo.setType(3)

	def setPulse(self):
		self.lfo.setType(4)

	def setBipolarPulse(self):
		self.lfo.setType(5)

	def setSnH(self):
		self.lfo.setType(6)

	def setModSine(self):
		self.lfo.setType(7)

	def reset(self):
		self.setSawUp()

	def enable(self):
		self.lfo.out()

	def disable(self):
		self.lfo.stop()

	def isOutputting(self):
		return self.lfo.isOutputting()

	def getSignal(self):
		return self.lfo

class ReverbEFF():
	def __init__(self, cleanS):
		self.stereoRev = STRev(cleanS, revtime = 1.0, cutoff = 5000, roomSize = 1.0, bal = 0.5)

	def setRevTime(self, revTime):
		self.stereoRev.setRevtime(revTime)

	def getRevTime(self):
		return self.stereoRev.revtime

	def setCutoff(self, cutoff):
		self.stereoRev.setCutoff(cutoff)

	def getCutoff(self):
		return self.stereoRev.cutoff

	def setRoomSize(self, roomSize):
		self.stereoRev.setRoomSize(roomSize)

	def getRoomSize(self):
		return self.stereoRev.roomSize

	def setBal(self, bal):
		self.stereoRev.setBal(bal)

	def getBal(self):
		return self.stereoRev.bal

	def reset(self):
		self.setRevTime(1)
		self.setCutoff(5000)
		self.setRoomSize(1.0)
		self.setBal(0.5)

	def enable(self, output):
		self.stereoRev.setInput(output)
		self.stereoRev.out()

	def disable(self):
		self.stereoRev.reset()
		self.stereoRev.stop()

	def setInput(self, x):
		self.stereoRev.setInput(x)


class DelayEFF():
	def __init__(self, cleanS):
		self.d = Delay(cleanS, delay = 0.25, feedback = 0)

	def setDelayAmount(self, delayAmount):
		self.d.setDelay(delayAmount)

	def getDelayAmount(self):
		return self.d.delay

	def setFeedback(self, feedback):
		self.d.setFeedback(feedback)

	def getFeedback(self):
		return self.d.feedback

	def reset(self):
		self.setDelayAmount(0.25)
		self.setFeedback(0.0)

	def enable(self, output):
		self.d.setInput(output)
		self.d.out()

	def disable(self):
		self.d.reset()# this reset is Pyo's reset function, not our custom one
		self.d.stop()

	def setInput(self, x):
		self.d.setInput(x)
