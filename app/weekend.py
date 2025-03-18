#!/usr/bin/python
# weekend.py
#

import glob

class Weekend(object):
    """race weekend"""

    def __init__(self, destination_path):
        self.race_session = ""
        self.race_name = ""
        self.race_info = ""
        self.race_round = "00"
        self.filetype = ""
        self.final_file_name = ""
        self.destination_folder = ""
        self.race_round_path = ""
        self.race_series = ""
        self.race_season = ""
        self.gp_suffix = ""
        self.weekend_order = ""
        self.directory_images = []
        self.destination_path = destination_path

    def set_directory_images_created(self, destination_folder):
        """ """
        self.directory_images.append(destination_folder)

    def get_directory_images_created(self):
        """ """
        return self.directory_images

    def set_race_session(self, race_session):
        """ """
        self.race_session = race_session

    def get_race_session(self):
        return self.race_session

    def set_gp_suffix(self, gp_suffix):
        """ """
        self.gp_suffix = gp_suffix

    def get_gp_suffix(self):
        return self.gp_suffix

    def set_race_name(self, race_name):
        """ """
        self.race_name = race_name

    def get_race_name(self):
        return self.race_name

    def set_race_info(self, race_info):
        """ """
        self.race_info = race_info

    def get_race_info(self):
        return self.race_info

    def set_race_round(self, race_round):
        """ """
        self.race_round = race_round

    def get_race_round(self):
        return self.race_round

    def set_filetype(self, filetype):
        """ """
        self.filetype = filetype

    def set_weekend_order(self, weekend_order):
        """ """
        self.weekend_order = weekend_order

    def set_race_series(self, race_series):
        """ """
        self.race_series = race_series

    def get_race_series(self):
        """ """
        return self.race_series

    def set_race_season(self, race_season):
        """ """
        self.race_season = race_season

    def get_race_season(self):
        return self.race_season

    def get_final_file_name(self):
        if self.race_series == "Formula 1":
            self.gp_suffix = " GP"

        return str(self.race_name + self.gp_suffix + " - S" + self.race_round + "E" +
                   self.weekend_order + " - " + self.race_session +
                   " [" + self.race_info + "]" + self.filetype)

    def get_destination_folder(self):
        """ use an existing race_season + race_round directory even if race_name differs"""

        # this is a partial path search to see if the race already exists with 
        # a slightly different name. The Imola/Italian GP problem.
        self.race_round_path = str(self.destination_path + "/" + self.race_series +
                                   "/" + self.race_season + "-" + self.race_round)
        self.race_round_path_found = glob.glob(self.race_round_path + '*')

        # if a partial match is found use it, otherwise return the build up
        # path name.
        if self.race_round_path_found:
            self.destination_folder = str(self.race_round_path_found[0])
            # print('Found existing race directory: ' + self.destination_folder)
        else:
            self.destination_folder = str(self.destination_path + "/" + self.race_series +
                                          "/" + self.race_season + "-" + self.race_round +
                                          " - " + self.race_name + self.gp_suffix)
            # print('Creating destination directory.')

        return self.destination_folder

    def get_destination_full_path(self):
        return str(self.destination_folder + "/" + self.get_final_file_name())
