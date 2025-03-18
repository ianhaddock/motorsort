# pytest tests

import pytest
import os
import shutil
import json
from configparser import ConfigParser
from motorsort import main, parse_file_name, get_file_list, find_sprint_weekends
from weekend import Weekend

config = ConfigParser()
config.read('config/config.ini')
file_prefix = tuple(config.get('config', 'file_prefix').split(','))
file_types = tuple(config.get('config', 'file_types').split(','))
weekends = config.get('config', 'sprint_weekends').split(',')
image_path = config.get('config', 'image_path')
track_path = config.get('config', 'track_path')
flag_path = config.get('config', 'flag_path')
font_path = config.get('config', 'font_path')

with open('config/series_prefix.json') as file:
    series_prefix = json.load(file)
with open('config/weekend_order.json') as file:
    the_weekend_order = json.load(file)
with open('config/session_map.json') as file:
    session_map = json.load(file)
with open('config/fonts.json') as file:
    font_list = json.load(file)


def test_get_final_name(tmp_path):

    race = Weekend(tmp_path)
    race.set_race_name('race_name')
    race.set_race_round('01')
    race.set_weekend_order('02')
    race.set_race_session('Qualifying')
    race.set_race_info('Race Info')
    race.set_filetype('.mov')

    assert race.get_final_file_name() == 'race_name - S01E02 - Qualifying [Race Info].mov'


def test_get_destination_folder_new_path(tmp_path):

    race = Weekend(f'{tmp_path}/motorsort')
    race.set_race_series("Race Series")
    race.set_race_name('race_name')
    race.set_race_season("2024")
    race.set_race_round('01')

    assert race.get_destination_folder() == f'{tmp_path}/motorsort/Race Series/2024-01 - race_name'


def test_get_destination_folder_partial_path_match(tmp_path):

    race = Weekend(f'{tmp_path}/motorsort')
    race.set_race_series("Race Series")
    race.set_race_name('race_name')
    race.set_race_season("2024")
    race.set_race_round('01')
    os.makedirs(f'{tmp_path}/motorsort/Race Series/2024-01 - other_race_name')

    assert race.get_destination_folder() == f'{tmp_path}/motorsort/Race Series/2024-01 - other_race_name'


def test_parse_file_name_formula_1_regular_weekend(tmp_path):

    race = Weekend(f'{tmp_path}/motorsort')
    sprint_weekends = [(2024, '05'), ('2023', '21')]
    file_name = 'test_media/Formula1.2022.Round04.Example.FP1.FastChannelHD.1080p.50fps.X264.Multi-AOA11 mkv'
    parse_file_name(race, series_prefix, session_map, sprint_weekends, the_weekend_order, file_name)

    assert race.get_final_file_name() == 'Example GP - S04E01 - Free Practice 1 [FastChannelHD 1080p 50fps X264].Multi-AOA11 mkv'


def test_parse_file_name_formula_1_sprint_weekend(tmp_path):

    race = Weekend(f'{tmp_path}/motorsort')
    sprint_weekends = [(2024, '05'), ('2023', '21')]
    file_name = 'test_media/Formula1.2023.Round21.Example.Sprint.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv'
    parse_file_name(race, series_prefix, session_map, sprint_weekends, the_weekend_order, file_name)

    assert race.get_race_session() == 'Sprint'


def test_parse_file_name_wec_and_no_suffix(tmp_path):

    race = Weekend(f'{tmp_path}/motorsort')
    sprint_weekends = [(2024, '05'), ('2023', '21')]
    file_name = 'test_media/WEC.2022.Round04.Example.Race04.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv'
    parse_file_name(race, series_prefix, session_map, sprint_weekends, the_weekend_order, file_name)

    assert race.get_race_series() == 'World Endurance Championship'
    assert not race.get_gp_suffix() == ' GP'


def test_parse_file_name_no_round_name(tmp_path):

    race = Weekend(f'{tmp_path}/motorsort')
    sprint_weekends = [(2024, '05'), ('2023', '21')]
    file_name = 'test_media/Formula1.2022.Round03.FP1.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv'
    parse_file_name(race, series_prefix, session_map, sprint_weekends, the_weekend_order, file_name)

    assert race.get_race_name() == ''


def test_parse_file_name_no_round_number(tmp_path):

    race = Weekend(f'{tmp_path}/motorsort')
    sprint_weekends = [(2024, '05'), ('2023', '21')]
    file_name = 'test_media/Formula1.2022.Example.FP1.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv'
    parse_file_name(race, series_prefix, session_map, sprint_weekends, the_weekend_order, file_name)

    assert race.get_race_round() == '00'


def test_parse_file_usa_remove(tmp_path):

    race = Weekend(f'{tmp_path}/motorsort')
    sprint_weekends = [(2024, '05'), ('2023', '21')]
    file_name = 'test_media/Formula1.2022.Round04.USA.Example.FP1.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv'
    parse_file_name(race, series_prefix, session_map, sprint_weekends, the_weekend_order, file_name)

    assert race.get_race_name() == 'Example'


def test_parse_file_france_remove(tmp_path):

    race = Weekend(f'{tmp_path}/motorsort')
    sprint_weekends = [(2024, '05'), ('2023', '21')]
    file_name = 'test_media/WEC.2022.Round04.France.Example.FP1.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv'
    parse_file_name(race, series_prefix, session_map, sprint_weekends, the_weekend_order, file_name)

    assert race.get_race_name() == 'Example'


def test_get_file_list_source_path_error():

    with pytest.raises(SystemExit) as exit_info:
        get_file_list('source/does_not_exist', 'F1', 'mkv')

    assert exit_info.value.args[0] == "ERROR, can't find source path: source/does_not_exist"


def test_get_file_list(tmp_path):

    shutil.copytree('media/source_files/complete', f'{tmp_path}/source/complete')

    assert get_file_list(f'{tmp_path}/source/complete', 'Formula1', 'mkv') == \
        [
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.FP1.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.FP2.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.FP3.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Onboard.Channel.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Quali.Analysis.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Qualifying.Buildup.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Qualifying.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Qualifying.Teds.Notebook.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Race.Analysis.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Race.Buildup.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Race.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Sprint.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Sprint.Shootout.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Teds.Race.Notebook.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Teds.Sprint.Notebook.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
        ]


def test_find_sprint_weekends(tmp_path):

    source_file_names = \
        [
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.FP1.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.FP2.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.FP3.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Onboard.Channel.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Quali.Analysis.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Qualifying.Buildup.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Qualifying.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Qualifying.Teds.Notebook.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Race.Analysis.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Race.Buildup.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Race.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Sprint.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Sprint.Shootout.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Teds.Race.Notebook.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
            f'{tmp_path}/source/complete/Formula1.2022.Round00.Example.Teds.Sprint.Notebook.FastChannelHD.1080p.50fps.X264.Multi-AOA11.mkv',
        ]

    assert find_sprint_weekends(source_file_names, weekends) == \
        [
        ('2025', '05'),
        ('2025', '06'),
        ('2025', '11'),
        ('2025', '19'),
        ('2025', '21'),
        ('2025', '23'),
        ('2022', '00')
        ]
