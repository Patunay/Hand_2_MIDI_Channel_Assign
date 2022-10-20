import mido

def Consolidate_Midi(midi_path, handness_array): 
    path = midi_path
    mid = mido.MidiFile(path, clip=True)

    out_mid = mido.MidiFile()
    track = mido.MidiTrack()
    out_mid.tracks.append(track)


    counter = 0
    for event in mid.tracks[0]:
        if not event.is_meta: # Gets Events
            counter += 1

    meta_msg_cnt = 0
    for i in mid.tracks[0]:
        if i.is_meta:  # Gets Metadata
            track.append(i)
            meta_msg_cnt += 1
    meta_msg_cnt = meta_msg_cnt - 1
    only_events = mid.tracks[0]
    only_events = only_events[meta_msg_cnt:]

    print(len(only_events))
    print(len(handness_array))

    for origin_mid_event, handness in zip(only_events,handness_array):
        if not origin_mid_event.is_meta: # Gets Events
            # counter += 1
            if handness[1] == "Left":
                origin_mid_event.channel = 2
                track.append(origin_mid_event)
            elif handness[1] == "Right":
                origin_mid_event.channel = 5
                track.append(origin_mid_event)
            else: # If Pedal
                # print("Pedal?")
                # print("Origin:",origin_mid_event)
                origin_mid_event.channel = 1
                track.append(origin_mid_event)
                # print("Update:",origin_mid_event,"\n")


    # for i in mid:
    #     print(i)
    # print("final", counter)

    out_mid.save("MIDI_OUT/out.mid")


    # mid_eval = mido.MidiFile(path, clip=True)
    # counter = 0
    # for event in mid_eval.tracks[0]:
    #     if not event.is_meta: # Gets Events
    #         counter += 1

    # print("Final Counter",counter) 
    return 


def main(midi_path,handness_list):
    Consolidate_Midi(midi_path,handness_list)
    return

if __name__ == "__main__":
    main()
# main("Development/Assets/Midi_assets/midi_asset2.mid")