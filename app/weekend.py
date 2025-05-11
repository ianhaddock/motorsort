#!/usr/bin/python
"""motorsort weekend.py"""

import glob


class Weekend:
    """race weekend"""

    def __init__(self, destination_path):
        self.event = {
            "destination_path": destination_path,
        }

    def set_kv(self, key: str, value: str):
        """set key value pairs for a race event"""
        self.event[key] = value.strip()

    def get_kv(self, key: str) -> str:
        """returns the value of a key"""
        return self.event[key]

    def get_race_name(self):
        """get race name"""
        if self.event["race_series"] == "Formula 1":
            return f'{self.event["race_name"]} GP'
        return self.event["race_name"]

    def get_final_file_name(self):
        """build final file name"""
        return str(
            self.get_race_name()
            + " - S"
            + self.event["race_round"]
            + "E"
            + self.event["weekend_order"]
            + " - "
            + self.event["race_session"]
            + " ["
            + self.event["race_info"].replace(".", " ").strip(" ")
            + "]"
            + self.event["file_extension"]
        )

    def get_destination_folder(self):
        """use an existing race_season + race_round directory even if race_name differs"""

        # this is a partial path search to see if the race already exists with
        # a slightly different name. The Imola/Italian GP problem.
        self.event["race_round_path"] = str(
            self.event["destination_path"]
            + "/"
            + self.event["race_series"]
            + "/"
            + self.event["race_season"]
            + "-"
            + self.event["race_round"]
        )
        self.event["race_round_path_found"] = glob.glob(
            self.event["race_round_path"] + "*"
        )

        # if a partial match is found use it, otherwise return the build up
        # path name.
        if self.event["race_round_path_found"]:
            self.event["destination_folder"] = str(
                self.event["race_round_path_found"][0]
            )
            # print('Found existing race directory: ' + self.event["destination_folder"])
        else:
            self.event["destination_folder"] = str(
                self.event["destination_path"]
                + "/"
                + self.event["race_series"]
                + "/"
                + self.event["race_season"]
                + "-"
                + self.event["race_round"]
                + " - "
                + self.get_race_name()
            )
            # print('Creating destination directory.')
        return self.event["destination_folder"]

    def get_destination_full_path(self):
        """get full path for destination files"""
        return str(self.get_destination_folder() + "/" + self.get_final_file_name())
