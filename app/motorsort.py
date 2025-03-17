#!/usr/bin/python
# racefiles.py
#
# Organize racing videos into seasons and create custom poster
# images. For use with a personal media server.
# 17 Dec 2023


import os
import json
from shutil import which, copy2
from datetime import datetime
from configparser import ConfigParser
from poster_maker import create_poster_image, create_background_image
from weekend import Weekend


def get_file_list(source_path, file_prefix, file_types) -> list:
    """ return path & name of files matching extensions and prefix lists"""

    file_list = []

    if not os.path.isdir(str(source_path)):
        raise SystemExit("ERROR, can't find source path: " + source_path)

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
        sprint_weekends.append((str(datetime.now().year), weekend))

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


def parse_file_name(race, series_prefix, session_map, sprint_weekends, the_weekend_order, source_file_name):
    """parse source file names for keywords to build folder structures and
    file names"""

    # sanitize filename
    source_file_name = source_file_name.replace('.', ' ')

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

    # remove USA from Formula 1 race name
    if race_series == "Formula 1" and 'USA' in source_file_name:
        race_name_index_start = source_file_name.index('USA') + len('USA') + 1

    # remove France from WEC race names - test for Le Mans files
    if race_series == "World Endurance Championship" and 'France' in source_file_name:
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
        race.set_weekend_order(str(the_weekend_order['sprint_order'].index(race_session)+1).zfill(2))
    elif race_series == "Formula 1":
        race.set_weekend_order(str(the_weekend_order['regular_order'].index(race_session)+1).zfill(2))
    else:
        race.set_weekend_order(str(the_weekend_order['sportscar_order'].index(race_session)+1).zfill(2))

    # set gp suffix
    race.set_gp_suffix("")
    if race_series == "Formula 1":
        race.set_gp_suffix(" GP")

    race.set_race_series(race_series)
    race.set_race_round(race_round)
    race.set_race_session(race_session)

    return


def main():
    """ main """

    if not which('convert'):
        raise SystemExit("ERROR: Imagemagick convert not found in path.")

    config = ConfigParser()
    config.read(f"{os.getenv('CONFIG_PATH', '/config')}/config.ini")
    try:
        file_prefix = tuple(config.get('config', 'file_prefix').split(','))
    except Exception as err:
        print(f'ERROR: Unable to read config.ini file: {err}')
        exit(1)
    file_types = tuple(config.get('config', 'file_types').split(','))
    weekends = config.get('config', 'sprint_weekends').split(',')
    source_path = os.getenv('MEDIA_SOURCE_PATH', config.get('config', 'source_path'))
    destination_path = os.getenv('MEDIA_DESTINATION_PATH', config.get('config', 'destination_path'))
    copy_files = (os.getenv('COPY_FILES', config.get('config', 'copy_files')) == 'True')  # str -> bool

    with open(f"{os.getenv('CONFIG_PATH', '/config')}/series_prefix.json") as file:
        series_prefix = json.load(file)
    with open(f"{os.getenv('CONFIG_PATH', '/config')}/weekend_order.json") as file:
        the_weekend_order = json.load(file)
    with open(f"{os.getenv('CONFIG_PATH', '/config')}/session_map.json") as file:
        session_map = json.load(file)
    with open(f"{os.getenv('CONFIG_PATH', '/config')}/fonts.json") as file:
        font_list = json.load(file)

    source_file_names = get_file_list(source_path, file_prefix, file_types)
    sprint_weekends = find_sprint_weekends(source_file_names, weekends)

    for source_file_name in source_file_names:
        race = Weekend(destination_path)

        parse_file_name(race,
                        series_prefix,
                        session_map,
                        sprint_weekends,
                        the_weekend_order,
                        source_file_name
                        )

        try:
            os.makedirs(race.get_destination_folder(), exist_ok=True)
        except OSError as err:
            raise SystemExit("ERROR: Can't create path: " + str(err))

        if race.get_destination_folder() not in race.get_directory_images_created():
            create_poster_image(race,
                                font_list,
                                config.get('config', 'track_path'),
                                config.get('config', 'flag_path'),
                                config.get('config', 'image_path')
                                )
            create_background_image(race,
                                    font_list,
                                    config.get('config', 'image_path')
                                    )
            race.set_directory_images_created(race.get_destination_folder())

        if not os.path.exists(race.get_destination_full_path()):
            if copy_files:
                try:
                    copy2(source_file_name, race.get_destination_full_path())
                except OSError as err:
                    raise SystemExit("ERROR: Can't copy file: " + str(err))
                else:
                    print("Copied: " + race.get_final_file_name())
            else:
                try:
                    os.link(source_file_name, race.get_destination_full_path())
                except OSError as err:
                    raise SystemExit("ERROR: Can't link file: " + str(err))
                else:
                    print("Linked: " + race.get_final_file_name())

    return 0


if __name__ == "__main__":
    main()
