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

    point_size_base = 120

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

    # get average brightness of poster image
    pb = ["convert", poster_image, "-colorspace", "gray",
          "-resize", "1x1", "-format", "'%[pixel:p{0,0}]'", "info:"]
    poster_brightness = subprocess.run(pb, capture_output=True, text=True)

    # convert result 'grey(xx.xxx)' to int
    poster_brightness_result = poster_brightness.stdout
    brightness = int(poster_brightness_result[6:8])

    # if brightness is greater than value, use a darker text color
    if brightness > 50:
        fill_color = "gray36"
        stroke_color = "white"
    else:
        fill_color = "gray90"
        stroke_color = "black"

    # adjust title size for longer race_name
    point_size = str(point_size_base-len(race_name)*5)

    # start building up the imagemagic command
    generate_race_poster_cmd = ["magick", poster_image,
                                "-resize", "600x900\!"]

    # if a map is available, add it to the command
    if os.path.isfile(track_map_image):
        generate_race_poster_cmd.extend(["-blur", "0x4",
                                         track_map_image,
                                         "-compose", "Src_Over",
                                         "-gravity", "Center",
                                         "-background", "None",
                                         "-composite"])

    # add the rest of the imagemagic command
    generate_race_poster_cmd.extend(["-gravity", "Center",
                                     "-font", font_name['font_black'],
                                     "-pointsize", point_size,
                                     "-fill", fill_color,
                                     "-stroke", stroke_color,
                                     "-strokewidth", "4",
                                     "-annotate", "+0-310", race_name.upper(),
                                     "-font", font_name['font_black'],
                                     "-fill", "red4",
                                     "-stroke", "white",
                                     "-strokewidth", "2",
                                     "-pointsize", "65",
                                     "-gravity", "SouthWest",
                                     "-annotate", "+20+20", race_season,
                                     "-gravity", "SouthEast",
                                     "-font", font_name['font_regular'],
                                     "-pointsize", "90",
                                     "-fill", "none",
                                     "-stroke", "white",
                                     "-strokewidth", "4",
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

