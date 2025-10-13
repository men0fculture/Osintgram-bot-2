#!/usr/bin/env python3
import os
import sys
import signal
import argparse

from src import artwork, config
from src import printcolors as pc
from src.hikercli import HikerCLI, hk
from src.Osintgram import Osintgram

# -------------------------------------------------------------
# Platform detection and readline import
# -------------------------------------------------------------
is_windows = os.name == "nt"

try:
    if is_windows:
        import pyreadline3 as readline
    else:
        import readline
except ImportError:
    readline = None

# -------------------------------------------------------------
# Utility: graceful exit
# -------------------------------------------------------------
def signal_handler(sig, frame):
    pc.printout("\nGoodbye!\n", pc.RED)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# -------------------------------------------------------------
# Print banner and help info
# -------------------------------------------------------------
def printlogo():
    pc.printout(artwork.ascii_art, pc.YELLOW)
    pc.printout("\nVersion 1.1 - Developed by Giuseppe Criscione", pc.YELLOW)
    pc.printout(f"\nHikerAPI {hk.__version__} https://hikerapi.com/help/about\n\n", pc.YELLOW)
    pc.printout("Type 'list' to show all allowed commands\n")
    pc.printout("Type 'FILE=y' or 'FILE=n' to enable/disable saving to text files\n")
    pc.printout("Type 'JSON=y' or 'JSON=n' to enable/disable JSON export\n")

# -------------------------------------------------------------
# Command listing
# -------------------------------------------------------------
def cmdlist():
    commands_help = {
        "FILE=y/n": "Enable/disable output to '<target>_<command>.txt'",
        "JSON=y/n": "Enable/disable export to '<target>_<command>.json'",
        "addrs": "Get all registered addresses from photos",
        "cache": "Clear tool cache",
        "captions": "Get photo captions",
        "commentdata": "List all comments on target posts",
        "comments": "Get total comment count",
        "followers": "Get target followers",
        "followings": "Get users followed by target",
        "fwersemail": "Get followers' email",
        "fwingsemail": "Get followings' email",
        "fwersnumber": "Get followers' phone numbers",
        "fwingsnumber": "Get followings' phone numbers",
        "hashtags": "Get hashtags used by target",
        "info": "Get target info",
        "likes": "Get total likes on posts",
        "mediatype": "Get type of media (photo/video)",
        "photodes": "Get photo descriptions",
        "photos": "Download photos",
        "propic": "Download profile picture",
        "stories": "Download stories",
        "tagged": "List users tagged by target",
        "target": "Set new target username",
        "wcommented": "List users who commented on target posts",
        "wtagged": "List users who tagged target",
        "quit / exit": "Exit the tool"
    }

    for cmd, desc in commands_help.items():
        pc.printout(f"{cmd:<15}", pc.YELLOW)
        print(desc)

# -------------------------------------------------------------
# Setup auto-completion
# -------------------------------------------------------------
def setup_completion(commands):
    if not readline:
        return
    def completer(text, state):
        options = [c for c in commands if c.startswith(text)]
        return options[state] if state < len(options) else None

    readline.set_completer(completer)
    try:
        readline.parse_and_bind("tab: complete")
    except Exception:
        pass

# -------------------------------------------------------------
# Quit helper
# -------------------------------------------------------------
def _quit():
    pc.printout("Goodbye!\n", pc.RED)
    sys.exit(0)

# -------------------------------------------------------------
# Argument parser
# -------------------------------------------------------------
parser = argparse.ArgumentParser(
    description="Osintgram: Instagram OSINT tool (cross-platform edition)"
)
parser.add_argument("id", type=str, help="target username")
parser.add_argument("-C", "--cookies", help="clear previous cookies", action="store_true")
parser.add_argument("-j", "--json", help="save output as JSON", action="store_true")
parser.add_argument("-f", "--file", help="save output in text file", action="store_true")
parser.add_argument("-c", "--command", help="execute a single command and exit")
parser.add_argument("-o", "--output", help="output directory for photos")

args = parser.parse_args()

# -------------------------------------------------------------
# Select API backend
# -------------------------------------------------------------
if config.getHikerToken():
    api = HikerCLI(args.id, args.file, args.json, args.command, args.output, args.cookies)
else:
    api = Osintgram(args.id, args.file, args.json, args.command, args.output, args.cookies)

# -------------------------------------------------------------
# Commands dictionary
# -------------------------------------------------------------
commands = {
    "list": cmdlist, "help": cmdlist, "quit": _quit, "exit": _quit,
    "addrs": api.get_addrs, "cache": api.clear_cache, "captions": api.get_captions,
    "commentdata": api.get_comment_data, "comments": api.get_total_comments,
    "followers": api.get_followers, "followings": api.get_followings,
    "fwersemail": api.get_fwersemail, "fwingsemail": api.get_fwingsemail,
    "fwersnumber": api.get_fwersnumber, "fwingsnumber": api.get_fwingsnumber,
    "hashtags": api.get_hashtags, "info": api.get_user_info, "likes": api.get_total_likes,
    "mediatype": api.get_media_type, "photodes": api.get_photo_description,
    "photos": api.get_user_photo, "propic": api.get_user_propic,
    "stories": api.get_user_stories, "tagged": api.get_people_tagged_by_user,
    "target": api.change_target, "wcommented": api.get_people_who_commented,
    "wtagged": api.get_people_who_tagged
}

# -------------------------------------------------------------
# Main loop
# -------------------------------------------------------------
setup_completion(commands)

if not args.command:
    printlogo()

while True:
    cmd = args.command if args.command else input(pc.YELLOW + "Run a command: " + pc.ENDC)
    _cmd = commands.get(cmd.strip())

    if _cmd:
        _cmd()
    elif cmd == "FILE=y":
        api.set_write_file(True)
    elif cmd == "FILE=n":
        api.set_write_file(False)
    elif cmd == "JSON=y":
        api.set_json_dump(True)
    elif cmd == "JSON=n":
        api.set_json_dump(False)
    elif cmd.strip() == "":
        pass
    else:
        pc.printout("Unknown command\n", pc.RED)

    if args.command:
        break
