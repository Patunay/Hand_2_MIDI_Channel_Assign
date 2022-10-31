import mido
# Development/Assets/Midi_assets/midi_asset2.mid

def Consolidate_Midi(): 
    path = "MIDI_OUT/out.mid"
    mid = mido.MidiFile(path, clip=True)
    counter = 0

    meta_cnt = 0
    only_events = []

    for event in mid.tracks[0]:
        if event.is_meta:  # Gets Metadata
            meta_cnt += 1
            continue
        elif not event.is_meta: # Gets Events
            # event.channel = 2
            # only_events.append(event)
            print(event)
    # only_events = mid.tracks[0]
    # only_events = only_events[meta_cnt:]

    # print(mid.tracks[0][0])
    # print(only_events)







    # for event in mid.tracks[0]:
    #     print(event)
    #     counter += 1

    #     # if event.is_meta:  # Gets Metadata
    #     #     # # track.append(event)
    #     #     # print(event)
    #     #     # track.append(event)
    #     #     continue
    #     # elif not event.is_meta: # Gets Events
    #     #     event.channel = 2
    #         # track.append(event)
    # # out_mid.save("MIDI_OUT/oruebaout.mid")
    # print("Final Counter",counter) 

    return 




Consolidate_Midi()