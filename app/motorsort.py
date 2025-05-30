#!/usr/bin/source python
"""Organize racing videos into seasons and create custom poster
images. For use with a PLEX personal media server. 17 Dec 2023"""

import os
import re
import json
from shutil import which, copy2
from datetime import datetime
from configparser import ConfigParser
from poster_maker import create_poster_image, create_background_image
from weekend import Weekend


def get_file_list(source_path, file_prefix, file_types) -> list:
    """return path & name of files matching extensions and prefix lists"""

    if not os.path.isdir(str(source_path)):
        raise SystemExit("ERROR, can't find source path: " + source_path)

    file_list = []
    for root, _, files in os.walk(source_path):
        for file in files:
            if file.endswith(file_types) and file.startswith(file_prefix):
                file_list.append(os.path.join(root, file))

    return sorted(file_list)


def find_sprint_weekends(source_file_names, weekends):
    """search for sprint weekends before parsing names"""

    sprint_weekends = []
    # add sprint weekends from list in config.ini
    for sprint_event in weekends:
        sprint_weekends.append((str(datetime.now().year), sprint_event))

    # search files for other sprint weekends
    for source_file_name in source_file_names:
        race_season, race_round = "", ""

        if "sprint" in source_file_name.lower():

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
    """Search for a four digit year, save to object, return remaining right
    side of string."""
    filename = race.get_kv("race_info")
    race_year = re.search("(20|19)[0-9][0-9]", filename)
    if race_year:
        race.set_kv("race_season", race_year.group())
        race.set_kv("race_info", filename.replace(race_year.group(), "", 1))
    else:
        race.set_kv("race_season", "1970")


def find_race_round(race: object) -> str:
    """Search for Round??, save to object, return remaining right side of
    string."""
    filename = race.get_kv("race_info")
    race_round = re.search("Round.?[0-9][0-9]", filename)
    if race_round:
        race.set_kv("race_round", race_round.group()[-2:])
        race.set_kv("race_info", filename.replace(race_round.group(), "", 1))
    else:
        race.set_kv("race_round", "00")


def find_race_series(race: object, series_prefix: list) -> str:
    """Search for race series prefix, safe to object, return remaining right
    side of string"""
    filename = race.get_kv("race_info")
    for key in series_prefix.keys():
        if filename.startswith(key):
            race.set_kv("race_series", series_prefix[key])
            race.set_kv("race_info", filename.replace(key, "", 1))
            break


def find_race_session(race: object, session_map: list) -> str:
    """find race session from dict, sort filename by name, info, and details"""
    race_name = ""
    race_session = ""
    race_info = ""
    for key in session_map.keys():
        if key in race.get_kv("race_info").replace(".", " ").lower():
            if len(race_session) <= len(key):
                race_session = session_map[key]
                race_details = re.split(
                    key,
                    race.get_kv("race_info").replace(".", " ").lower(),
                    flags=re.IGNORECASE,
                )
                race_name = race_details[0].title()
                race_info = race_details[-1].upper()
                # print(
                #     f">>key>> {session_map[key]} >race_name> {race_name} >race_info> {race_info}"
                # )
    race.set_kv("race_name", race_name)
    race.set_kv("race_session", race_session)
    race.set_kv("race_info", race_info)


def find_weekend_order(race: object, sprint_weekends: list, the_weekend_order: list):
    """sort race session by race series order"""

    sort_order = the_weekend_order["sportscar_order"]

    if race.get_kv("race_series") == "Formula 1":
        if (race.get_kv("race_season"), race.get_kv("race_round")) in sprint_weekends:
            sort_order = the_weekend_order["sprint_order"]
        else:
            sort_order = the_weekend_order["regular_order"]
    try:
        wknd_order = sort_order.index(race.get_kv("race_session"))
    except ValueError as err:
        raise ValueError("not found in weekend order") from err

    race.set_kv("weekend_order", str(wknd_order + 1).zfill(2))


