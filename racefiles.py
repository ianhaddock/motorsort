# racefile renamer

import os

test_chars = ['2', 'T', 'F', 'Q', 'R', 'S', 'W']
file_types = ['mkv', 'mp4']

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
            if sourcefilename[i:i+3] == 'WEC':
                race_series = 'WEC'
            if sourcefilename[i:i+8] == 'Formula1':
                race_series = 'Formula1'
            if sourcefilename[i:i+4].isnumeric():
                raceseason = sourcefilename[i:i+4]
            if sourcefilename[i:i+5] == 'Round':
                raceround = sourcefilename[i+5:i+7]
                race_name_index_start = i+8
            if sourcefilename[i:i+4] == 'Teds':
                teds = True
            if sourcefilename[i:i+2] == 'FP':
                racesession = sourcefilename[i:i+3]
                racename = sourcefilename[race_name_index_start:i-1]
                raceinfo = sourcefilename[i+4:-4]
                if racesession == 'FP1':
                    raceepisode = '01'
                elif racesession == 'FP2':
                    raceepisode = '06'
                elif racesession == 'FP3':
                    raceepisode = '11'
            if sourcefilename[i:i+5] == 'Quali':
                racesession = 'Qualifying' # sourcefilename[i:i+10]
                racename = sourcefilename[race_name_index_start:i-1]
                raceinfo = sourcefilename[i+11:-4]
                raceepisode = '03'
            #elif Quali Buildup
            #elif Quali Analysis
            if sourcefilename[i:i+4] == 'Race' or sourcefilename[i:i+4] == 'RACE':
                if sourcefilename[i-5:i-1] == 'Teds':
                    racename = sourcefilename[race_name_index_start:i-6]
                    racesession = 'Teds Notebook'
                    raceepisode = '15'
                elif sourcefilename[i-7:i-1] == 'Sprint':
                    racename = sourcefilename[race_name_index_start:i-8]
                    racesession = sourcefilename[i-7:i-1]
                    raceepisode = '08'
                else:
                    racename = sourcefilename[race_name_index_start:i-1]
                    racesession = sourcefilename[i:i+4]
                    raceepisode = '13'
                raceinfo = sourcefilename[i+5:-4]
            if sourcefilename[i:i+6] == 'Sprint':
            #    print(sourcefilename[i:i+6])
            #    print(sourcefilename[i+7:i+10])
                if sourcefilename[i+7:i+10] == 'Sky':
                    racesession = sourcefilename[i:i+6]
                    racename = sourcefilename[race_name_index_start:i-1]
                    raceinfo = sourcefilename[i+7:-4]
                    raceepisode = '08'
                if sourcefilename[i+7:i+10] == 'Sho':
                    racesession = 'Sprint Shootout' #sourcefilename[i:i+15]
                    racename = sourcefilename[race_name_index_start:i-1]
                    raceinfo = sourcefilename[i+16:-4]
                    raceepisode = '07'

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

    return (race_series, raceseason, raceround, racename, raceepisode, racesession, raceinfo)


sourcefilenames = listfiles()

for sourcefilename in sourcefilenames:
    print()
    print("Source filename: " + sourcefilename)

    sourcefilename_clean = sourcefilename.replace('.', ' ')

    if sourcefilename[-3:] in file_types:
        filetype = sourcefilename[-3:]

        race_series, raceseason, raceround, racename, raceepisode, racesession, raceinfo = parsefilename(sourcefilename_clean)

        foldername = str(raceseason + "-" + raceround + " - " + racename + " GP")

        finalfilename = str(racename + " GP - S" + raceround + "E" + raceepisode + " - " + racesession + " [" + raceinfo + "]." + filetype)

        destfolder = str("mediafiles/" + race_series + "/" + foldername)

        print(destfolder + "/" + finalfilename)
        os.makedirs(destfolder, exist_ok=True)


        sourcefilepath = str('../sourcefiles/' + sourcefilename)
        finalfilepath = str(destfolder + '/' + finalfilename)

        try:
            os.symlink(sourcefilepath, finalfilepath)
        except FileExistsError as err:
            print("Symlink exists: ") #  + str(err))


