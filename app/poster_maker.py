#!/usr/bin/python
# poster_maker.py

import os
import subprocess


def create_background_image(race, font_name, image_path):
    """ generates images with imageconvert"""

    background_destination = str(race.get_destination_folder() + "/background.jpg")

    # if image already exists, dont recreate
    if os.path.isfile(background_destination):
        return

    # prefer race name to race year to default
    background_image = str(image_path + "/" + race.get_race_name() + "-background.jpg")
    if not os.path.isfile(background_image):
        background_image = str(image_path + "/" + race.get_race_season() + "-background.jpg")
    if not os.path.isfile(background_image):
        background_image = str(image_path + "/background.jpg")

    generate_background_cmd = ["convert", background_image,
                               "-resize", "1920x1080!",
                               "-gravity", "NorthEast",
                               "-font", font_name['regular'][0],
                               "-pointsize", "280",
                               "-fill", "none",
                               "-stroke", "white",
                               "-strokewidth", "14",
                               "-annotate", "+160+160", race.get_race_round(),
                               background_destination]

    try:
        subprocess.call(generate_background_cmd)
    except FileExistsError as err:
        print(err)
    else:
        print("Background: " + os.path.basename(race.get_destination_folder()))

    return


def create_poster_image(race, font_name, track_path, image_path):
    """ generates images with imageconvert"""

    point_size_base = 120

    # format title depending on race series
    if race.get_race_series() == "Formula 1":
        full_race_name = f"{race.get_race_series().upper()}\n{race.get_race_name().upper()}\nGRAND PRIX"
    elif race.get_race_series() == "World Endurance Championship":
        full_race_name = f"World\nEndurance\nChampionship\n{race.get_race_name()}"
    else:
        full_race_name = f'{race.get_race_series()}'

    race_poster_destination = str(race.get_destination_folder() + "/show.png")
    track_map_image = str(track_path + "/" + race.get_race_name() + ".png")

    # if image already exists, dont recreate
    if os.path.isfile(race_poster_destination):
        return

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

    # if a map is available, add it to the command
    if os.path.isfile(track_map_image):
        generate_race_poster_cmd.extend(["-blur", "0x4",
                                         track_map_image,
                                         "-compose", "Src_Over",
                                         "-gravity", "Center",
                                         "-background", "None",
                                         "-composite"])

    # add the rest of the imagemagic command
    generate_race_poster_cmd.extend(["-gravity", "NorthWest",
                                     "-font", font_name['black'][0],
                                     "-pointsize", point_size,
                                     "-fill", fill_color,
                                     "-stroke", stroke_color,
                                     "-strokewidth", "4",
                                     "-annotate", "+20+40", full_race_name,
                                     "-font", font_name['black'][0],
                                     "-fill", "red4",
                                     "-stroke", "white",
                                     "-strokewidth", "2",
                                     "-pointsize", "65",
                                     "-gravity", "SouthWest",
                                     "-annotate", "+20+20", race.get_race_season(),
                                     "-gravity", "SouthEast",
                                     "-font", font_name['regular'][0],
                                     "-pointsize", "90",
                                     "-fill", "none",
                                     "-stroke", "white",
                                     "-strokewidth", "4",
                                     "-annotate", "+10+10", race.get_race_round(),
                                     race_poster_destination])

    try:
        subprocess.call(generate_race_poster_cmd)
    except FileExistsError as err:
        print(err)
    else:
        print("Poster: " + os.path.basename(race.get_destination_folder()))

    return


if __name__ == "__main__":
    """ main """
    print("Designed to be run by racefiles.py")

