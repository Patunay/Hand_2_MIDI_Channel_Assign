import cv2 as cv


def Video_Midi_Sync(vidPath): # Returns frame which corresponds to first midi event
    # Set Frame location on first midi event
    cap = cv.VideoCapture(vidPath)
    # width, height = new_Dimensions[0],new_Dimensions[1]
    fps = cap.get(cv.CAP_PROP_FPS)
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))-1
    duration = frame_count/fps
    print("FPS: ",fps)
    print("Total Frames[From 0]: ",frame_count)
    minutes = int(duration/60)
    seconds = duration%60
    print('Total duration (M:S): ' + str(minutes) + ' : ' + str(seconds))
    print()

    first_event_location_ms = int(input("Enter location(ms) that corresponds to 1st midi event: "))  # Input inquiry frame
    last_event_location_ms = int(input("Enter location(ms) that corresponds to last midi event: "))  # Input inquiry frame
    return (first_event_location_ms, last_event_location_ms)


def main(vid_path):
    sync_onsets = Video_Midi_Sync(vid_path)
    return sync_onsets

if __name__ == "__main__":
    main()