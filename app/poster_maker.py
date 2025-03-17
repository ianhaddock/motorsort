#!/usr/bin/python
# poster_maker.py

import os
import subprocess


if __name__ == "__main__":
    print("Designed to be called by motorsort")


def create_background_image(race, font_name, image_path):
    """ generates images with imageconvert"""

    destination_folder = race.get_destination_folder()
    background_destination = str(race.get_destination_folder() + "/background.jpg")

    # if image already exists, dont recreate
    if os.path.isfile(background_destination):
        return

    # build path if not found
    try:
        os.makedirs(destination_folder, exist_ok=True)
    except OSError as err:
        raise SystemExit("ERROR, can't create path: " + str(err))

    # prefer race name to race year to default
    background_image = str(image_path + "/" + race.get_race_name() + "-background.jpg")
    if not os.path.isfile(background_image):
        background_image = str(image_path + "/" + race.get_race_season() + "-background.jpg")
    if not os.path.isfile(background_image):
        background_image = str(image_path + "/background.jpg")

    generate_background_cmd = ["convert", background_image,
                               "-resize", "1920x1080!",
                               "-gravity", "NorthEast",
                               "-font", font_name['titi-bold'],
                               "-pointsize", "280",
                               "-fill", "none",
                               "-stroke", "white",
                               "-strokewidth", "14",
                               "-annotate", "+160+160", race.get_race_round(),
                               background_destination]

    try:
        subprocess.check_output(generate_background_cmd)
    except subprocess.CalledProcessError as err:
        raise SystemExit('ERROR Imagemagic exit code: ' + str(err.returncode))
    else:
        print("Background: " + os.path.basename(race.get_destination_folder()))

    return 0


def create_poster_image(race, font_name, track_path, flag_path, image_path):
    """ generates images with imageconvert"""

    # format title depending on race series
    if race.get_race_series() == "Formula 1":
        full_race_name = f"{race.get_race_series().upper()}\n{race.get_race_name().upper()}\nGRAND PRIX\n{race.get_race_season()}"
        race_name_font = font_name['black']
        race_name_interline_spacing = "+2"
        race_name_annotate_offset = "+20+40"
        point_size_base = 120
    elif race.get_race_series() == "World Endurance Championship":
        full_race_name = f"World\nEndurance\nChampionship\n{race.get_race_name()}\n{race.get_race_season()}"
        race_name_font = font_name['titi-black']
        race_name_interline_spacing = "-45"
        race_name_annotate_offset = "+20+10"
        point_size_base = 130
    else:
        full_race_name = f'{race.get_race_series()}'
        race_name_font = font_name['titi-black']
        race_name_interline_spacing = "-45"
        race_name_annotate_offset = "+20+10"
        point_size_base = 130

    destination_folder = race.get_destination_folder()
    race_poster_destination = str(race.get_destination_folder() + "/show.png")
    track_map_image = str(track_path + "/" + race.get_race_name() + ".png")
    race_flag = str(flag_path + "/" + race.get_race_name().lower() + ".png")

    # if image already exists, dont recreate
    if os.path.isfile(race_poster_destination):
        return

    # build path if not found
    try:
        os.makedirs(destination_folder, exist_ok=True)
    except OSError as err:
        raise SystemExit("ERROR, can't create path: " + str(err))

    # prefer race name to race year to default
    poster_image = str(image_path + "/" + race.get_race_name() + "-poster.jpg")
    if not os.path.isfile(poster_image):
        poster_image = str(image_path + "/" + race.get_race_season() + "-poster.jpg")
    if not os.path.isfile(poster_image):
        poster_image = str(image_path + "/poster.jpg")

    # use simplified fill colors
    fill_color = "white"
    stroke_color = "black"

    # adjust race_name size if larger than the min, which is
    # the 'championship' part of the WEC title text.
    point_size = str(point_size_base-(max(len(race.get_race_name()), 12)*5))

    # start building up the imagemagic command
    generate_race_poster_cmd = ["convert", poster_image,
                                "-resize", "600x900!"]

    # if a map is available
    if os.path.isfile(track_map_image):
        generate_race_poster_cmd.extend(["-blur", "0x4",
                                         track_map_image,
                                         "-compose", "Src_Over",
                                         "-gravity", "Center",
                                         "-geometry", "+0+80",
                                         "-background", "None",
                                         "-composite"])

    # add country flag if available
    if os.path.isfile(race_flag):
        generate_race_poster_cmd.extend([race_flag,
                                         "-gravity", "SouthWest",
                                         "-geometry", "+20+20",
                                         "-compose", "Src_Over",
                                         "-background", "None",
                                         "-composite"])

    # add the rest of the imagemagic command
    generate_race_poster_cmd.extend(["-gravity", "NorthWest",
                                     "-font", race_name_font,
                                     "-pointsize", point_size,
                                     "-interline-spacing", race_name_interline_spacing,
                                     "-fill", fill_color,
                                     "-stroke", stroke_color,
                                     "-strokewidth", "1",
                                     "-annotate", race_name_annotate_offset, full_race_name,
                                     "-gravity", "SouthEast",
                                     "-font", font_name['titi-bold'],
                                     "-pointsize", "115",
                                     "-fill", "none",
                                     "-stroke", "white",
                                     "-strokewidth", "2",
                                     "-annotate", "+10-20", race.get_race_round(),
                                     race_poster_destination])

    try:
        subprocess.check_output(generate_race_poster_cmd)
    except subprocess.CalledProcessError as err:
        raise SystemExit('ERROR Imagemagic exit code: ' + str(err.returncode))
    else:
        print("Poster: " + os.path.basename(race.get_destination_folder()))

    return 0
