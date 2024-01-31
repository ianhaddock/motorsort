# racefiles.py
# sort and rename files into folder structure based on keywords

# f1 track svg files
# https://github.com/f1laps/f1-track-vectors

# testing on devbox
# wget https://imagemagick.org/archive/binaries/magick
# mv magick to /usr/local/sbin/
# chmod 777 /usr/local/sbin/magick
# sudo ln -s /home/ansible/fonts /usr/share/fonts/formula1

import os
import subprocess
from shutil import which
import urllib.request

source_path = 'sourcefiles'
destination_path = 'mediafiles'

file_types = ('.mkv', '.mp4')
file_prefix = ('Formula1', 'Formula.1')

font_path = 'fonts'
font_list = [('https://www.formula1.com/etc/designs/fom-website/fonts/\
F1Regular/Formula1-Regular.ttf', 'Formula1-Regular.ttf'),
             ('https://www.formula1.com/etc/designs/fom-website/fonts/\
F1Bold/Formula1-Bold.ttf', 'Formula1-Bold.ttf'),
             ('https://www.formula1.com/etc/designs/fom-website/fonts/\
F1Wide/Formula1-Wide.ttf', 'Formula1-Wide.ttf'),
             ('https://www.formula1.com/etc/designs/fom-website/fonts/\
F1Black/Formula1-Black.ttf', 'Formula1-Black.ttf')]

image_path = 'images'
track_path = 'track_png'

sprint_weekends = [('2024', '00')]

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


def list_files(source_path):
    file_list = []
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.endswith(file_types) and \
               file.startswith(file_prefix):
                file_list.append(os.path.join(root, file))
    return file_list


