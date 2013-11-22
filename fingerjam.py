#!/usr/bin/python
import Tkinter, sys
from threading import Timer
from serial import Serial
import fluidsynth
from time import sleep

keys = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']
keyBases={'C':'C4','C#':'C#4','D':'D4','Eb':'Eb4','E':'E4','F':'F4','F#':'F#4','G':'G3','A':'A3','Ab':'Ab3','Bb':'Bb3','B':'B3'}
keyCodes={"G5":59,"F#5":58,"F5":57,"E5":56,"Eb5":55,"D5":54,"C#5":53,"C5":52,"B4":51,"Bb4":50,"A4":49,"Ab4":48,"G4":47,"F#4":46,"F4":45,"E4":44,"Eb4":43,"D4":42,"C#4":41,"C4":40,"B3":39,"Bb3":38,"A3":37,"Ab3":36,"G3":35}
noteMap = {30: 4, 35: 3, 40: 2, 45: 1, 48: 0}
pad = 50
endpad = 60
threshold = 300

class Keyboard:
  def __init__(self, sf2):
    self.key = "C#"
    self.shift = 0
    self.minor = False
    if (self.minor):
      self.buildMinor(self.key)
    else:
      self.buildMajor(self.key)
    
    self.fs = fluidsynth.Synth()
    self.fs.start("alsa")
    sfid = self.fs.sfload(sf2)
    self.fs.program_select(0, sfid, 0, 0)

    self.sounds = {}

  def printKey(self):
    m = ""
    if self.minor:
      m = "m"
    print self.key+m
    
  def play(self, note, volume):
    if not note:
      return
    if note in self.sounds:
      self.adjust(note, volume)
    else:
      self.sounds[note] = Sound(self, note, volume)
      self.sounds[note].start()

  def adjust(self, note, volume):
    if note in self.sounds:
      sound = self.sounds[note]
      sound.adjust(volume)

  def stop(self, note):
    if note in self.sounds:
      sound = self.sounds[note]
      sound.stop()

  def changeMode(self):
    self.changeKey(self.key, not self.minor)

  def changeKey(self, key, minor):
    self.shift = 0
    self.key = key
    self.minor = minor
    if not minor:
      self.buildMajor(key)
    else:
      self.buildMinor(key)
    self.printKey()

  def buildMajor(self, key):
    base = keyCodes[keyBases[key]]
    self.notes = [base] #1st
    self.notes.append(base+2) #2nd
    self.notes.append(base+4) #3rd
    self.notes.append(base+5) #4th notpent
    self.notes.append(base+7) #5th
    self.notes.append(base+9) #6th
    self.notes.append(base+11) #7th notpent
    self.notes.append(base+12) #8th
    self.notes.append(base+14) #7th notpent
    self.notes.append(base+16) #8th
  
  def buildMinor(self, key):
    base = keyCodes[keyBases[key]]
    self.notes = [base]
    self.notes.append(base+2) #2rd notpent
    self.notes.append(base+3) #3rd
    self.notes.append(base+5) #4rd
    self.notes.append(base+7) #5th
    self.notes.append(base+8) #6th notpent
    self.notes.append(base+10) #7th
    self.notes.append(base+12) #8th
    self.notes.append(base+14) #8th
    self.notes.append(base+15) #8th

  def shiftUp(self):
    self.shift += 1
    if self.notes[3] + 12 > 88:
      return
    self.notes.pop(0)
    self.notes.append(self.notes[2] + 12)
    if self.shift % 7 == 0:
      print "Octave"
  
  def shiftDown(self):
    self.shift -= 1
    if self.notes[-4] - 12 < 1:
      return
    self.notes.pop()
    self.notes.insert(0, self.notes[-3] - 12)
    if self.shift % 7 == 0:
      print "Octave"

class Sound:
  def __init__(self, keyboard, note, volume):
    self.keyboard = keyboard
    self.note = note
    self.volume = volume

  def start(self):
    self.keyboard.fs.noteon(0, self.note, self.volume)
  
  def adjust(self, volume):
    self.volume = volume
    self.keyboard.fs.cc(self.note, 7, volume)

  def stop(self):
    self.keyboard.fs.noteoff(0, self.note)
    if self.note in self.keyboard.sounds:
      self.keyboard.sounds.pop(self.note)

class App:
  
  def __init__(self, sf2):
    # Set up the frame
    self.root = Tkinter.Tk()
    self.frame = Tkinter.Frame(self.root, width=100, height=100)
     
    # set up a mouse event
    self.frame.bind("<Button-1>", self.click)
    self.frame.bind("<Button-3>", self.click3)
    self.frame.bind("<Button-4>", self.wheelup)
    self.frame.bind("<Button-5>", self.wheeldown)
    self.frame.pack()

    # This call gives the frame focus so that it receives input.
    self.frame.focus_set()
    
    self.curkey = 0
    self.keyboard = Keyboard(sf2)
    
    try:
      ser = Serial('/dev/ttyUSB0', 9600)
      sleep(1)
      print "...connected!"

    except:
      print "Couldn't connect!"
      sys.exit(1)


    try:
        count = 0 
        endcount = 0
        reading = False
        readingNote = False
        note = None
        a = False
        while True:
            data = ser.read(1)
            if len(data) == 0: break
            val = ord(data)
            if reading:
              if readingNote:
                if val > 2:
                  self.keyboard.play(note, 127) 
                else:
                  self.keyboard.stop(note)
                readingNote = False
                note = None
              elif val in noteMap:
                  note = self.getNote(noteMap[val])
                  if val == 50:
                    a = True
                  else:
                    a = False
                  readingNote = True
              elif val == endpad:
                endcount += 1
                if endcount == 4:
                  endcount = 0
                  reading = False
                  continue
              else:
                endcount = 0
            else:
              if val == pad:
                count += 1
                if count == 4:
                  count = 0
                  reading = True
              else:
                count = 0
            
    except IOError:
        pass

    print "disconnected"

    ser.close()

  def click(self, event):
    self.curkey += 1
    if self.curkey >= len(keys):
      self.curkey = 0
    self.keyboard.changeKey(keys[self.curkey],minor=False)
  
  def wheeldown(self, event):
    self.keyboard.shiftDown()
  
  def wheelup(self, event):
    self.keyboard.shiftUp()

  def click3(self, event):
    self.keyboard.changeMode()

  def getNote(self, ind):
    return self.keyboard.notes[ind]

if __name__ == "__main__":
  import optparse,sys
  from os import path
  op = optparse.OptionParser()
  op.add_option("-s", "--sf2", help="Path to sf2")
  (options, args) = op.parse_args()
  if not options.sf2:
    options.sf2 = "sf2/piano.sf2"
  if not path.exists(options.sf2):
    other = "sf2/"+options.sf2+".sf2"
    if not path.exists(other):
      print "SF2 not found:", options.sf2
      sys.exit(1)      
    else:
      options.sf2 = other
  App(options.sf2)

