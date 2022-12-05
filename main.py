"""

"""
import gzip
import requests
import saveas

from time import time
from os import walk
from os.path import sep


"""Core Functions"""


def get_target_folders():
    """Reads target_folders.txt and returns a list of target folders"""
    try:
        with open("target_folders.txt", "r") as file_handle:
            server_folders_string = str(file_handle.read())
        feedback("'target_folders.txt' loaded successfully!")
    except FileNotFoundError:
        oops("No target_folders.txt found in local directory.\n"
             "Please double check that this file is in the same directory as main.py.\n"
             "You can get another copy of it from the github repository, but making your own shouldn't cause problems.")

    server_folders_list = server_folders_string.split("\n")

    if server_folders_list[-1] == "":
        server_folders_list.pop(-1)

    return server_folders_list


def get_file_list(directories: list) -> list:
    """Catalogues the paths of all .log.gz files in target directories & sub directories"""
    file_list = []
    feedback("Searching target folders for .log.gz files...")

    for directory in directories:
        for (root, dirs, file) in walk(directory):
            for f in file:
                if ".log.gz" in f:
                    file_list.append(f"{root}{sep}{f}")

    if len(file_list) == 0:  # error check
        oops("No .log.gz files found in specified directories.\n"
             "Please double check target_folders.txt and make sure your server directories are correct.\n"
             'A "correct" server directory is either the root (where the server jar is) or the logs folder. '
             "Paths can be written relative to this directory or as full paths, but only one path per line is allowed.")

    feedback(f"Found {len(file_list)} applicable files!")
    return file_list


def combine_file_list(file_list: list[str]) -> list[str]:
    """Combines all found log files into a list with each line of each file as an element"""
    log_rows = []
    bad_files_string = ""
    feedback(f"Loading {len(file_list)} files, this will the longest operation...")

    for filepath in file_list:
        try:
            with gzip.open(filepath, "rb") as opened_file:
                readfile = str(opened_file.read())
            log_rows += readfile.split("\\r\\n")
        except Exception:  # yes it's too broad, no I don't know what the right exception is, this should never trigger
            bad_files_string += (filepath + "\n")

    if len(bad_files_string) > 0:
        global BAD_FILES
        BAD_FILES = True
        saveas.txt("bad_files.txt", bad_files_string)

    return log_rows


def get_player_names(log_rows: list[str]) -> list[str]:
    """Extracts all unique player names from combined log files"""
    players = []
    feedback("Finding unique player names in log files...")

    for row in log_rows:
        if "joined the game" in row:
            player_name = row.split(" ")[-4]
            if player_name not in players:  # ensures only unique player names are added to the list
                players.append(player_name)

    feedback(f"Found {len(players)} unique player names!")
    return players


def get_uuid(player_name) -> str:
    """
    Looks up a player's UUID using their account name and the mojang API: https://wiki.vg/Mojang_API#Username_to_UUID

    I am formally acknowledging Usernames to UUIDs would plainly be more efficient; however...
    Outside of testing, I planned on running a total of one times, so easier == better
    Similar concessions have been made in regards to nice_uuid's formatting
    """
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}")
    uuid = response.json()["id"]
    nice_uuid = f"{uuid[0:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
    feedback(f"{nice_uuid} : {player_name}")
    return nice_uuid


def generate_whitelist(player_names: list[str]) -> list[dict]:
    """
    This is the function that actually generates the whitelist from a list of player names
    :param player_names: A list of player names
    :return: A list of dictionaries, formatted to be used as a whitelist for a Minecraft server
    """
    whitelist = []
    feedback(f"Looking up UUIDs for {len(player_names)} player names...")

    for name in player_names:
        uuid = get_uuid(name)
        entry = {
            "uuid": uuid,
            "name": name
        }
        whitelist.append(entry)
    return whitelist


"""Periphery functions"""


def oops(error_message: str):
    """Simple way to display an error to the user without creating files or causing the terminal to close"""
    print("\n\n! ! ! ERROR ! ! !\n")
    input(f"{error_message}\n\nPress 'Enter' to close, or close the window.")
    exit()


def feedback(feedback_string: str):
    """Used in place of making the below if statement everytime I want to generate feedback to the user"""
    if DO_FEEDBACK:
        print(feedback_string)


def main():  # main
    """Main"""
    start = time()  # for time-elapsed calculation

    # meat and potatoes
    targets = get_target_folders()  # get target folders
    file_list = get_file_list(targets)  # get all .gz files in all target folders/sub folders
    log_rows = combine_file_list(file_list)  # open and split all log file rows into list
    player_names = get_player_names(log_rows)  # extract unique player names from list
    whitelist = generate_whitelist(player_names)  # generate whitelist from player names
    saveas.json("whitelist.json", whitelist)  # save to disc

    # everything past this line is feedback related
    feedback("\nDone! Your whitelist has been saved to the directory you ran this script from as 'whitelist.json'"
             "\nHave a great day, and happy hosting!")
    if BAD_FILES and DO_FEEDBACK:  # the BAD_FILES flag change can be found in the combine_file_list() function
        print("Some files failed to open. Please see 'bad_files.txt for a list.")
    if DO_FEEDBACK:
        input(f"\n{round(time() - start, 2)}s elapsed. Press 'enter' to close this window.")  # display time elapsed


DO_FEEDBACK = False  # so, if for some reason, you use my functions in your code, they don't print all the things
BAD_FILES = False

if __name__ == '__main__':
    DO_FEEDBACK = True
    main()
