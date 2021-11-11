import sys
import argparse
from accel.host import Host
from accel.scrape import Scrape
from accel.sunnyside import Sunnyside
from accel.inputs import Input, InputSet
from accel.mp4  import Mp4
from accel.mp3  import Mp3
from accel.pdf  import Pdf
from accel.svg  import Svg
from accel.gif  import Gif
from accel.zip  import Zip
from accel.epub import Epub
from accel.doku import Doku
from accel.html import Html
from accel.conf import Conf
from accel.make import Make

COMMANDS = (
    Host,
    Scrape,
    Sunnyside,
    Zip,
    
    Mp4,
    Mp3,
    Pdf,
    Svg,
    Gif,
    Epub,
    Doku,
    Html,
    Conf,
    Make,
)

COMMAND_MAP = {cmd.KEY: cmd for cmd in COMMANDS}

def cli():
    parser = argparse.ArgumentParser(description='Andrew\'s Custom Command Environment for Linux.')
    subparsers = parser.add_subparsers(dest='cmd', help='Commands')
    for Command in COMMANDS:
        Command.addParserItems(subparsers)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help='Show verbose output.')
    parser.set_defaults(verbose=False)
    args, rems = parser.parse_known_args()
    if args.cmd in COMMAND_MAP:
        exe = COMMAND_MAP[args.cmd](args) 
    else:
        print('Unrecognized command: %s\n' % args.cmd)
        parser.print_help(sys.stderr)
        sys.exit(1)
