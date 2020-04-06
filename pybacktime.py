"""Backs up files and database as per settings, uploads to destination"""
import json
import sys
import os
import subprocess

# check parameters
PARAM_COUNT = len (sys.argv)
REQ_PARAMS = 2
if PARAM_COUNT != REQ_PARAMS:
    print ("Parameter error: Invalid usage\n")
    sys.exit()

# get set name to execute
BACKUP_SETNAME = sys.argv [1]

# keys and constants
SETTINGS_FILE = "settings.json"
SET_CONTAINER = "backup_sets"
SET_ACTIVE = "active"
SET_DESC = "description"
SET_SETTINGS = "settings"
SET_DEST = "backup_destination"
SET_SRC = "filepaths"

# open the settings file
try:
    SETTINGS = json.load (open (SETTINGS_FILE, "r"))
except FileNotFoundError:
    print(f"File error: Settings not found - {SETTINGS_FILE}.\n")
    sys.exit()

# check if there is a container for the
# backup sets
BACKUP_SETS = SETTINGS.get (SET_CONTAINER)
if BACKUP_SETS is None:
    print(f"Key error: Backup sets not found.\n")
    sys.exit()

# check if set exists
SET_CONFIG = BACKUP_SETS.get (BACKUP_SETNAME)
if SET_CONFIG is None:
    print(f"Set error: Specified backup set not found.\n")
    sys.exit()
print (f"Processing: {BACKUP_SETNAME}")

# set exists
# get set information
# is set active present and true?
ACTIVE_CFG = SET_CONFIG.get (SET_ACTIVE)
if ACTIVE_CFG is None:
    print(f"Set error: Active indicator key not found.\n")
    sys.exit()
if not ACTIVE_CFG:
    print(f"Set error: Specified backup set is not active.\n")
    sys.exit()

# get set description
DESC_CFG = SET_CONFIG.get (SET_DESC)
if DESC_CFG is None:
    print(f"Set error: Description key not found.\n")
    sys.exit()
print (f"Description: {DESC_CFG}")

# check if settings exist
SETTINGS_CFG = SET_CONFIG.get (SET_SETTINGS)
if SETTINGS_CFG is None:
    print(f"Set error: Set settings not found.\n")
    sys.exit()

# get backup destination
# check if the key exists
DEST_CFG = SETTINGS_CFG.get (SET_DEST)
if DEST_CFG is None:
    print(f"Set error: Backup destination not specified.\n")
    sys.exit()

# check if there's a slash at the end
if DEST_CFG[-1:] != "/":
    print(f"Set error: Backup destination should end with a slash '/'.\n")
    sys.exit()
print (f"Destination folder: {DEST_CFG}")

# check if the actual folder exists
if not os.path.exists (DEST_CFG) \
    or not os.path.isdir (DEST_CFG):
    print(f"Set error: Backup destination folder does not exist.\n")
    sys.exit()

# get files to backup
# check if the key exists
SRC_CFG = SETTINGS_CFG.get (SET_SRC)
if SRC_CFG is None:
    print(f"Set error: Backup source not specified.\n")
    sys.exit()

# check if it's a list
if not isinstance (SRC_CFG, list):
    print(f"Set error: File paths should be a list.\n")
    sys.exit()

# check each file path specified.
# ends with slash, exists
SRC_ERROR = False
for one_path in SRC_CFG:
    if one_path[-1:] != "/":
        print(f"Set error: Source folder should end with a slash '/' - {one_path}.")
        SRC_ERROR = True

    if not os.path.exists (one_path) \
        or not os.path.isdir (one_path):
        print(f"Set error: Source folder does not exist. - {one_path}")
        SRC_ERROR = True

# if there was an error in the source
# paths, exit
if SRC_ERROR:
    print ("There were one or more errors in the source folders.\n")
    sys.exit()

# print the source folders
# and build src string
SRC_FOLDERS = ""
for one_path in SRC_CFG:
    SRC_FOLDERS += one_path + " "
    print (f"Source folder: {one_path}")

print ()

# figure out a filename
NUMBERING = 0
BASE_FILENAME = f"{BACKUP_SETNAME}_{NUMBERING}.tar.gz"
while os.path.exists (DEST_CFG + BASE_FILENAME):
    NUMBERING += 1
    BASE_FILENAME = f"{BACKUP_SETNAME}_{NUMBERING}.tar.gz"

# file checks completed.
# proceed to compression
print (f"Compressing {one_path}")
PARAMS = f"-zcvf {DEST_CFG}{BASE_FILENAME} {SRC_FOLDERS}"
COMMAND = f"tar {PARAMS}"
subprocess.call (COMMAND, shell=True)
