import mido

def Consolidate_Midi(midi_path, handness_array): 
    path = midi_path
    mid = mido.MidiFile(path, clip=True)

    out_mid = mido.MidiFile()
    track = mido.MidiTrack()
    out_mid.tracks.append(track)

    meta_msg_cnt = 0
    for i in mid.tracks[0]:
        if i.is_meta:  # Gets Metadata
            track.append(i)
            meta_msg_cnt += 1
    meta_msg_cnt = meta_msg_cnt - 1
    only_events = mid.tracks[0]
    only_events = only_events[meta_msg_cnt:]

    for origin_mid_event, handness in zip(only_events,handness_array):
        if not origin_mid_event.is_meta: # Gets Events
            if handness[1] == "Left":
                origin_mid_event.channel = 1
                track.append(origin_mid_event)
            elif handness[1] == "Right":
                origin_mid_event.channel = 5
                track.append(origin_mid_event)
            elif handness[1] == None:
                origin_mid_event.channel = 3
                track.append(origin_mid_event)               
            else: # If Pedal
                origin_mid_event.channel = 0
                track.append(origin_mid_event)
    out_mid.save("Current Version/Alpha 0.2/MIDI_OUT/out.mid")
    return 

def main(midi_path,handness_list):
    Consolidate_Midi(midi_path,handness_list)
    return

if __name__ == "__main__":
    main()