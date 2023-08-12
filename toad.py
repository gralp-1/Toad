#!/usr/bin/env python3

# TODO: Config in ~/.config/toad/config.toml
#       || appdata/toad/config.toml for windows

import sys
import fire
import pickle
import time
import prettytable as pt

save_path = "./todo_items.pickle"


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
            time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["set_time"]))
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
        with open(save_path, "wb") as f:
            pickle.dump(self.__items, f)

    def __load_data(self) -> dict:
        with open(save_path, "rb") as f:
            return pickle.load(f)
    def __next_index(self) -> int:
        return len(self.__items) + 1
    def __del__(self):
        self.__save_data()

if __name__ == "__main__":
    fire.Fire(Toad)
