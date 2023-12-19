# racefile renamer

import os

filetype = "mkv"
raceseries = "Formula1"

def listfiles():
    filelist = os.listdir('sourcefiles/')
    return filelist
    #return ("Formula1.2023.Round19.USA.COTA.Teds.Race.Notebook.Sky.F1TV.WEB-DL.1080p.H264.English-DC46.mkv")


def parsefilename(sourcefilename):
    for i, c in enumerate(sourcefilename):
    #    print(sourcefilename[i:i+18])
        if c == "T":
            if sourcefilename[i:i+18] == 'Teds.Race.Notebook':
                racesession = sourcefilename[i:i+18]
                racename = sourcefilename[22:i-1]
                #print("race name is: " + racename)
                raceinfo = sourcefilename[i+19:-4]
                raceepisode = '13'
                return (racename, raceepisode, racesession, raceinfo)
        if c == "F":
            if sourcefilename[i:i+2] == 'FP':
                racesession = sourcefilename[i:i+3]
                #print("found FP")
                racename = sourcefilename[22:i-1]
                raceinfo = sourcefilename[i+4:-4]
                if racesession == 'FP1':
                    raceepisode = '01'
                elif racesession == 'FP2':
                    raceepisode = '05'
                elif racesession == 'FP3':
                    raceepisode = '09'
                return (racename, raceepisode, racesession, raceinfo)
        if c == "Q":
            if sourcefilename[i:i+10] == 'Qualifying':
                racesession = sourcefilename[i:i+10]
                racename = sourcefilename[22:i-1]
                raceinfo = sourcefilename[i+11:-4]
                raceepisode = '03'
                return (racename, raceepisode, racesession, raceinfo)
        if c == "R":
            if sourcefilename[i:i+4] == 'Race' or sourcefilename[i:i+4] == 'RACE':
                racesession = sourcefilename[i:i+4]
                racename = sourcefilename[22:i-1]
                raceinfo = sourcefilename[i+5:-4]
                raceepisode = '11'
                return (racename, raceepisode, racesession, raceinfo)
        if c == "S":
            if sourcefilename[i:i+15] == 'Sprint.Shootout':
                racesession = sourcefilename[i:i+15]
                racename = sourcefilename[22:i-1]
                raceinfo = sourcefilename[i+16:-4]
                raceepisode = '06'
                return (racename, raceepisode, racesession, raceinfo)
            elif sourcefilename[i:i+6] == 'Sprint':
                racesession = sourcefilename[i:i+6]
                racename = sourcefilename[22:i-1]
                raceinfo = sourcefilename[i+7:-4]
                raceepisode = '07'
                return (racename, raceepisode, racesession, raceinfo)



sourcefilenames = listfiles()

for sourcefilename in sourcefilenames:
    print()
    print("Source filename: " + sourcefilename)

    sourcefilename = sourcefilename.replace('.',' ')

    # file checks 
    if sourcefilename[-3:] == 'mp4' or sourcefilename[-3:] == 'mkv':
        filetype = sourcefilename[-3:]
        if sourcefilename[0:8] == 'Formula1':
            if sourcefilename[9:11] == '20':
                raceseason = sourcefilename[9:13]
            if sourcefilename[14:19] == 'Round':
                raceround = sourcefilename[19:21]
    
            racename, raceepisode, racesession, raceinfo = parsefilename(sourcefilename)
    
            print("Folder Name: " + raceseason + "-" + raceround + " - " + racename + " GP/")
            print("Parsed filename: " + racename + " - S" + raceround + "E" + raceepisode + " - " + racesession + " [" + raceinfo + "]." + filetype)

