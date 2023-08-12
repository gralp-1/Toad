#!/usr/bin/env python3

# TODO: Config in ~/.config/toad/config.toml
#       || %APPDATA%\toad\config.toml for windows

import sys
import os
import yaml
from pathlib import Path
import fire
import pickle
import time
import prettytable as pt


def base_path() -> Path:
    """
    Return the path to the data directory (where the tasks are stored)A
    """
    if sys.platform == "win32":
        return Path(os.getenv("APPDATA")) / "toad" / "tasks.pickle"
    else:
        return Path(os.getenv("HOME")) / ".config" / "toad" / "tasks.pickle"


# config_path = base_path() / "config.yaml"
data_path = base_path() / "tasks.pickle"


def check_first_run():
    """if data_path() does not exist, create it and write an empty dict to it"""
    base_path_exists = base_path().exists()
    # config_path_exists = config_path.exists()
    data_path_exists = data_path.exists()
    if not base_path_exists:
        print("Creating toad path")
        os.makedirs(base_path())
    # if not config_path_exists:
    #    print("Creating config file")
    #    with open(config_path, "w") as f:
    #        yaml.dump({}, f)
    if not data_path_exists:
        print("Creating tasks save file")
        with open(data_path, "wb") as f:
            pickle.dump({}, f)


class Toad(object):
    def __init__(self):
        self.__items = self.__load_data()

    def done(self, index: int):
        """
        Complete a task at the given index
        """
        self.__items[index]["complete"] = True

    def list(self):
        """
        List all tasks
        """
        table = pt.PrettyTable()
        table.field_names = ["Index", "Name", "Set Time", "Complete"]
        for index, item in self.__items.items():
            complete_string = "✅" if item["complete"] else "❌"
            # format time
            time_string = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(item["set_time"])
            )
            table.add_row([index, item["name"], time_string, complete_string])
        print(table)

    def add(self, name: str):
        """
        Add a new task to the list
        """
        self.__items[self.__next_index()] = {
            "name": name,
            "set_time": time.time(),
            "complete": False,
        }

    def remove(self, index: int):
        """
        Remove the task at the given index
        """
        del self.__items[index]

    def clear(self):
        """
        Remove all tasks
        """
        self.__items = {}

    def __save_data(self):
        with open(data_path, "wb") as f:
            pickle.dump(self.__items, f)

    def __load_data(self) -> dict:
        with open(data_path, "rb") as f:
            return pickle.load(f)

    def __next_index(self) -> int:
        return len(self.__items) + 1

    def __del__(self):
        self.__save_data()


if __name__ == "__main__":
    check_first_run()
    fire.Fire(Toad)
