import argparse
import logging
# 

# TODO move to scrapers.py?
scrapers = {'simple-link-scraper': None,
            'simple-image-scraper': None}

# TODO
available_hosts = ()

def cli():
    parser = argparse.ArgumentParser(description='Andrew\'s Custom Command Environment for Linux.')
    subparsers = parser.add_subparsers(dest='cmd', help='Commands')

    scrape_parser = subparsers.add_parser('scrape', help='Automate data collection from the web.')
    scrape_parser.add_argument('scraper', choices=scrapers.keys(), help='The type of content to be scraped.')
    scrape_parser.add_argument('page', type=str, help='Webpage url.')
    scrape_parser.add_argument('-o', '--output', metavar='DIRNAME', dest='output', type=str, default='', action='store', help='Output directory.')

    host_parser = subparsers.add_parser('host', help='Spawn a lightweight server.')
    host_parser.add_argument('helper', choices=available_hosts, help='The custom server.')

    sunnyside_parser = subparsers.add_parser('sunnyside', help='Change your file\'s DNA.')    
    sunnyside_parser.add_argument('shift', type=int, help='Shift amount.')
    sunnyside_parser.add_argument('key', type=str, help='Character key.')

    # TODO intermediate args

    conf_parser = subparsers.add_parser('conf', help='Process a ConfLists.txt file to configure accel builds.')
    conf_parser.add_argument('dir', type=str, help='Location of the ConfLists.txt file.')
    
    make_parser = subparsers.add_parser('make', help='Process a makefile to carry out accel builds.')
    make_parser.add_argument('-v', '--verbose', dest='make_verbose', action='store_true')
    make_parser.add_argument('-j', '--cores', type=int, default=1, help='Number of cores allowed.')
    parser.set_defaults(make_verbose=False)   

    args, rems = parser.parse_known_args()

    # TODO
    print(args)
    print(rems)

    logging.basicConfig(level=logging.INFO)
