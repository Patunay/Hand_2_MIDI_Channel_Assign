# Hands2MIDIChannels <font size="3" >_by Carlos Mauro_ </font>

## _Automatic hand assignation algorithm for keyboard instruments recordings_

_Nov, 2022_

## Alpha 0.2 update:

- Video preparation process overhaul.

  - It now requires less user input.
  - Better results faster.

- Contour finetuning module added [Contour_finetuning.py].

  - The user now has the ability to correct the position of the keyboard key's contours.
  - For the black keys:
    - Distribution of inner contours on the X axis is automatically computed based on the user defined value corresponding to the "Anchor keys contour position".
  - For White keys:
    - Distribution of inner contours as well as their individual width are automatically computed based on the user defined value corresponding to the "Anchor keys contour position"
  - This solved a prevalent issue in the previous version where automatically generated contours did not matched the reference video input.

  - Preliminary contour creation process adjusted.
    - Now it only creates contours, there is no need to attatch it to a midi number yet.
  - Midi note numbers are attatched to their corresponding contours only after Contour_finetuning.py finishes updating the contours.

- Simplification of code and improvement of comments.

  - Some modules in the previous version [Alpha 0.1] where redundant.
  - For some other modules, there was no justification for them to be treated as modules.
  - These modules have been added to Driver.py as functions.

- Fixed bugs, improved logical gates, and improved the hand recognition code at [Compare_update.py]
  - Bug on [closest_contour_check()] method where it gave wrong assesments is now fixed.
  - There are now 4 logical gates that [Compare_update.py] uses to arrive to a guess regarding which hand played a inquired MIDI event.
    - [1] No hand detected.
    - [2] One hand detected.
    - [3] Check if a hand is inside the pertinent contour.
    - [4] Check which hand is closest to the pertinent contour.
  - Regarding hand recognition code improvements:
    - For the purposes of this program, the algorithm only needs to get the position of the finguertips on each hand. Other hand landmark data is irrevant and ignored by [Compare_update.py] significantly improving processing time and guess accuracy.
    - Improved code on handedness determination for each detected hand.

### Coming up soon:

- Fix unwanted messages that are outputed to the terminal regarding Tk() isntances update when the Tk() instance was already terminated.

### Eventually:

- Overhaul video/MIDI syncronization.
  - In theory, the user only needs to input the start onset of a MIDI file as it is represented in the corresponding video.
  - However, while working on this module, I found that they tend to become out sync linearly as the algoprithm iterates thorough the MIDI events in the MIDI file.
  - To solve this, the algorithm asks for two inputs:
    - Start Onset.
      - Onset for first midi event as it is shown in the video.
    - End Onset.
      - Onset for last midi event as it is shown in the video.
  - The algorthm then scales the onset data to the user defined range and gives accurate results.
  - Eventually, I want the algoruthm to only need the first onset and to give the same or better results.

_Oct, 2022_

## Alpha 0.1 update:

- First working iteration of the algorithm.
- Accuracy: ~82%
- Countour assignation for static keys needs refining:
  - For the black keys, they there is a noticable offset between calculated and actual area

### Coming up soon:

- Contour assignation fix:
  - In the next update, a contour area fine tuning will be added to compensate for any posisble offset.

### Eventually:

- Refine logical gates at Compare.py to increase output accuracy as well as improving the overall algoruithm speed.
