#!/usr/bin/python
# racefiles.py
#
# Organize racing videos into seasons and create custom poster
# images. For use with a personal media server.
# 17 Dec 2023


import os
import re
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
    for sprint_event in weekends:
        sprint_weekends.append((str(datetime.now().year), sprint_event))

    # search files for other sprint weekends
    for source_file_name in source_file_names:
        race_season, race_round = '', ''

        if 'sprint' in source_file_name.lower():

            race_year = re.search("(20|19)[0-9][0-9]", source_file_name)
            if race_year:
                race_season = race_year.group()

            r_round = re.search("Round.?[0-9][0-9]", source_file_name)
            if r_round:
                race_round = r_round.group()[-2:]

            if (race_season, race_round) not in sprint_weekends:
                sprint_weekends.append((race_season, race_round))

    return sprint_weekends


def find_race_year(race: object) -> str:
    """ Search for a four digit year, save to object, return remaining right
    side of string. """
    race_year = re.search("(20|19)[0-9][0-9]", race.get_race_info())
    if race_year:
        race.set_race_season(race_year.group())
    else:
        race.set_race_season('1970')
    race_details = re.split(race.get_race_season(), race.get_race_info(), maxsplit=1)
    race.set_race_info(race_details[-1])
    return


def find_race_round(race: object) -> str:
    """ Search for Round??, save to object, return remaining right side of
    string. """
    race_round = re.search("Round.?[0-9][0-9]", race.get_race_info())
    if race_round:
        race.set_race_round(race_round.group()[-2:])
    else:
        race.set_race_round('00')
    race_details = re.split(race.get_race_round(), race.get_race_info(), maxsplit=1)
    race.set_race_info(race_details[-1])
    return


def find_race_series(race: object, series_prefix: list) -> str:
    """Search for race series prefix, safe to object, return remaining right
    side of string """
    for key in series_prefix.keys():
        if race.get_race_info().startswith(key):
            race_details = re.split(key, race.get_race_info(), maxsplit=1)
            race.set_race_series(series_prefix[key])
            break
    if race.get_race_series() == "Formula 1":
        race_details = re.split("USA", race.get_race_info(), maxsplit=1)
    if race.get_race_series() == "World Endurance Championship":
        race_details = re.split("France", race.get_race_info(), maxsplit=1)
    race.set_race_info(race_details[-1])
    return


def find_race_session(race: object, session_map: list) -> str:
    """ """
    race_name = ""
    race_session = "Unknown"
    race_info = ""
    for key in session_map.keys():
        if key in race.get_race_info().replace('.', ' ').lower():
            if len(race_session) <= len(key):
                race_session = session_map[key]
                race_details = re.split(key, race.get_race_info(), flags=re.IGNORECASE)
                race_name = race_details[0]
                race_info = race_details[-1]
                print(f'>>key>> {session_map[key]} >> {race_name} >> {race_info}')
    race.set_race_name(race_name)
    race.set_race_session(race_session)
    race.set_race_info(race_info)
    return


def find_weekend_order(race: object, sprint_weekends: list, the_weekend_order: list) -> str:
    """ """
    if race.get_race_series() == "Formula 1" and (race.get_race_season(), race.get_race_round()) in sprint_weekends:
        race.set_weekend_order(str(the_weekend_order['sprint_order'].index(race.get_race_session())+1).zfill(2))
    elif race.get_race_series() == "Formula 1":
        race.set_weekend_order(str(the_weekend_order['regular_order'].index(race.get_race_session())+1).zfill(2))
    else:
        race.set_weekend_order(str(the_weekend_order['sportscar_order'].index(race.get_race_session())+1).zfill(2))
    if race.get_weekend_order() == "":
        race.set_weekend_order("Unknown")
    return


def link_files(race, source_file_name: str, copy_files: bool):
    """ """
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
    return


def build_images(race, font_list, track_path, flag_path, image_path):
    """ """
    try:
        os.makedirs(race.get_destination_folder(), exist_ok=True)
    except OSError as err:
        raise SystemExit("ERROR: Can't create path: " + str(err))

    create_poster_image(race,
                        font_list,
                        track_path,
                        flag_path,
                        image_path
                        )
    create_background_image(race,
                            font_list,
                            image_path
                            )
    return


def main():
    """Pull configurations, call functions to parse, build images, and link files."""

    if not which('convert'):
        raise SystemExit("ERROR: Imagemagick convert not found in path.")

    config = ConfigParser()
    config.read(f"{os.getenv('CONFIG_PATH', '/config')}/config.ini")
    try:
        source_path = os.getenv('MEDIA_SOURCE_PATH', config.get('paths', 'source_path'))
    except Exception as err:
        print(f'ERROR: Unable to read config.ini file: {err}')
        exit(1)
    file_prefix = tuple(config.get('config', 'file_prefix').split(','))
    file_types = tuple(config.get('config', 'file_types').split(','))
    spnt_weekends = config.get('config', 'sprint_weekends').split(',')

    with open(config.get('json', 'series_prefix')) as file:
        series_prefix = json.load(file)
    with open(config.get('json', 'weekend_order')) as file:
        the_weekend_order = json.load(file)
    with open(config.get('json', 'session_map')) as file:
        session_map = json.load(file)
    with open(config.get('json', 'fonts')) as file:
        font_list = json.load(file)

    source_file_names = get_file_list(source_path,
                                      file_prefix,
                                      file_types
                                      )
    sprint_weekends = find_sprint_weekends(source_file_names,
                                           spnt_weekends
                                           )

    # main loop
    for source_file_name in get_file_list(source_path,
                                          file_prefix,
                                          file_types
                                          ):
        race = Weekend(os.getenv('MEDIA_DESTINATION_PATH', config.get('paths', 'destination_path')))

        file_name_path, file_extension = os.path.splitext(source_file_name)
        race.set_filetype(file_extension)
        race.set_race_info(os.path.basename(file_name_path))

        find_race_series(race, series_prefix)
        find_race_year(race)
        find_race_round(race)
        find_race_session(race, session_map)
        find_weekend_order(race, sprint_weekends, the_weekend_order)

        if not os.path.exists(race.get_destination_folder()):
            build_images(race,
                         font_list,
                         config.get('paths', 'track_path'),
                         config.get('paths', 'flag_path'),
                         config.get('paths', 'image_path')
                         )

        if not os.path.exists(race.get_destination_full_path()):
            link_files(race,
                       source_file_name,
                       os.getenv('COPY_FILES', config.get('config', 'copy_files')) == 'True'  # str -> bool
                       )

    return 0


if __name__ == "__main__":
    main()
