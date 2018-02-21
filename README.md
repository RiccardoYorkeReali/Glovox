# Glovox
![logo](https://user-images.githubusercontent.com/29773493/36478291-881e7160-1704-11e8-8749-454cdcc20929.png)

## Assignment
Build a musical instruments (consisting of a glove with a microphone) that let the user use his voice as a musical instrument.
The users must be able to select an effect from an application and apply it to his voice, which is captured by the **Glovox**.
The idea comes from one of the Primiata Forneria Marconi’s singer, Bernardo Lanzetti.

## Goals
 - Find a way to convert the audio input in a digital signal.
 - Real-Time processing of the digital signal, so that to modify it with the application.
 - Implement a GUI application that allow the user to manage the effects desired.
 - Build the physical instrument, consisting of a glove and a microphones.

## Technologies
 - Real-time audio Processing is done using a Python free library called **Pyo**.
 - The interface is developed with the PyQt Framework using Python. 
 - Waveform of audio signal is done using NumPy package.
 - The glove has been created using a mini-jack microphone and a glove of synthetic fabric.

## Realization
### Analog to Digital Conversion
The ideal device should have brought **portability** and **low latency** to the system.
Because of the sampling capacity and the delay a compromise was found.
**Focusrite Saffire** audio card has been used to output the signal and the computer itself to convert the input.

### Model-View-Controller
**MVC** pattern has been used to create the control GUI application that the user uses to manage the available effects. In particular, we used Pyo to realize the model. 

### Pyo
Real-Time Digital Signal Processing (RT DSP) has been realized using Python and Python’s module called **Pyo**.
Pyo contain classes for a wide variety of audio signal processing.
With Pyo, the user will be able to include signal processing chains directly in Python scripts or projects, and to manipulate them in real-time through the interpreter.

Pyo offers primitives, like mathematical operations on audio signals, basic signal processing (filters, delay, synthesis generators, etc), but also complex algorithms to create audio manipulations.
Pyo also supports the MIDI protocol for generating sound events and controlling process parameters.

### Glovox (The Model)
This class is used to keep track of the references of every effect: so, the View/Controller communicates just with this class and delegates to it the management of the effects.
It is responsible of starting **Pyo’s Server**.
Contains methods to get, enable and disable the effects, and some methods, based on **Pyo’s Tables**, to create the waveform of the currently selected signal.

### Effects
Effects can be divided in **Pyo’s special effects** and **Pyo’s signal generator**.
The first one use a signal generator called Input. This generator is used to get the microphone’s signal in Real-Time. With Input we can create some effects like Distortion, Harmonizer, Auto-Wah, Reverb and Delay.
The other effects consist in some synthesized sounds. This sounds are obtained using signal generators and they are created based on a frequency range which is computed using a Gate on the input signal. We included the following effects: Super Saw, Blit, Phasor, Sinusoidal Oscillator, RC Oscillator and Low Filter Oscillator.

### Interface
The GUI of Glovox has been realized using **PyQt5**. At startup the application will present itself with a simple interface.
Initially, no effect is activated, but only the original signal from the microphone is processed.
<img width="829" alt="interface3" src="https://user-images.githubusercontent.com/29773493/36478381-c2f6b0e0-1704-11e8-827f-f9a061fdee01.png">

The GUI provide a list to choose the effect and three boxes to vary parameters of Reverb, Delay and the chosen effect.
Also, it’s present a box to show the waveform of every effect.
It is possible to get a brief description of the effect and its parameters.
<img width="827" alt="interface4" src="https://user-images.githubusercontent.com/29773493/36478415-e40188be-1704-11e8-8886-ae33c932ebf0.png">
<img width="841" alt="interface5" src="https://user-images.githubusercontent.com/29773493/36478416-e4447e12-1704-11e8-96c4-656393988a32.png">

### Glove
The Glove has been created using a mini-jack microphone and a glove of synthetic fabric. 
The microphone has then been sewn inside the glove in such a way to put the sensors exactly halfway between the thumb and the forefinger.
![glove](https://user-images.githubusercontent.com/29773493/36478619-acd96824-1705-11e8-8331-921f429f7cd3.jpg)


The Glove can be used, connecting the jack to the computer, the computer to the audio card, launching the application and singing with the glove under the throat.

<img width="388" alt="reo" src="https://user-images.githubusercontent.com/29773493/36478750-484b88f0-1706-11e8-9889-99a55f6f6e05.png">

## Usability Test
To test the usability of the Glovox, we choose a SEQ test composed by twelve questions, that can be evaluated from 1 to 7.
The test took place in a comfortable room, with two surrounding speakers and the microphone’s input volume lowered to the minimum possible, due to the unpleasant effect created by the feedback of the speakers.
Before starting the test, we gave a brief explanation of what Glovox is and does.

### Tasks
Tasks:
 - Put the Glove under your throat. 
 - Now, take confidence with your voice and try to sing some notes.
 - Try to enable the Harmonizer effect and enjoy using it!
 - Try to vary between all the available chords. 
 - Try to enable Reverb and to vary its parameters, as you want.
 - Now, change effect and enable Super Saw.
 - Vary its parameters, as you want.
 - If you want, enable Delay and/or Reverb and vary their parameters.
 - Now you’re free! Enjoy Glovox doing whatever you want!

### SEQ
We examined a population of thirteen interviewees.
Before making global consideration overall the answers, we used the twelfth question to divide the population between musicians and non-musicians.
For a rate greater than 4, we considered the interviewee a musician, otherwise we considered him a non-musician. 
Each question has been evaluated with the average and the standard deviation of the collected rates.

**Musicians**
<img width="825" alt="res" src="https://user-images.githubusercontent.com/29773493/36479305-799f5b1e-1708-11e8-9a0d-c5dde8742630.png">

**Non Musicians**
<img width="825" alt="res2" src="https://user-images.githubusercontent.com/29773493/36479307-7a200598-1708-11e8-9086-eab9853d986d.png">

**Global Evaluation**
<img width="830" alt="res3" src="https://user-images.githubusercontent.com/29773493/36479308-7a82e38e-1708-11e8-8cbf-b9683524a3ab.png">

## Conclusion
 - The results of the Usability tests highlighted the potential of Glovox.
 - A problem of Glovox has been the amount of noise, while the sound latency has not been very considerable, despite our previsions. 
 - An improvement concerns the possibility of using a jack directly connected to the audio card removing the latency that we encountered at the first steps of the project.
 - We should also consider the idea of making a portable version of Glovox, for example using a device with an LCD screen and potentiometers - or touch screen displaying the GUI - instead of the computer and the audio card.
