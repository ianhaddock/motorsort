# racefile renamer

import os

filetype = "mkv"
raceseries = "Formula1"

test_chars = ['T', 'F', 'Q', 'R', 'S']

#try:
#    os.symlink('../sourcefiles/sourcefile_names.txt', 'mediafiles/files.txt')
#except FileExistsError as err:
#    pass

def listfiles():
    filelist = os.listdir('sourcefiles/')
    return filelist


def parsefilename(sourcefilename):
    teds = False

    for i, c in enumerate(sourcefilename):
#        print(sourcefilename[i-6:i-2])
        if c in test_chars:
            print("FOUND IT! " + c)

        if c == "T":
            if sourcefilename[i:i+4] == 'Teds':
                teds = True
        if c == "F":
            if sourcefilename[i:i+2] == 'FP':
                racesession = sourcefilename[i:i+3]
                #print("found FP")
                racename = sourcefilename[22:i-1]
                raceinfo = sourcefilename[i+4:-4]
                if racesession == 'FP1':
                    raceepisode = '01'
                elif racesession == 'FP2':
                    raceepisode = '06'
                elif racesession == 'FP3':
                    raceepisode = '11'
        elif c == "Q":
            if sourcefilename[i:i+10] == 'Qualifying':
                racesession = sourcefilename[i:i+10]
                racename = sourcefilename[22:i-1]
                raceinfo = sourcefilename[i+11:-4]
                raceepisode = '03'
            #elif Quali Buildup
            #elif Quali Analysis
        elif c == "R":
            if sourcefilename[i:i+4] == 'Race' or sourcefilename[i:i+4] == 'RACE':
                if sourcefilename[i-5:i-1] == 'Teds':
                    racename = sourcefilename[22:i-6]
                else:
                    racename = sourcefilename[22:i-1]
                racesession = sourcefilename[i:i+4]
                raceinfo = sourcefilename[i+5:-4]
                raceepisode = '13'
        elif c == "S":
            if sourcefilename[i:i+15] == 'Sprint.Shootout':
                racesession = sourcefilename[i:i+15]
                racename = sourcefilename[22:i-1]
                raceinfo = sourcefilename[i+16:-4]
                raceepisode = '07'
            elif sourcefilename[i:i+6] == 'Sprint':
                racesession = sourcefilename[i:i+6]
                racename = sourcefilename[22:i-1]
                raceinfo = sourcefilename[i+7:-4]
                raceepisode = '08'

    if teds is True:
        if racesession == 'Qualifying':
            raceepisode = '05'
            racesession = 'Qualifying Notebook'
        elif racesession == 'Sprint':
            raceepisode = '10'
            racesession = 'Spint Notebook'
        elif racesession == 'Race':
            raceepisode = '15'
            racesession = 'Race Notebook'


    return (racename, raceepisode, racesession, raceinfo)

sourcefilenames = listfiles()

for sourcefilename in sourcefilenames:
    print()
    print("Source filename: " + sourcefilename)

    sourcefilename_clean = sourcefilename.replace('.', ' ')

    # file checks 
    if sourcefilename[-3:] == 'mp4' or sourcefilename[-3:] == 'mkv':
        filetype = sourcefilename[-3:]
        if sourcefilename[0:8] == 'Formula1':
            if sourcefilename[9:11] == '20':
                raceseason = sourcefilename[9:13]
            if sourcefilename[14:19] == 'Round':
                raceround = sourcefilename[19:21]

            racename, raceepisode, racesession, raceinfo = parsefilename(sourcefilename_clean)
            foldername = str(raceseason + "-" + raceround + " - " + racename + " GP")
            finalfilename = str(racename + " - S" + raceround + "E" + raceepisode + " - " + racesession + " [" + raceinfo + "]." + filetype)
            print("Folder Name: " + foldername)
            destfolder = str("mediafiles/" + foldername)
            os.makedirs(destfolder, exist_ok=True)
            print("Parsed filename: " + finalfilename)
            sourcefilepath = str('../sourcefiles/' + sourcefilename)
            finalfilepath = str(destfolder + '/' + finalfilename)
#            try:
#                os.symlink(sourcefilepath, finalfilepath)
#            except FileExistsError as err:
#                print("Symlink exists: " + str(err))