def parse_file_name(source_file_name):
    """ parse source file names for keywords based on test_chars list"""

    test_chars = ['2', 'A', 'T', 'F', 'N', 'O', 'P', 'Q', 'R', 'S', 'W']
    teds = False
    race_name = source_file_name
    teds_race_name = source_file_name

    for i, c in enumerate(source_file_name):
        # print(source_file_name[i-6:i-2])
        if c in test_chars:
            if source_file_name[i:i+3] == 'WEC':
                race_series = 'WEC'
            if source_file_name[i:i+8] == 'Formula1' or \
               source_file_name[i:i+9] == 'Formula 1':
                race_series = 'Formula 1'
            if source_file_name[i:i+4].isnumeric():
                race_season = source_file_name[i:i+4]
            if source_file_name[i:i+5] == 'Round':
                if source_file_name[i+5:i+7].isnumeric():
                    race_round = source_file_name[i+5:i+7]
                    if source_file_name[i+8:i+11] == 'USA':
                        race_name_index_start = i+12
                    else: 
                        race_name_index_start = i+8
                else:
                    race_round = source_file_name[i+6:i+8]
                    if source_file_name[i+9:i+12] == 'USA':
                        race_name_index_start = i+13
                    else: 
                        race_name_index_start = i+9
            if source_file_name[i:i+8] == 'Notebook':
                teds = True
                if len(teds_race_name) > len(source_file_name[race_name_index_start:i-1]):
                    teds_race_name = source_file_name[race_name_index_start:i-1]
            if source_file_name[i:i+4] == 'Teds':
                teds = True
                teds_race_name = source_file_name[race_name_index_start:i-1]
            if source_file_name[i:i+3] == 'Pre':
                race_name = source_file_name[race_name_index_start:i-1]
            if source_file_name[i:i+4] == 'Post':
                race_name = source_file_name[race_name_index_start:i-1]

            # print(source_file_name[i:i+7])
            if source_file_name[i:i+7].lower() == 'onboard':
                race_session = 'Onboard Channel'
                if source_file_name[i-5:i-1].lower() == 'race':
                    race_name = source_file_name[race_name_index_start:i-6]
                else:
                    race_name = source_file_name[race_name_index_start:i-1]
                race_info = source_file_name[i+16:-4]

            # print(source_file_name[i:i+2])
            if source_file_name[i:i+2].lower() == 'fp':
                race_session = str("Free Practice " + source_file_name[i+2])
                race_name = source_file_name[race_name_index_start:i-1]
                race_info = source_file_name[i+4:-4]

            # print(source_file_name[i:i+10])
            if source_file_name[i:i+11].lower() == 'qualifying ':
                if len(race_name) > len(source_file_name[race_name_index_start:i-1]):
                    race_name = source_file_name[race_name_index_start:i-1]
                if source_file_name[i:i+19] == 'Qualifying Analysis':
                    race_session = 'Quali Analysis'
                    race_info = source_file_name[i+20:-4]
                elif source_file_name[i:i+18] == 'Qualifying Buildup':
                    race_session = 'Quali Buildup'
                    race_info = source_file_name[i+19:-4]
                elif source_file_name[i-5:i+5] == 'Post Quali':
                    race_session = 'Quali Analysis'
                    race_info = source_file_name[i+6:-4]
                elif source_file_name[i-4:i+5] == 'Pre Quali':
                    race_session = 'Quali Buildup'
                    race_info = source_file_name[i+6:-4]
                else:
                    race_session = 'Qualifying'
                    race_info = source_file_name[i+11:-4]

            # print(source_file_name[i:i+6])
            if source_file_name[i:i+6].lower() == 'quali ':
                if len(race_name) > len(source_file_name[race_name_index_start:i-1]):
                    race_name = source_file_name[race_name_index_start:i-1]
                if source_file_name[i:i+14] == 'Quali Analysis':
                    race_session = 'Quali Analysis'
                    race_info = source_file_name[i+15:-4]
                elif source_file_name[i:i+13] == 'Quali Buildup':
                    race_session = 'Quali Buildup'
                    race_info = source_file_name[i+14:-4]
                elif source_file_name[i-5:i+5] == 'Post Quali':
                    race_session = 'Quali Analysis'
                    race_info = source_file_name[i+6:-4]
                elif source_file_name[i-4:i+5] == 'Pre Quali':
                    race_session = 'Quali Buildup'
                    race_info = source_file_name[i+6:-4]
                else:
                    race_session = 'Qualifying'
                    race_info = source_file_name[i+6:-4]

            # print(source_file_name[i-7:i-1])
            if source_file_name[i:i+5].lower() == 'race ':
                if len(race_name) > len(source_file_name[race_name_index_start:i-1]):
                    race_name = source_file_name[race_name_index_start:i-1]
                if source_file_name[i:i+13] == 'Race Analysis':
                    race_session = 'Race Analysis'
                    race_info = source_file_name[i+14:-4]
                elif source_file_name[i:i+12] == 'Race Buildup':
                    race_session = 'Race Buildup'
                    race_info = source_file_name[i+13:-4]
                elif source_file_name[i-5:i+4] == 'Post Race':
                    race_session = 'Race Analysis'
                    race_info = source_file_name[i+5:-4]
                elif source_file_name[i-4:i+4] == 'Pre Race':
                    race_session = 'Race Buildup'
                    race_info = source_file_name[i+5:-4]
                elif not source_file_name[i-7:i+4] == 'Sprint Race':
                    race_session = 'Race'
                    race_info = source_file_name[i+5:-4]

            # print(source_file_name[i:i+6])
            if source_file_name[i:i+7].lower() == 'sprint ':
                race_name = source_file_name[race_name_index_start:i-1]
                if source_file_name[i:i+10] == 'Sprint Sho':
                    race_session = 'Sprint Shootout'
                    race_info = source_file_name[i+16:-4]
                else:
                    race_session = 'Sprint'
                    race_info = source_file_name[i+7:-4]

    if teds is True:
        if len(teds_race_name) < len(race_name):
            race_name = teds_race_name
        if race_session[0:5] == 'Quali':
            race_session = 'Quali Notebook'
        if race_session[0:6] == 'Sprint':
            race_session = 'Sprint Notebook'
        if race_session[0:4] == 'Race':
            race_session = 'Race Notebook'

    return (race_series, race_season, race_round, race_name, race_session,
            race_info)


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


def create_background_image(f1_fonts, image_path, destination_folder, race_season, race_round, race_name):
    """ generates images with imagemagick"""

