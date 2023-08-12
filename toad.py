#!/usr/bin/env python3

import sys
import pickle
import json
import logging as log
log.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

save_path = "./todo_items.json"
# {name:"", set_time:000, complete:False}

def save_data(data: dict):
    with open(save_path, "wb") as f:
        pickle.dump(data, f)
        log.debug("Saved data")


def load_data() -> dict:
    with open(save_path, "rb") as f:
        data: dict = json.load(f)
        log.debug(f"Loaded data {data}")
    return data


def main(args: list[str]):
    todo_items: dict = load_data()
    match args[0]:
        case "add":
            todo_items[args[1]] = {"set_time": 0, "complete": False}
        case "remove":
            del todo_items[args[1]]
        case "list":
            for key, value in todo_items.items():
                print(key, value)
        case "complete":
            todo_items[args[1]]["complete"] = True
    save_data(todo_items)

if __name__ == "__main__":
    main(sys.argv[1:])
