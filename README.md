# mc-retroactive-whitelist-gen
This is a simple—if inelegantly named—tool I cooked up in an hour or two to generate a single unified whitelist I can use across all my minecraft servers. It's intended for people running private servers for small communities, like myself. Maybe you'll find it useful.

The design intention was to whitelist everyone who has already played on any of my servers, minimizing the possibility that anyone will bother me saying they aren't on the whitelist. Basically I wanted to transparently whitelist the server, not for any discretionary reason, but out of convenience for the existing player base. It worked great!

The way it works is: it catalogues and opens all .log.gz files in the provided directories (target_folders.txt) and their sub-directories, searches them for instances of players joining, creates a list of unique player names, looks up everyone's UUID, and finally, saves the name & id pairs in the correct file format to be used as a whitelist. The prospective server host may then distribute said whitelist into as many servers as they desire.

## Dependencies

Requires [Python 3](https://www.python.org/) & [Requests](https://github.com/psf/requests) to run. 

It was written using Python 3.10 on Windows, but it's simple enough that it probably works on Python 3.x. The paths were written using the os.path.sep character, so it should work on Mac and Linux as well, but I promise nothing.

## Usage

1. Make sure you have the dependencies.
2. Replace the contents of **target_folders.txt** with the log folder path(s) you wish to search. I've left some full paths in the file as an example.
3. Run **main.py**. If it's working correctly, it should start streaming commentary as it works, including errors.
4. Check the resulting whitelist.json file for accuracy and prune any undesirables.
5. Distribute said file among your server(s).

You'll still need to enable the whitelist on your server, but this handles the hassle of whitelisting all your players.
