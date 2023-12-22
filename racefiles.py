# racefiles.py
# sort and rename files into folder structure based on keywords

import os

file_types = ['mkv', 'mp4']
source_files = 'sourcefiles'

sprint_weekends = [('2024', '00')]

sprint_order = ['Free Practice 1',
                'Quali Buildup',
                'Qualifying',
                'Quali Analysis',
                'Quali Notebook',
                'Free Practice 2',
                'Sprint Shootout',
                'Sprint',
                'Sprint Analysis',
                'Sprint Notebook',
                'Free Practice 3',
                'Race Buildup',
                'Race',
                'Race Analysis',
                'Race Notebook',
                'Onboard Channel']

regular_order = ['Free Practice 1',
                 'Free Practice 2',
                 'Free Practice 3',
                 'Quali Buildup',
                 'Qualifying',
                 'Quali Analysis',
                 'Quali Notebook',
                 'Race Buildup',
                 'Race',
                 'Race Analysis',
                 'Race Notebook',
                 'Onboard Channel']


def listfiles(source_files):
    filelist = os.listdir(source_files)
    return filelist


def parsefilename(sourcefilename):
    """ parse source file names for keywords based on test_cars list"""

    test_chars = ['2', 'A', 'T', 'F', 'O', 'Q', 'R', 'S', 'W']
    teds = False
    race_name = sourcefilename

    for i, c in enumerate(sourcefilename):
        # print(sourcefilename[i-6:i-2])
        if c in test_chars:
            if sourcefilename[i:i+3] == 'WEC':
                race_series = 'WEC'
            if sourcefilename[i:i+8] == 'Formula1' or \
               sourcefilename[i:i+9] == 'Formula 1':
                race_series = 'Formula 1'
            if sourcefilename[i:i+4].isnumeric():
                race_season = sourcefilename[i:i+4]
            if sourcefilename[i:i+5] == 'Round':
                race_round = sourcefilename[i+5:i+7]
                race_name_index_start = i+8
            if sourcefilename[i:i+4] == 'Teds':
                teds = True
                teds_race_name = sourcefilename[race_name_index_start:i-1]

            # print(sourcefilename[i:i+7])
            if sourcefilename[i:i+7].lower() == 'onboard':
                race_session = 'Onboard Channel'
                race_name = sourcefilename[race_name_index_start:i-1]
                race_info = sourcefilename[i+16:-4]

            # print(sourcefilename[i:i+2])
            if sourcefilename[i:i+2].lower() == 'fp':
                race_session = str("Free Practice " + sourcefilename[i+2])
                race_name = sourcefilename[race_name_index_start:i-1]
                race_info = sourcefilename[i+4:-4]

            # print(sourcefilename[i:i+10])
            if sourcefilename[i:i+11].lower() == 'qualifying ':
                race_name = sourcefilename[race_name_index_start:i-1]
                if sourcefilename[i:i+19] == 'Qualifying Analysis':
                    race_session = 'Quali Analysis'
                    race_info = sourcefilename[i+20:-4]
                elif sourcefilename[i:i+18] == 'Qualifying Buildup':
                    race_session = 'Quali Buildup'
                    race_info = sourcefilename[i+19:-4]
                else:
                    race_session = 'Qualifying'
                    race_info = sourcefilename[i+11:-4]

            # print(sourcefilename[i:i+6])
            if sourcefilename[i:i+6].lower() == 'quali ':
                race_name = sourcefilename[race_name_index_start:i-1]
                if sourcefilename[i:i+14] == 'Quali Analysis':
                    race_session = 'Quali Analysis'
                    race_info = sourcefilename[i+15:-4]
                elif sourcefilename[i:i+13] == 'Quali Buildup':
                    race_session = 'Quali Buildup'
                    race_info = sourcefilename[i+14:-4]
                else:
                    race_session = 'Qualifying'
                    race_info = sourcefilename[i+6:-4]

            #print(sourcefilename[i-7:i-1])
            if sourcefilename[i:i+5].lower() == 'race ':
                if len(race_name) > len(sourcefilename[race_name_index_start:i-1]):
                    race_name = sourcefilename[race_name_index_start:i-1]
                if sourcefilename[i:i+13] == 'Race Analysis':
                    race_session = 'Race Analysis'
                    race_info = sourcefilename[i+14:-4]
                elif sourcefilename[i:i+12] == 'Race Buildup':
                    race_session = 'Race Buildup'
                    race_info = sourcefilename[i+13:-4]
                else:
                    race_session = 'Race'
                    race_info = sourcefilename[i+5:-4]

            # print(sourcefilename[i:i+6])
            if sourcefilename[i:i+7].lower() == 'sprint ':
                race_name = sourcefilename[race_name_index_start:i-1]
                if sourcefilename[i:i+10] == 'Sprint Sho':
                    race_session = 'Sprint Shootout'
                    race_info = sourcefilename[i+16:-4]
                else:
                    race_session = 'Sprint'
                    race_info = sourcefilename[i+7:-4]

    if teds is True:
        if len(teds_race_name) < len(race_name):
            race_name = teds_race_name
        if race_session[0:5] == 'Quali':
            race_session = 'Quali Notebook'
        if race_session[0:6] == 'Sprint':
            race_session = 'Sprint Notebook'
        if race_session[0:4] == 'Race':
            race_session = 'Race Notebook'

    return (race_series, race_season, race_round, race_name, race_session,
            race_info)




def find_sprint_weekends(sourcefilenames):
    # search for sprint weekends before parsing names
    for sourcefilename in sourcefilenames:
        for i, c in enumerate(sourcefilename):
            if c == '2':
                if sourcefilename[i:i+4].isnumeric():
                    race_season = sourcefilename[i:i+4]
                # print(sourcefilename[i:i+4])
            if c == 'R':
                # print(sourcefilename[i:i+5])
                if sourcefilename[i:i+5] == 'Round':
                    race_round = sourcefilename[i+5:i+7]
                    # print(sourcefilename[i+5:i+7])
            if c == 'S':
                # print(sourcefilename[i:i+6])
                if sourcefilename[i:i+6] == 'Sprint':
                    if (race_season, race_round) not in sprint_weekends:
                        sprint_weekends.append((race_season, race_round))
    return sprint_weekends


def sort_files(sourcefilenames):
    for sourcefilename in sourcefilenames:
        print()
        print("Source filename: " + sourcefilename)

        if sourcefilename[-3:] in file_types:

            sourcefilename_clean = sourcefilename.replace('.', ' ')

            filetype = sourcefilename[-3:]

            race_series, race_season, race_round, race_name, race_session, race_info = parsefilename(sourcefilename_clean)

            if (race_season, race_round) in sprint_weekends:
                weekend_order = str(sprint_order.index(race_session)+1).zfill(2)
            else:
                weekend_order = str(regular_order.index(race_session)+1).zfill(2)

            finalfilename = str(race_name + " GP - S" + race_round + "E" + weekend_order + " - " + race_session + " [" + race_info + "]." + filetype)

            foldername = str(race_season + "-" + race_round + " - " + race_name + " GP")
            destfolder = str("mediafiles/" + race_series + "/" + foldername)

            print(destfolder + "/" + finalfilename)
            os.makedirs(destfolder, exist_ok=True)

            sourcefilepath = str(source_files + "/" + sourcefilename)
            finalfilepath = str(destfolder + '/' + finalfilename)

            try:
                os.link(sourcefilepath, finalfilepath)
            except FileExistsError as err:
                print("file exists: ") #  + str(err))


sourcefilenames = listfiles(source_files)

print(find_sprint_weekends(sourcefilenames))

sort_files(sourcefilenames)






