# $ magick composite  -background none -gravity NorthEast -compose atop -geometry 960x960+160+160 ../track_svgs/usa.svg COTA-background.jpg track-output-poster.png
# $ magick COTA-background.jpg ../track_svgs/usa.png -compose Src_Over -background None -gravity East -geometry 960x960+160+160 -composite -gravity NorthEast -font Formula1-Display-Regular  -pointsize 160 -fill none -stroke white -strokewidth 10  -annotate +120+120 '04' track-output-poster3.png
   ## include pull svgs https://github.com/f1laps/f1-track-vectors
   ## these are modified to increase track width and size
   ## convert svg to png with alphas
   ## $ for i in *; do echo "$i"; magick -background none  "$i" -resize 540x540 ../track_png/"$(echo "$i" | sed 's/svg/png/')" ; done
   ## rotate and rename specific races

    if not f1_fonts:
        font_regular = 'Copperplate'
        font_bold = 'Copperplate-Bold'
        font_wide = 'Copperplate-Bold'
        font_black = 'Copperplate-Bold'
    else:
        font_regular = 'Formula1-Display-Regular'
        font_bold = 'Formula1-Display-Bold'
        font_wide = 'Formula1-Display-Wide'
        font_black = 'Formula1-Display-Black'

    if os.path.isfile(str(image_path + "/" + race_name + "-background.jpg")):
        background_image = str(image_path + "/" + race_name + "-background.jpg")
    else:
        background_image = str(image_path + "/" + race_season + "-background.jpg")
    background_destination = str(destination_folder + "/background.jpg")

    if os.path.isfile(str(track_path + "/" + race_name.lower() + ".png")):
        track_map_image = str(track_path + "/" + race_name.lower() + ".png")
        track_geometry = '540x540+160+160'
        generate_background_cmd = ["magick", background_image,
                                   "-resize", "1920x1080\!",
                                   "-blur", "0x4",
                                   track_map_image,
                                   "-compose", "Src_Over",
                                   "-background", "None",
                                   "-gravity", "NorthEast",
                                   "-geometry", track_geometry,
                                   "-composite",
                                   "-gravity", "NorthEast",
                                   "-font", font_regular,
                                   "-pointsize", "240",
                                   "-fill", "none",
                                   "-stroke", "white",
                                   "-strokewidth", "10",
                                   "-annotate", "+120+120", race_round,
                                   background_destination]

    else:
        generate_background_cmd = ["magick", background_image,
                                   "-resize", "1920x1080\!",
                                   "-blur", "0x1",
                                   "-gravity", "NorthEast",
                                   "-font", font_regular,
                                   "-pointsize", "240",
                                   "-fill", "none",
                                   "-stroke", "white",
                                   "-strokewidth", "10",
                                   "-annotate", "+120+120", race_round,
                                   background_destination]

    try:
        subprocess.call(generate_background_cmd)
    except FileExistsError as err:
        print(err)

    return


