import xml.etree.ElementTree as ET
import os, argparse


def string_to_timecode(tc):
    #convert the int tc into hours, minutes, seconds and frames
    frames = (tc%25)*40 #.srt files take frames in milliseconds, hence the *40
    seconds = ((tc-(tc%25))//25)%60
    minutes = ((tc-(tc%25))//25)//60
    hours = seconds//3600
    return f'{hours:02d}:{minutes:02d}:{seconds:02d},{frames:03d}'

def main():
    #setup the argument parser, add the requred filename and set the var file to the path/filename provided
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--filename", required=True, help="Path to .xml to convert")
    args = vars(ap.parse_args())
    file = args["filename"]

    filename, _ = os.path.basename(file).rsplit('.', 1) #get the name of the file without location or TLA filetype - used to name the .srt file lateron
    filename_path = os.path.dirname(file) #the absolute path of the input file, .srt will be created in the same location

    tree = ET.parse(file) #parse the xml file
    root = tree.getroot()
    sub = root.findall('.//clipitem/filter/')
    start = root.findall('.//clipitem/start') #start time of subtitle in frames
    end = root.findall('.//clipitem/end') #end time of subtitle in frames

#Filter out the elements <name> which are empty or are part of another type of <filter>
    subtitles = []
    for subs in sub:
        if subs[1].text == 'GraphicAndType':
            if subs[0].text is not None and len(subs[0].text) > 1:
                subtitles.append(subs[0].text)

    with open(f"{filename_path}/{filename}.srt", 'w+') as export:
        num = 1
        for i, sub in enumerate(subtitles):
            export.write(f'{num}\n{string_to_timecode(int(start[i].text))} --> {string_to_timecode(int(end[i].text))}\n{sub}\n\n')
            num += 1


if __name__ == "__main__":
    main()
