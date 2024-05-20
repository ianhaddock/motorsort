#!/usr/bin/python
# racefiles.py
#
# Automatically organize racing videos into seasons and create custom poster
# images. For use with a personal media server.
# 17 Dec 2023


import os
import glob
import subprocess
from shutil import which
import urllib.request
from configparser import ConfigParser


file_types = ('.mkv', '.mp4')

file_prefix = ('Formula1', 'Formula.1', 'WEC')

series_prefix = [('Formula1', 'Formula 1'),
                 ('Formula 1', 'Formula 1'),
                 ('WEC', 'WEC')]

fonts = ['font_regular',
         'font_bold',
         'font_wide',
         'font_black']

sprint_weekends = []

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

session_map = [('fp1', 'Free Practice 1'),
               ('fp2', 'Free Practice 2'),
               ('fp3', 'Free Practice 3'),
               ('qualifying', 'Qualifying'),
               ('pre quali', 'Quali Buildup'),
               ('pre qualifying', 'Quali Buildup'),
               ('qualifying buildup', 'Quali Buildup'),
               ('qualifying build-up', 'Quali Buildup'),
               ('quali', 'Qualifying'),
               ('post quali', 'Quali Analysis'),
               ('post qualifying', 'Quali Analysis'),
               ('quali analysis', 'Quali Analysis'),
               ('quali buildup', 'Quali Buildup'),
               ('qualifying analysis', 'Quali Analysis'),
               ('sprint', 'Sprint'),
               ('sprint shootout', 'Sprint Shootout'),
               ('sprint quali', 'Sprint Shootout'),
               ('sprint race', 'Sprint'),
               ('pre race', 'Race Buildup'),
               ('race buildup', 'Race Buildup'),
               ('race build-up', 'Race Buildup'),
               ('race', 'Race'),
               ('post race', 'Race Analysis'),
               ('race analysis', 'Race Analysis'),
               ('race notebook', 'Race Notebook'),
               ('quali notebook', 'Quali Notebook'),
               ('teds notebook', 'Race Notebook'),
               ('teds quali notebook', 'Quali Notebook'),
               ('qualifying notebook', 'Quali Notebook'),
               ('teds qualifying notebook', 'Quali Notebook'),
               ('qualifying teds notebook', 'Quali Notebook'),
               ('teds race notebook', 'Race Notebook'),
               ('teds sprint notebook', 'Sprint Notebook'),
               ('race teds notebook', 'Race Notebook'),
               ('onboard channel', 'Onboard Channel'),
               ('race onboard channel', 'Onboard Channel'),
               ('onboard', 'Onboard Channel')]


def get_config(item, config_file='config.ini'):
    """get settings in config file"""
    config = ConfigParser()
    config.read(config_file)

    return config.get('config', str(item))


def get_fonts(fonts, path):
    """ download fonts if missing"""

    downloaded = False
    fonts_list = []
    font_name = {}

    for font in fonts:
        fonts_list.append((get_config(font).split(',')))
        font_name[font] = fonts_list[-1][0]

    os.makedirs(path, exist_ok=True)
    for name, url_path in fonts_list:
        font = os.path.basename(url_path)
        if not os.path.isfile(str(font_path + "/" + font)):
            try:
                urllib.request.urlretrieve(url_path, str(path + "/" + font))
            except OSError as err:
                print("Can't download F1 Font: " + str(err))
                raise SystemExit()
            else:
                downloaded = True
                print("Downloaded " + name)

    if downloaded:
        print("Please install downloaded fonts to proceed.")
        raise SystemExit()

    return font_name


def list_files(source_path):
    file_list = []
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(file_types) and \
               file.startswith(file_prefix):
                file_list.append(os.path.join(root, file))

    return sorted(file_list)


def find_sprint_weekends(source_file_names, sprint_weekends):
    """ search for sprint weekends before parsing names """
    for source_file_name in source_file_names:
        for i, c in enumerate(source_file_name):
            if c == '2':
                if source_file_name[i:i+4].isnumeric():
                    race_season = source_file_name[i:i+4]
                # print(source_file_name[i:i+4])
            if c == 'R':
                # print(source_file_name[i:i+5])
                if source_file_name[i:i+5] == 'Round':
                    race_round = source_file_name[i+5:i+7]
                    # print(source_file_name[i+5:i+7])
            if c == 'S':
                # print(source_file_name[i:i+6])
                if source_file_name[i:i+6] == 'Sprint':
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

    # cleanup race series naming
    for prefix, name in series_prefix:
        if prefix in source_file_name:
            race_series = name

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
    for key, value in session_map:
        if key in source_file_name.lower():
            if len(race_session) <= len(key):
                race_session = value
                race_name = source_file_name[race_name_index_start:source_file_name.lower().index(key) - 1].strip()
                race_info = source_file_name[source_file_name.lower().index(key) + len(key) + 1:-4].strip()

    return (race_series, race_season, race_round, race_name, race_session,
            race_info)


