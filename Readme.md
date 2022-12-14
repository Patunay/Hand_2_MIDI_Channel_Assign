# Hands2MIDIChannels <font size="3" >_by Carlos Mauro_ </font>

**Copyright © CMG Solutions - All Rights Reserved**

Unauthorized copying of files in this repository, via any medium is **strictly prohibited**

**Proprietary and confidential**

_Written by Carlos Camilo Mauro Galvez [cmg.solutions.a@gmail.com], 11/02/2022_

## Introduction:

Hands2MIDIChannels is a software that aims to provide music composers, improvisers and keyboard instrument performers a tool that will automatically analyze a MIDI file and assigns a MIDI channel depending on which hand played a MIDI event.

This is done by comparing the MIDI file with the a corresponding top-view video recording showing the performer's hands over the keyboard while the MIDI recording is taking place.

At the the current state of the main algorithm in Hands2MIDIChannels, it can only do the analysis after the recording has been made. However, as I work on improving the efficiency of the algorithm, real-time processing is a possibility.

Hands2MIDIChannels is powered by openCV, Mediapipe, and MIDO.

**Current stable version: Alpha 0.2**

## In this repository:

- Archive:
  - Stores the code for all obsolete versions of Hands2MIDIChannels since the first version.
- Assets:
  - Stores MIDI assets for testing purposes.
- Current Version:
  - Stores the current version.
- Update:
  - Stores the files that are being used in the update.
