#!/usr/bin/python
# racefiles.py
#
# Organize racing videos into seasons and create custom poster
# images. For use with a personal media server.
# 17 Dec 2023


import os
import glob
import json
from shutil import which, copy2
import urllib.request
from datetime import datetime
from configparser import ConfigParser
from poster_maker import create_poster_image, create_background_image


class weekend(object):
    """race weekend"""

    def __init__(self):
        self.race_session = ""
        self.race_name = ""
        self.race_info = ""
        self.race_round = "00"
        self.filetype = ""
        self.final_file_name = ""
        self.destination_folder = ""
        self.race_round_path = ""
        self.race_series = ""
        self.race_season = ""
        self.weekend_order = ""

    def set_race_session(self, race_session):
        """ """
        self.race_session = race_session

    def set_gp_suffix(self, gp_suffix):
        """ """
        self.gp_suffix = gp_suffix

    def set_race_name(self, race_name):
        """ """
        self.race_name = race_name

    def get_race_name(self):
        return self.race_name

    def set_race_info(self, race_info):
        """ """
        self.race_info = race_info

    def set_race_round(self, race_round):
        """ """
        self.race_round = race_round

    def get_race_round(self):
        return self.race_round

    def set_filetype(self, filetype):
        """ """
        self.filetype = filetype

    def set_weekend_order(self, weekend_order):
        """ """
        self.weekend_order = weekend_order

    def set_race_series(self, race_series):
        """ """
        self.race_series = race_series

    def get_race_series(self):
        """ """
        return self.race_series

    def set_race_season(self, race_season):
        """ """
        self.race_season = race_season

    def get_race_season(self):
        return self.race_season

    def get_final_file_name(self):
        return str(self.race_name + self.gp_suffix + " - S" + self.race_round + "E" +
                   self.weekend_order + " - " + self.race_session +
                   " [" + self.race_info + "]." + self.filetype)

    def get_destination_folder(self):
        """ use an existing race_season + race_round directory even if race_name differs"""

        self.race_round_path = str(destination_path + "/" + self.race_series +
                                   "/" + self.race_season + "-" + self.race_round)
        self.race_round_path_found = glob.glob(self.race_round_path + '*')

        if self.race_round_path_found:
            self.destination_folder = str(self.race_round_path_found[0])
            # print('Found existing race directory: ' + self.destination_folder)
        else:
            self.destination_folder = str(destination_path + "/" + self.race_series +
                                          "/" + self.race_season + "-" + self.race_round +
                                          " - " + self.race_name + self.gp_suffix)
            # print('Creating destination directory.')

        return self.destination_folder


def get_file_list(source_path, file_prefix, file_types):
    """ return path & name of files matching extensions and prefix lists"""

    file_list = []

    if not os.path.isdir(str(source_path)):
        print("Can't find source path: " + source_path)
        raise SystemExit()

    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(file_types) and file.startswith(file_prefix):
                file_list.append(os.path.join(root, file))

    return sorted(file_list)


def find_sprint_weekends(source_file_names, weekends):
    """ search for sprint weekends before parsing names """

    sprint_weekends = []
    # add sprint weekends from list in config.ini
    for weekend in weekends:
        sprint_weekends.append((datetime.now().year, weekend))

    # search files for other sprint weekends
    for source_file_name in source_file_names:
        race_season, race_round = '', ''

        if 'Sprint' in source_file_name:

            if '20' in source_file_name:
                i = source_file_name.index('20')
                year = source_file_name[i:i+4]
                if year.isnumeric():
                    race_season = year

            if 'Round' in source_file_name:
                i = source_file_name.index('Round')
                race_round = source_file_name[i+5:i+8].strip('.')

            if (race_season, race_round) not in sprint_weekends:
                sprint_weekends.append((race_season, race_round))

    return sprint_weekends