def link_files(race, source_file_name: str, copy_files: bool):
    """hardlink or copy files to final destination"""
    if copy_files:
        try:
            copy2(source_file_name, race.get_destination_full_path())
        except OSError as err:
            raise SystemExit("ERROR: Can't copy file: ") from err
        print("Copied: " + race.get_final_file_name())
    else:
        try:
            os.link(source_file_name, race.get_destination_full_path())
        except OSError as err:
            raise SystemExit("ERROR: Can't link file: ") from err
        print("Linked: " + race.get_final_file_name())


def build_images(race, font_list, track_path, flag_path, image_path):
    """generate folder images"""
    try:
        os.makedirs(race.get_destination_folder(), exist_ok=True)
    except OSError as err:
        raise SystemExit("ERROR: Can't create path: ") from err

    create_poster_image(race, font_list, track_path, flag_path, image_path)
    create_background_image(race, font_list, image_path)


def main():
    # disable too many local variables - pylint: disable=R0914
    """Pull configurations, call functions to parse, build images,
    and link files."""

    if not which("convert"):
        raise SystemExit("ERROR: Imagemagick convert not found in path.")

    config = ConfigParser()
    config.read(f"{os.getenv('CONFIG_PATH', '/config')}/config.ini")
    try:
        source_path = os.getenv("MEDIA_SOURCE_PATH", config.get("paths", "source_path"))
    except OSError as err:
        raise SystemExit("ERROR: Unable to read config.ini file: ") from err

    file_prefix = tuple(config.get("config", "file_prefix").split(","))
    file_types = tuple(config.get("config", "file_types").split(","))
    spnt_weekends = config.get("config", "sprint_weekends").split(",")

    with open(config.get("json", "series_prefix"), "r", encoding="utf-8") as file:
        series_prefix = json.load(file)
    with open(config.get("json", "weekend_order"), "r", encoding="utf-8") as file:
        the_weekend_order = json.load(file)
    with open(config.get("json", "session_map"), "r", encoding="utf-8") as file:
        session_map = json.load(file)
    with open(config.get("json", "fonts"), "r", encoding="utf-8") as file:
        font_list = json.load(file)

    source_file_names = get_file_list(source_path, file_prefix, file_types)
    sprint_weekends = find_sprint_weekends(source_file_names, spnt_weekends)

    # main loop
    for source_file_name in source_file_names:
        # print(f"> Source file name: {source_file_name}")
        race = Weekend(
            os.getenv("MEDIA_DESTINATION_PATH", config.get("paths", "destination_path"))
        )

        file_name_path, file_extension = os.path.splitext(source_file_name)
        race.set_kv("file_extension", file_extension)
        race.set_kv("race_info", os.path.basename(file_name_path))

        # print(source_file_name)

        find_race_year(race)
        find_race_series(race, series_prefix)
        find_race_round(race)
        find_race_session(race, session_map)

        try:
            find_weekend_order(race, sprint_weekends, the_weekend_order)
        except ValueError:
            print(f"ERROR: Can't parse file, skipping: {source_file_name}")
            continue

        filename = race.get_kv("race_name")
        # print(f">>>> filename: {filename}")
        if race.get_kv("race_series") == "Formula 1":
            race.set_kv("race_name", filename.replace("Usa", "", 1))
        if race.get_kv("race_series") == "World Endurance Championship":
            race.set_kv("race_name", filename.replace("France", "", 1))

        if not os.path.exists(race.get_destination_folder()):
            build_images(
                race,
                font_list,
                config.get("paths", "track_path"),
                config.get("paths", "flag_path"),
                config.get("paths", "image_path"),
            )

        if not os.path.exists(race.get_destination_full_path()):
            link_files(
                race,
                source_file_name,
                os.getenv("COPY_FILES", config.get("config", "copy_files"))
                == "True",  # str -> bool
            )

    return 0


if __name__ == "__main__":
    main()
