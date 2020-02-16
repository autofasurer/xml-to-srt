import xml.etree.ElementTree as ET
import os, argparse


def stringToTimecode(tc):
    #convert the int tc into hours, minutes, seconds and frames
    frames = (tc%25)*40 #.srt files take frames in milliseconds, hence the *40
    seconds = ((tc-(tc%25))//25)%60
    minutes = ((tc-(tc%25))//25)//60
    hours = seconds//3600
    return f'{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)},{str(frames).zfill(3)}'

def main():
    #setup the argument parser, add the requred filename and set the var file to the path/filename provided
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required=True, help="Path to .xml to convert")
    args = vars(ap.parse_args())
    file = args["filename"]

    filename = os.path.basename(file)[:-4] #get the name of the file without location or TLA filetype - used to name the .srt file lateron
    filenamePath = os.path.dirname(file) #the absolute path of the input file, .srt will be created in the same location

    tree = ET.parse(file) #parse the xml file
    root = tree.getroot()
    sub = root.findall('.//clipitem/filter/')
    start = root.findall('.//clipitem/start')
    end = root.findall('.//clipitem/end')

#Filter out the elements <name> which are empty or are part of another type of <filter>
    subtitles = []
    for subs in sub:
        if subs[1].text == 'GraphicAndType':
            if subs[0].text is not None and len(subs[0].text) > 1:
                subtitles.append(subs[0].text)

    with open(f"{filenamePath}/{filename}.srt", 'w+') as export:
        num = 1
        for i, sub in enumerate(subtitles):
            export.write(f'{num}\n{stringToTimecode(int(start[i].text))} --> {stringToTimecode(int(end[i].text))}\n{sub}\n\n')
            num += 1


if __name__ == "__main__":
    main()
