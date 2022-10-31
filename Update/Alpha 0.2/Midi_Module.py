import mido

"""
pedal_counter = 0
    if i[0] == "control_change":
        pedal_counter += 1
"""

def Init_Midi_Filter(midi_path): # Initial filtering of midi file
    # Get important Metadata
    path = midi_path
    mid = mido.MidiFile(path, clip=True)
    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000  # Standart tempo representation for 120bpm

    # counter = 0
    # Save relevant midi data as .txt

    mid_str = ""
    for event in mid.tracks[0]:
        if not event.is_meta: # Gets Events
            mid_str =mid_str + str(event) + "\n"


    mid_str = mid_str[:-1]  # Eliminates last empty new line
    mid_array = mid_str.split("\n")

    summed_midi_events = []
    for i in mid_array:
        data = i.split(" ")
        summed_midi_events.append(data)
    
    # print("Midi create counter:", counter)
    with open("Assets/temp_files/midi.txt", "w+") as txt:
        txt.write(mid_str)
    # return summed_midi_events, ticks_per_beat, tempo

    def Calc_Abs_Onset(mid, ticksperbeat, tempo):
        total_time = 0 
        last_event_ticks = 0
        microseconds = 0

        parsed_midi_with_onsets = []

        for event in mid:
            event_data_ticks = event[4]
            event_data_ticks = event_data_ticks.split("=")
            event_data_ticks = event_data_ticks[1]
            event_data_ticks = float(event_data_ticks)
            # print(event_data_ticks)

            delta_ticks = event_data_ticks - last_event_ticks
            last_event_ticks = event_data_ticks
            delta_microseconds = tempo * delta_ticks / ticksperbeat
            microseconds += delta_microseconds
            # print(microseconds)
            total_time += microseconds

            # event_data_onset = f"onset={total_time}"
            event_data_onset = total_time

            event.append(event_data_onset)
            parsed_midi_with_onsets.append(event)

        def pedal_filter(midi_event_list):
            pedal_container_array = []
            event_container_without_pedal = []
            for event in mid:
                if event[0] == "control_change":
                    pedal_container_array.append(event)
                else:
                    event_container_without_pedal.append(event)
            return pedal_container_array, event_container_without_pedal

        pedal_list, midi_note_list = pedal_filter(parsed_midi_with_onsets)

        return parsed_midi_with_onsets, pedal_list, midi_note_list

    COMPLETE_midi_array, pedal_array, notes_array = Calc_Abs_Onset(summed_midi_events,ticks_per_beat, tempo)
    return COMPLETE_midi_array, pedal_array,notes_array

def main(midi_path):
    full_midi, pedal_array, notes_array = Init_Midi_Filter(midi_path)
    print("Original midievent len;",len(full_midi))
    return full_midi, pedal_array, notes_array

if __name__ == "__main__":
    main()