def create_poster_image(f1_fonts, image_path, destination_folder, race_season, race_round, race_name):
    """ generates images with imagemagick"""

    race_poster = str(image_path + "/" + race_season + ".png")
    race_poster_destination = str(destination_folder + "/show.png")

    if not f1_fonts:
        font_regular = 'Copperplate'
        font_bold = 'Copperplate-Bold'
        font_wide = 'Copperplate-Bold'
        font_black = 'Copperplate-Bold'
    else:
        font_regular = 'Formula1-Display-Regular'
        font_bold = 'Formula1-Display-Bold'
        font_wide = 'Formula1-Display-Wide'
        font_black = 'Formula1-Display-Black'

    # adjust title size for longer race_name
    if len(race_name) > 10:
        point_size = "65"
    else:
        point_size = "86"

    if os.path.isfile(str(track_path + "/" + race_name.lower() + ".png")):
        track_map_image = str(track_path + "/" + race_name.lower() + ".png")
        track_geometry = '300x300+60'
        generate_race_poster_cmd = ["magick", race_poster,
                                    "-resize", "600x900\!",
                                    "-blur", "0x6",
                                    track_map_image,
                                    "-compose", "Src_Over",
                                    "-background", "None",
                                    "-gravity", "Center",
                                    "-geometry", track_geometry,
                                    "-composite",
                                    "-gravity", "Center",
                                    "-font", font_black,
                                    "-pointsize", point_size,
                                    "-fill", "red",
                                    "-stroke", "black",
                                    "-strokewidth", "2",
                                    "-annotate", "+0-220", race_name,
                                    "-font", font_wide,
                                    "-fill", "black",
                                    "-stroke", "white",
                                    "-strokewidth", "2",
                                    "-pointsize", "40",
                                    "-gravity", "NorthWest",
                                    "-annotate", "+30+30", race_season,
                                    "-gravity", "SouthEast",
                                    "-font", font_regular,
                                    "-pointsize", "160",
                                    "-fill", "none",
                                    "-stroke", "white",
                                    "-strokewidth", "10",
                                    "-annotate", "+10+10", race_round,
                                    race_poster_destination]
    else:
        generate_race_poster_cmd = ["magick", race_poster,
                                    "-resize", "600x900\!",
                                    "-blur", "0x2",
                                    "-gravity", "Center",
                                    "-font", font_black,
                                    "-pointsize", point_size,
                                    "-fill", "red",
                                    "-stroke", "black",
                                    "-strokewidth", "2",
                                    "-annotate", "+0-220", race_name,
                                    "-font", font_wide,
                                    "-fill", "black",
                                    "-stroke", "white",
                                    "-strokewidth", "2",
                                    "-pointsize", "40",
                                    "-gravity", "NorthWest",
                                    "-annotate", "+30+30", race_season,
                                    "-gravity", "SouthEast",
                                    "-font", font_regular,
                                    "-pointsize", "160",
                                    "-fill", "none",
                                    "-stroke", "white",
                                    "-strokewidth", "10",
                                    "-annotate", "+10+10", race_round,
                                    race_poster_destination]

    try:
        subprocess.call(generate_race_poster_cmd)
    except FileExistsError as err:
        print(err)
    else:
        print("Created image: " + race_poster_destination)

    return


def build_out_files(source_file_names, sprint_weekends):
    """ check if this is a media file, parse filename, sort by keywords into
    folders, link files to destination directory"""

    images_linked = []
    backgrounds_linked = []

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
            os.makedirs(destination_folder, exist_ok=True)
            final_file_path = str(destination_folder + '/' + final_file_name)
            # print(final_file_path)

            if destination_folder not in backgrounds_linked:
                create_background_image(f1_fonts, image_path, destination_folder,
                                        race_season, race_round, race_name)
                backgrounds_linked.append(destination_folder)

            if destination_folder not in images_linked:
                create_poster_image(f1_fonts, image_path, destination_folder,
                                    race_season, race_round, race_name)
                images_linked.append(destination_folder)

            try:
                os.link(source_file_name, final_file_path)
            except FileExistsError as err:
                print(str(err))


def get_f1_fonts(fonts, path):
    """ download F1 official fonts if missing"""

    f1_fonts = True

    os.makedirs(path, exist_ok=True)
    for url_path, font_name in fonts:
        if not os.path.isfile(str(font_path + "/" + font_name)):
            try:
                urllib.request.urlretrieve(url_path, str(path + "/" + font_name))
            except OSError as err:
                print("Can't download F1 Font: " + str(err))
                f1_fonts = False
            else:
                print("Downloaded " + font_name)
    return f1_fonts


if __name__ == "__main__":
    """ main """

    # sanity checks
    f1_fonts = get_f1_fonts(font_list, font_path)

    if not f1_fonts:
        print("Can't download required fonts")
        raise SystemExit()
    elif not which('magick'):
        print("imagemagick not found")
        raise SystemExit()
    else:
        print("checks passed")

    # main start

    source_file_names = list_files(source_path)

    print("Found " + str(len(source_file_names)) + " items to process.")

    sprint_weekends = find_sprint_weekends(source_file_names, sprint_weekends)

    print("Found " + str(len(sprint_weekends)) + " sprint weekends.")

    print("Linking files.")

    build_out_files(source_file_names, sprint_weekends)






