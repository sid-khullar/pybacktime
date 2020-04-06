"""Backs up files and database as per settings, uploads to destination"""
import json
import sys

SETTINGS_FILE = "backup_settings.json"

try:
    SETTINGS = json.load (open (SETTINGS_FILE, "r"))
except FileNotFoundError:
    print (f"Settings file not found - {SETTINGS_FILE}.\n")
    sys.exit()

BACKUP_FOLDER = SETTINGS.get ("backup_folder")
if BACKUP_FOLDER is None:
    print (f"Backup folder setting not found - backup_folder.")
    sys.exit()

print (BACKUP_FOLDER)
