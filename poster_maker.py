#!/usr/bin/python
# poster_maker.py

import os
import subprocess


def create_background_image(font_name, image_path, destination_folder, race_season, race_round, race_name):
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


def create_poster_image(font_name, track_path, image_path, destination_folder, race_season, race_round, race_name):
    """ generates images with imagemagick"""

    point_size_base = 80

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
    point_size = str(point_size_base-len(race_name)*2)

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


if __name__ == "__main__":
    """ main """
    print("Designed to be run by racefiles.py")

