import Midi_Module

def Midi_event_onset_2_frame(sync_onsets,midi_path):   # Creates corresponding video onsets for midi events

    def onset_fix(inquiry,final_max,final_min,inq_max,inq_min): # mapping function: intup_range -> [mapping funciton] -> outpuit_range
        fixed = inquiry - inq_min
        fixed = fixed / (inq_max-inq_min)
        fixed = fixed * (final_max-final_min)
        fixed = fixed + final_min
        return fixed

    full_mid,ped_array, note_array = Midi_Module.main(midi_path)

    delta = full_mid[0][5]
    # print(delta)
    normalized_onsets = []
    for i in full_mid:
        norm_onset = i[5] - delta
        norm_onset = norm_onset + sync_onsets[0]
        normalized_onsets.append(norm_onset)

    inq_max = max(normalized_onsets)
    inq_min = min(normalized_onsets)
    final_max = sync_onsets[1]
    final_min = sync_onsets[0]

    fixed_onsets = []
    for i in normalized_onsets:
        i = onset_fix(i,final_max,final_min,inq_max,inq_min)
        fixed_onsets.append(i)

    norm_ons2 = []
    for i , e in zip(full_mid,fixed_onsets):
        i.append(e)
        norm_ons2.append(i)

    # with open("Development/Assets/temp_files/checkonsetconversion.txt","w+") as f: # for debugging only
    #     for i in norm_ons2:
    #         i = str(i) + "\n"
    #         f.write(i)
    return norm_ons2




def main(sync_onsets,midi_path):
    synqued_midi_data = Midi_event_onset_2_frame(sync_onsets,midi_path)
    print("midievent len after fixing onsets;",len(synqued_midi_data))
    return synqued_midi_data

if __name__ == "__main__":
    main()