def create_background_image(image_path, destination_folder, race_season, race_round, race_name):
    """ generates images with imagemagick"""

    background_destination = str(destination_folder + "/background.jpg")

    # if image already exists, dont recreate
    if os.path.isfile(background_destination):
        return

    # prefer race name to race year to default
    background_image = str(image_path + "/" + race_name + "-background.jpg")
    if not os.path.isfile(background_image):
        background_image = str(image_path + "/" + race_season + "-background.jpg")
    if not os.path.isfile(background_image):
        background_image = str(image_path + "/background.jpg")

    generate_background_cmd = ["magick", background_image,
                               "-resize", "1920x1080\!",
                               "-gravity", "NorthEast",
                               "-font", font_name['font_regular'],
                               "-pointsize", "280",
                               "-fill", "none",
                               "-stroke", "white",
                               "-strokewidth", "14",
                               "-annotate", "+160+160", race_round,
                               background_destination]

    try:
        subprocess.call(generate_background_cmd)
    except FileExistsError as err:
        print(err)
    else:
        print("Background: " + os.path.basename(destination_folder))

    return


def create_poster_image(image_path, destination_folder, race_season, race_round, race_name):
    """ generates images with imagemagick"""

    race_poster_destination = str(destination_folder + "/show.png")
    track_map_image = str(track_path + "/" + race_name + ".png")

    # if image already exists, dont recreate
    if os.path.isfile(race_poster_destination):
        return

    # prefer race name to race year to default
    poster_image = str(image_path + "/" + race_name + "-poster.jpg")
    if not os.path.isfile(poster_image):
        poster_image = str(image_path + "/" + race_season + "-poster.jpg")
    if not os.path.isfile(poster_image):
        poster_image = str(image_path + "/poster.jpg")

    # adjust title size for longer race_name
    point_size = str(100-len(race_name)*2)

    # start building up the imagemagic command
    generate_race_poster_cmd = ["magick", poster_image,
                                "-resize", "600x900\!"]

    # if a map is available, add it to the command
    if os.path.isfile(track_map_image):
        generate_race_poster_cmd.extend(["-blur", "0x2",
                                         track_map_image,
                                         "-compose", "Src_Over",
                                         "-gravity", "Center",
                                         "-background", "None",
                                         "-composite"])

    # add the rest of the imagemagic command
    generate_race_poster_cmd.extend(["-gravity", "Center",
                                     "-font", font_name['font_bold'],
                                     "-pointsize", point_size,
                                     "-fill", "red2",
                                     "-stroke", "red4",
                                     "-strokewidth", "4",
                                     "-annotate", "+0-310", race_name,
                                     "-font", font_name['font_black'],
                                     "-fill", "red4",
                                     "-stroke", "white",
                                     "-strokewidth", "2",
                                     "-pointsize", "65",
                                     "-gravity", "SouthWest",
                                     "-annotate", "+20+20", race_season,
                                     "-gravity", "SouthEast",
                                     "-font", font_name['font_regular'],
                                     "-pointsize", "120",
                                     "-fill", "none",
                                     "-stroke", "white",
                                     "-strokewidth", "8",
                                     "-annotate", "+10+10", race_round,
                                     race_poster_destination])

    try:
        subprocess.call(generate_race_poster_cmd)
    except FileExistsError as err:
        print(err)
    else:
        print("Poster: " + os.path.basename(destination_folder))

    return


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
                create_background_image(image_path, destination_folder,
                                        race_season, race_round, race_name)
                backgrounds_linked.append(destination_folder)

            # only build a poster once for each directory
            if destination_folder not in images_linked:
                create_poster_image(image_path, destination_folder,
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

    # config, paths
    source_path = get_config('source_path')
    destination_path = get_config('destination_path')
    font_path = get_config('font_path')
    image_path = get_config('image_path')
    track_path = get_config('track_path')

    # config, build sprint weekends list from string
    weekends = get_config('sprint_weekends').split(',')
    for weekend in weekends:
        sprint_weekends.append(('2024', weekend))

    # sanity checks
    if not os.path.isdir(str(source_path)):
        print("Can't find source path: " + source_path)
        raise SystemExit()

    if not which('magick'):
        print("imagemagick not found")
        raise SystemExit()

    font_name = get_fonts(fonts, font_path)

    source_file_names = list_files(source_path)
    print("Found " + str(len(source_file_names)) + " items to process.")

    sprint_weekends = find_sprint_weekends(source_file_names, sprint_weekends)
    print("Found " + str(len(sprint_weekends)) + " sprint weekends.")

    print("Creating files.")
    build_out_files(source_file_names, sprint_weekends)

