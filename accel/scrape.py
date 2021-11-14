from accel.utils.inputs import Input
from accel.core.conversion import Conversion

# TODO
scrapers = {'simple-link-scraper': None,
            'simple-image-scraper': None}

class Scrape(Conversion):
    KEY = 'scrape'
    ALLOWED_TYPES = [
        Input.URL
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Scrape.KEY, help='Automate data collection from the web.')
        Conversion.addParserItems(parser, Scrape.ALLOWED_TYPES)
        parser.add_argument('-s', '--scraper', choices=scrapers.keys(), default='simple-link-scraper', help='The type of content to be scraped.')
        parser.add_argument('-x', '--xpath', type=str, default='', help='XPath to the tag encompassing the objects to be scraped.')
    @staticmethod
    def fromArgs(args):
        return Scrape(args.input, args.output, args.verbose) # TODO
    def __init__(self, input, output, verbose):
        super(Scrape, self).__init__(input, output, verbose)
        raise NotImplementedError
        # check if output is dir and/or file/dir spec %d