def parse_file_name(race, source_file_name):
    """parse source file names for keywords to build folder structures and
    file names"""

    race.set_filetype(source_file_name[-3:])

    # remove subfolders from path before sorting by filename
    source_file_name = source_file_name[source_file_name.rindex('/') + 1:]

    for key in series_prefix.keys():
        if source_file_name.startswith(key):
            race_series = series_prefix[key]

    # get Round number
    if 'Round' in source_file_name:
        i = source_file_name.index('Round')
        race_round = source_file_name[i+5:i+8].strip()
        race_name_index_start = source_file_name.index('Round') + len('Round00') + 1
    else:
        race_round = "00"

    # get race year
    if '20' in source_file_name:
        i = source_file_name.index('20')
        year = source_file_name[i:i+4]
        if year.isnumeric():
            race_season = year
            race.set_race_season(year)

    # remove USA from race name
    if 'USA' in source_file_name:
        race_name_index_start = source_file_name.index('USA') + len('USA') + 1

    # remove France from race name - test for Le Mans files
    if race.get_race_series() == "World Endurance Championship" and 'France' in source_file_name:
        race_name_index_start = source_file_name.index('France') + len('France') + 1

    # sort race sessions
    race_session = ""
    for key in session_map.keys():
        if key in source_file_name.lower():
            if len(race_session) <= len(key):
                race_session = session_map[key]
                race.set_race_info(source_file_name[source_file_name.lower().index(key) + len(key) + 1:-4].strip())
                # if no race Round was found, use the series name as the race name
                try:
                    race_name_index_start
                except NameError:
                    race.set_race_name(race_series)
                else:
                    race.set_race_name(source_file_name[race_name_index_start:source_file_name.lower().index(key) - 1].strip())

    # set weekend event order
    if race_series == "Formula 1" and (race_season, race_round) in sprint_weekends:
        race.set_weekend_order(str(sprint_order.index(race_session)+1).zfill(2))
    elif race_series == "Formula 1":
        race.set_weekend_order(str(regular_order.index(race_session)+1).zfill(2))
    else:
        race.set_weekend_order(str(sportscar_order.index(race_session)+1).zfill(2))

    # set gp suffix
    if race_series == "Formula 1":
        race.set_gp_suffix(" GP")
    else:
        race.set_gp_suffix("")

    race.set_race_series(race_series)
    race.set_race_round(race_round)
    race.set_race_session(race_session)

    return


if __name__ == "__main__":
    """ main """

    images_linked = []
    backgrounds_linked = []

    font_path = '/usr/local/share/fonts/Formula1'
    image_path = '/custom/images'
    track_path = '/custom/tracks'
    flag_path = '/custom/flags'

    # import enviroment variables
    source_path = os.environ.get('MEDIA_SOURCE_PATH', '/mnt/media/source_files/complete')
    destination_path = os.environ.get('MEDIA_DESTINATION_PATH', '/mnt/media')
    copy_files = (os.environ.get('COPY_FILES', 'False') == 'True')

    # read config.ini file
    config = ConfigParser()
    config.read('/config/config.ini')
    file_prefix = tuple(config.get('config', 'file_prefix').split(','))
    file_types = tuple(config.get('config', 'file_types').split(','))
    weekends = config.get('config', 'sprint_weekends').split(',')

    # read json files
    with open('/config/series_prefix.json') as file:
        series_prefix = json.load(file)
    with open('/config/weekend_order.json') as file:
        the_weekend_order = json.load(file)
        sprint_order = the_weekend_order['sprint_order']
        regular_order = the_weekend_order['regular_order']
        sportscar_order = the_weekend_order['sportscar_order']
    with open('/config/session_map.json') as file:
        session_map = json.load(file)
    with open('/config/fonts.json') as file:
        font_list = json.load(file)

    # checks
    if not which('convert'):
        raise SystemExit("ERROR: Can't find imageconvert")

    # sort source directory for files that fit criteria
    source_file_names = get_file_list(source_path, file_prefix, file_types)
    print("Found " + str(len(source_file_names)) + " items to process.")

    # search found files for events that match F1 sprint weekend order
    sprint_weekends = find_sprint_weekends(source_file_names, weekends)
    print("Found " + str(len(sprint_weekends)) + " sprint weekends.")

    # start buliding
    print("Creating files.")
    for source_file_name in source_file_names:
        # print()
        # print(source_file_name)

        race = weekend()

        parse_file_name(race, source_file_name.replace('.', ' '))

        try:
            os.makedirs(race.get_destination_folder(), exist_ok=True)
        except OSError as err:
            raise SystemExit("ERROR: Can't create path: " + race.get_destination_folder() + "\n" + str(err))

        destination_folder = race.get_destination_folder()
        # only build background once for each directory
        if destination_folder not in backgrounds_linked:
            create_background_image(race, font_list, image_path)
            backgrounds_linked.append(destination_folder)

        # only build poster once for each directory
        if destination_folder not in images_linked:
            create_poster_image(race, font_list, track_path, flag_path, image_path)
            images_linked.append(destination_folder)

        # skip if destination file exists, link file unless copy_files is set
        # true. check first as shutil.copy2 will overwrite an existing file
        #
        destination_full_path = str(race.get_destination_folder() + '/' +
                                    race.get_final_file_name())

        if os.path.exists(destination_full_path):
            # print("File Exists: " + destination_full_path)
            pass
        else:
            if copy_files:
                try:
                    copy2(source_file_name, destination_full_path)
                except OSError as err:
                    raise SystemExit("ERROR: Can't copy file: " + "\n" + str(err))
                else:
                    print("Copied: " + os.path.basename(destination_full_path))
            else:
                try:
                    os.link(source_file_name, destination_full_path)
                except OSError as err:
                    raise SystemExit("ERROR: Can't link file: " + "\n" + str(err))
                else:
                    print("Linked: " + os.path.basename(destination_full_path))
