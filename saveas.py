"""
Simple utility functions to easily save files in various formats.
V2
"""
from json import dump
import gzip


def txt(filename: str, filecontents: str):
    """
    Saves filecontents as a .txt file.
    :param filename: the name of the file you wish to create (including the extension)
    :param filecontents: the data you wish to save in your file
    :return: None
    """
    with open(filename, "w") as filehandle:
        filehandle.write(filecontents)


def json(filename: str, filecontents):
    """
    Saves filecontents as a .json file.
    :param filename: the name of the file you wish to create (including the extension)
    :param filecontents: the data you wish to save in your file
    :return: None
    """
    with open(filename, "w") as filehandle:
        dump(filecontents, filehandle, indent=4)


def gz(filename: str, filecontents):
    """
    Saves filecontents as a .gz file.
    :param filename:
    :param filecontents:
    :return:
    """
    with gzip.open(filename, "wt", encoding="UTF-8") as filehandle:
        dump(filecontents, filehandle, indent=4)


def file(filename: str, filecontents):
    """
    Saves filecontents as the appropriate filetype based on the extension of filename.
    :param filename:
    :param filecontents:
    :return:
    """
    sections = filename.split(".")
    extension = sections[-1]
    if extension == "txt":
        txt(filename, filecontents)
    elif extension == "json":
        json(filename, filecontents)
    elif extension == "gz":
        gz(filename, filecontents)
    else:
        print("File type not found!")
    pass


def test():
    file("test.txt", "this is a test for the .txt function")
    file("test.json", {"this is": "a test for the .json function"})
    file("test.json.gz", {"this is": "a test for the .gz function"})
    # csv("test.csv", {"header 1": ["a2", "a3"],
    #                  "header 2": ["b2", "b3", "b4"]})


if __name__ == "__main__":
    test()
