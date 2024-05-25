#!/usr/bin/python
# racefiles.py
#
# Automatically organize racing videos into seasons and create custom poster
# images. For use with a personal media server.
# 17 Dec 2023


import os
import glob
import json
from shutil import which
import urllib.request
from datetime import datetime
from configparser import ConfigParser
from poster_maker import create_poster_image, create_background_image


def download_missing_fonts(path):
    """ download fonts if missing"""

    os.makedirs(path, exist_ok=True)

    downloaded = False

    for key in font_list.keys():
        font_url = font_list[key][1]
        font = os.path.basename(font_list[key][1])
        if not os.path.isfile(str(path + "/" + font)):
            try:
                urllib.request.urlretrieve(font_url, str(path + "/" + font))
            except OSError as err:
                print("Can't download F1 Font: " + str(err))
                raise SystemExit()
            else:
                downloaded = True
                print("Downloaded " + font_list[key][0])

    if downloaded:
        print("Please install downloaded fonts to proceed.")
        raise SystemExit()

    return


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


def parse_file_name(source_file_name):
    """parse source file names for keywords to build folder structures and
    file names"""

    race_session, race_name, race_info = '', '', ''

    # remove subfolders from path before sorting by filename
    while '/' in source_file_name:
        source_file_name = source_file_name[source_file_name.index('/') + 1:]

    for key in series_prefix.keys():
        if key in source_file_name:
            race_series = series_prefix[key]

    # get Round number
    if 'Round' in source_file_name:
        i = source_file_name.index('Round')
        race_round = source_file_name[i+5:i+8].strip()
        race_name_index_start = source_file_name.index('Round') + len('Round00') + 1

    # get race year
    if '20' in source_file_name:
        i = source_file_name.index('20')
        year = source_file_name[i:i+4]
        if year.isnumeric():
            race_season = year

    # remove USA from race name
    if 'USA' in source_file_name:
        race_name_index_start = source_file_name.index('USA') + len('USA') + 1

    # sort race sessions
    for key in session_map.keys():
        if key in source_file_name.lower():
            if len(race_session) <= len(key):
                race_session = session_map[key]
                race_name = source_file_name[race_name_index_start:source_file_name.lower().index(key) - 1].strip()
                race_info = source_file_name[source_file_name.lower().index(key) + len(key) + 1:-4].strip()

    return (race_series, race_season, race_round, race_name, race_session,
            race_info)


def build_out_files(source_file_names, sprint_weekends):
    """ check if this is a media file, parse filename, sort by keywords into
    folders, link files to destination directory"""

    images_linked = []
    backgrounds_linked = []

    try:
        os.makedirs(destination_path, exist_ok=True)
    except OSError as err:
        print("Can't create " + destination_path + ": " + err)
        raise SystemExit()

    for source_file_name in source_file_names:
        # print()
        # print(source_file_name)
        if source_file_name[-4:] in file_types:

            filetype = source_file_name[-3:]

            race_series, race_season, race_round, race_name, race_session, \
                race_info = parse_file_name(source_file_name.replace('.', ' '))

            if (race_season, race_round) in sprint_weekends:
                weekend_order = str(sprint_order.index(race_session)+1).zfill(2)
            else:
                weekend_order = str(regular_order.index(race_session)+1).zfill(2)

            final_file_name = str(race_name + " GP - S" + race_round + "E" +
                                  weekend_order + " - " + race_session +
                                  " [" + race_info + "]." + filetype)

            destination_folder = str(destination_path + "/" + race_series +
                                     "/" + race_season + "-" + race_round +
                                     " - " + race_name + " GP")
            # print(destination_folder + "/" + final_file_name)

            # reduce duplicate race directories due to differences in race names
            race_round_path = str(destination_path + "/" + race_series +
                                  "/" + race_season + "-" + race_round)
            race_round_path_found = glob.glob(race_round_path + '*')
            if race_round_path_found:
                # print('Found existing race directory: ' + str(race_round_path_found[0]))
                destination_folder = str(race_round_path_found[0])
                final_file_path = str(race_round_path_found[0]) + '/' + final_file_name
            else:
                os.makedirs(destination_folder, exist_ok=True)
                final_file_path = str(destination_folder + '/' + final_file_name)
            # print(final_file_path)

            # only build a background image once for each directory
            if destination_folder not in backgrounds_linked:
                create_background_image(font_list, image_path, destination_folder,
                                        race_season, race_round, race_name)
                backgrounds_linked.append(destination_folder)

            # only build a poster once for each directory
            if destination_folder not in images_linked:
                create_poster_image(font_list, track_path, image_path, destination_folder,
                                    race_season, race_round, race_name)
                images_linked.append(destination_folder)

            try:
                os.link(source_file_name, final_file_path)
            except FileExistsError:
                pass  # print("Skipping: " + final_file_name)
            else:
                print("Linked: " + os.path.basename(final_file_name))


if __name__ == "__main__":
    """ main """

    # dependency check
    if not which('magick'):
        print("imagemagick not found")
        raise SystemExit()

    # read config.ini file
    config = ConfigParser()
    config.read('config.ini')
    destination_path = config.get('config', 'destination_path')
    image_path = config.get('config', 'image_path')
    track_path = config.get('config', 'track_path')
    font_path = config.get('config', 'font_path')
    source_path = config.get('config', 'source_path')
    file_prefix = tuple(config.get('config', 'file_prefix').split(','))
    file_types = tuple(config.get('config', 'file_types').split(','))
    weekends = config.get('config', 'sprint_weekends').split(',')

    # read json files
    with open('series_prefix.json') as file:
        series_prefix = json.load(file)
    with open('weekend_order.json') as file:
        weekend_order = json.load(file)
        sprint_order = weekend_order['sprint_order']
        regular_order = weekend_order['regular_order']
        sportscar_order = weekend_order['sportscar_order']
    with open('session_map.json') as file:
        session_map = json.load(file)
    with open('fonts.json') as file:
        font_list = json.load(file)

    # test
    # for key, value in config.items('config'):
    #     print("Key: " + key + " Value: " + value)

    download_missing_fonts(font_path)

    source_file_names = get_file_list(source_path, file_prefix, file_types)
    print("Found " + str(len(source_file_names)) + " items to process.")

    sprint_weekends = find_sprint_weekends(source_file_names, weekends)
    print("Found " + str(len(sprint_weekends)) + " sprint weekends.")

    print("Creating files.")
    build_out_files(source_file_names, sprint_weekends)
