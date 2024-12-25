# pytest tests
#
# if you want to see the temp_path the images are written to, add 'assert 0' after
# the last test and look at the error output
#


import pytest
import os
import shutil
import json
from configparser import ConfigParser
from motorsort import weekend
from poster_maker import create_poster_image, create_background_image

sprint_weekends = [(2024, '05'), ('2023', '21')]
destination_path = "destination_top"

race = weekend()
race.set_race_name('race_name')
race.set_gp_suffix('GP')
race.set_race_round('01')
race.set_weekend_order('02')
race.set_race_session('Qualifying')
race.set_race_info('Race Info')
race.set_filetype('mov')
race.set_race_series("Race Series")
race.set_race_season("2024")

# read config.ini file
config = ConfigParser()
config.read('config/config.ini')
file_prefix = tuple(config.get('config', 'file_prefix').split(','))
file_types = tuple(config.get('config', 'file_types').split(','))
weekends = config.get('config', 'sprint_weekends').split(',')
image_path = 'config/images'
track_path = 'config/tracks'
flag_path = 'config/flags'
font_path = 'fonts'

# read json files
with open('config/series_prefix.json') as file:
    series_prefix = json.load(file)
with open('config/weekend_order.json') as file:
    the_weekend_order = json.load(file)
with open('config/session_map.json') as file:
    session_map = json.load(file)
with open('config/fonts.json') as file:
    font_list = json.load(file)


def test_poster_maker_cant_write_background_to_dest(tmp_path):

    os.makedirs(f'{tmp_path}/Race Series', mode=0o500, exist_ok=False)
    with pytest.raises(SystemExit) as exit_info:
        create_background_image(race, font_list, image_path, str(tmp_path))

    assert exit_info.value.args[0] == f"ERROR, can't create path: [Errno 13] Permission denied: '{tmp_path}/Race Series/2024-01 - race_name GP'"


def test_poster_maker_cant_write_poster_to_dest(tmp_path):

    os.makedirs(f'{tmp_path}/Race Series', mode=0o500, exist_ok=False)
    with pytest.raises(SystemExit) as exit_info:
        create_poster_image(race, font_list, track_path, flag_path,  image_path, str(tmp_path))

    assert exit_info.value.args[0] == f"ERROR, can't create path: [Errno 13] Permission denied: '{tmp_path}/Race Series/2024-01 - race_name GP'"


def test_poster_maker_background_exists(tmp_path):

    os.makedirs(f'{tmp_path}/Race Series/2024-01 - race_name GP')
    shutil.copy('tests/test_data/background.jpg', f'{tmp_path}/Race Series/2024-01 - race_name GP/background.jpg')
    create_background_image(race, font_list, image_path, str(tmp_path))

    assert os.path.isfile(f'{str(tmp_path)}/Race Series/2024-01 - race_name GP/background.jpg')


def test_poster_maker_poster_exists(tmp_path):

    os.makedirs(f'{tmp_path}/Race Series/2024-01 - race_name GP')
    shutil.copy('tests/test_data/show.png', f'{tmp_path}/Race Series/2024-01 - race_name GP/show.png')
    create_poster_image(race, font_list, track_path, flag_path,  image_path, str(tmp_path))

    assert os.path.isfile(f'{str(tmp_path)}/Race Series/2024-01 - race_name GP/show.png')


def test_poster_maker_create_background_image_default_background_image(tmp_path):

    create_background_image(race, font_list, image_path, str(tmp_path))

    assert os.path.isfile(f'{str(tmp_path)}/Race Series/2024-01 - race_name GP/background.jpg')


def test_poster_maker_create_background_image_with_race_season_background(tmp_path):

    race.set_race_season('2023')
    create_background_image(race, font_list, image_path, str(tmp_path))

    assert os.path.isfile(f'{str(tmp_path)}/Race Series/2023-01 - race_name GP/background.jpg')


def test_poster_maker_create_background_image_with_race_name_background(tmp_path):

    race.set_race_name('COTA')
    create_background_image(race, font_list, image_path, str(tmp_path))

    assert os.path.isfile(f'{str(tmp_path)}/Race Series/2023-01 - COTA GP/background.jpg')


def test_poster_maker_create_poster_image(tmp_path):

    create_poster_image(race, font_list, track_path, flag_path, image_path, str(tmp_path))

    assert os.path.isfile(f'{str(tmp_path)}/Race Series/2023-01 - COTA GP/show.png')


def test_poster_maker_create_poster_image_formula_1_series(tmp_path):

    race.set_race_series('Formula 1')
    race.set_race_name('race_name')
    create_poster_image(race, font_list, track_path, flag_path, image_path, str(tmp_path))

    assert os.path.isfile(f'{str(tmp_path)}/Formula 1/2023-01 - race_name GP/show.png')


def test_poster_maker_create_poster_image_WEC_series(tmp_path):

    race.set_race_series('World Endurance Championship')
    create_poster_image(race, font_list, track_path, flag_path, image_path, str(tmp_path))

    assert os.path.isfile(f'{str(tmp_path)}/World Endurance Championship/2023-01 - race_name GP/show.png')


def test_poster_maker_create_poster_image_with_track_map(tmp_path):

    race.set_race_name('COTA')
    race.set_race_series('Formula 1')
    create_poster_image(race, font_list, track_path, flag_path, image_path, str(tmp_path))

    assert os.path.isfile(f'{str(tmp_path)}/Formula 1/2023-01 - COTA GP/show.png')


def test_poster_maker_create_poster_image_with_default_poster_bkg_image(tmp_path):

    race.set_race_name('race_name')
    race.set_race_series('Le Mans')
    race.set_race_season('2222')
    create_poster_image(race, font_list, track_path, flag_path, image_path, str(tmp_path))

    assert os.path.isfile(f'{str(tmp_path)}/Le Mans/2222-01 - race_name GP/show.png')
